from django.contrib import admin
from .models import ShortenedURL, ClickRecord

class ClickRecordInline(admin.TabularInline):
    model = ClickRecord
    extra = 0
    readonly_fields = ['clicked_at', 'user_agent', 'ip_address', 'referrer']

@admin.register(ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):
    list_display = ['short_code', 'original_url', 'created_by', 'created_at', 'total_clicks', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['short_code', 'original_url']
    readonly_fields = ['short_code', 'total_clicks']
    inlines = [ClickRecordInline]

@admin.register(ClickRecord)
class ClickRecordAdmin(admin.ModelAdmin):
    list_display = ['shortened_url', 'clicked_at', 'ip_address']
    list_filter = ['clicked_at']
    readonly_fields = ['clicked_at', 'user_agent', 'ip_address', 'referrer']
