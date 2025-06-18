from django.contrib import admin
from .models import NewsResource, NewsAlert


@admin.register(NewsResource)
class NewsResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)
    list_filter = ('uploaded_at',)
    ordering = ('-uploaded_at',)


@admin.register(NewsAlert)
class NewsAlertAdmin(admin.ModelAdmin):
    list_display = ('short_headline', 'matched_on', 'triggered_by')
    search_fields = ('headline',)
    list_filter = ('matched_on', 'triggered_by')
    date_hierarchy = 'matched_on'
    ordering = ('-matched_on',)

    def short_headline(self, obj):
        return obj.headline[:80] + ("..." if len(obj.headline) > 80 else "")
    short_headline.short_description = "Headline"

