import os
from django.conf import settings
from agent2_news.models import NewsAlert, NewsResource

def match_headlines_to_rules(headlines):
    triggered_alerts = []

    for resource in NewsResource.objects.all():
        # Get full path to the uploaded resource file
        path = os.path.join(settings.MEDIA_ROOT, resource.file.name)
        if not os.path.exists(path):
            continue

        # Load keywords from file (text-based match)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            keywords = f.read().lower()

        for news in headlines:
            text = (news["title"] + " " + news.get("summary", "")).lower()
            if any(keyword in text for keyword in keywords.split()):
                alert, created = NewsAlert.objects.get_or_create(
                    headline=news["title"],
                    url=news["url"],
                    triggered_by=resource
                )
                if created:
                    triggered_alerts.append(alert)

    return triggered_alerts
