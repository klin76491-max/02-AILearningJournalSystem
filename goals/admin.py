from django.contrib import admin
from .models import GoalProject

@admin.register(GoalProject)
class GoalProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'timeframe', 'status', 'created_at')
    list_filter = ('timeframe', 'status')
    search_fields = ('title', 'why_statement', 'user__username')
