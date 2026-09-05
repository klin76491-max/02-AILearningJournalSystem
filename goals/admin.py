from django.contrib import admin
from .models import AnchorGoal


@admin.register(AnchorGoal)
class AnchorGoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_active', 'created_at', 'archived_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'why', 'user__username', 'user__email')
