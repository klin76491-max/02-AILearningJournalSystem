from django.contrib import admin
from .models import AISummaryReport

@admin.register(AISummaryReport)
class AISummaryReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'report_type', 'title', 'start_date', 'end_date', 'created_at')
    list_filter = ('report_type', 'end_date')
    search_fields = ('user__username', 'title', 'core_learnings')
