from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


class NewsResource(models.Model):
    """Uploaded resource used to evaluate news content."""
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='news_resources/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class NewsAlert(models.Model):
    """News article that matched a resource trigger."""
    headline = models.TextField()
    url = models.URLField()
    matched_on = models.DateTimeField(auto_now_add=True)
    triggered_by = models.ForeignKey(NewsResource, on_delete=models.CASCADE)

    def __str__(self):
        return f"ALERT: {self.headline[:50]}..."


# ✅ Auto email when a new alert is created (Upgrade 3)
@receiver(post_save, sender=NewsAlert)
def send_alert_email(sender, instance, created, **kwargs):
    if created and settings.EMAIL_HOST_USER:
        send_mail(
            subject='🛎️ AI Compliance Alert Triggered',
            message=(
                f"📰 Headline: {instance.headline}\n"
                f"🔗 URL: {instance.url}\n"
                f"📄 Triggered by: {instance.triggered_by.title}\n"
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],  # Replace with client email
            fail_silently=True,
        )

