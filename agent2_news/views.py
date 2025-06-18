from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.conf import settings

from .models import NewsResource, NewsAlert
from .forms import ResourceUploadForm
from .rss_monitor import fetch_latest_news
from .responder import match_headlines_to_rules


@csrf_exempt
def upload_resource(request):
    if request.method == 'POST':
        form = ResourceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save()
            return redirect('alerts')  # redirect to alerts page after upload
    else:
        form = ResourceUploadForm()
    return render(request, 'agent2/upload.html', {'form': form})


def fetch_and_react(request):
    news = fetch_latest_news()
    triggered = match_headlines_to_rules(news)

    # Email notifications (if any match)
    if triggered and settings.EMAIL_HOST_USER:
        for alert in triggered:
            send_mail(
                subject='🛎️ AI Alert Triggered!',
                message=f"Headline: {alert.headline}\nURL: {alert.url}\nMatched Rule: {alert.triggered_by.title}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],  # send to self/client
                fail_silently=True,
            )

    return redirect('alerts')


def list_alerts(request):
    alerts = NewsAlert.objects.all().order_by('-matched_on')
    return render(request, 'agent2/alerts.html', {'alerts': alerts})

