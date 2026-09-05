from django.contrib import admin
from .models import JournalEntry, SoulReflection


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'entry_date', 'goal', 'created_at')
    list_filter = ('entry_date', 'created_at')
    search_fields = ('user__username', 'did_today', 'learned_today', 'failed_today', 'resistance_today')


@admin.register(SoulReflection)
class SoulReflectionAdmin(admin.ModelAdmin):
    list_display = ('entry', 'source', 'soul_question', 'created_at')
    list_filter = ('source', 'created_at')
    search_fields = ('summary', 'blindspot', 'soul_question', 'user_answer')
