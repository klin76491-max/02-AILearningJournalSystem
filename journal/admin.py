from django.contrib import admin
from .models import JournalEntry, BulletItem, MonthlyLog, FutureLogItem, CustomCollection


class BulletItemInline(admin.TabularInline):
    model = BulletItem
    extra = 1
    fields = ('item_type', 'status', 'signifier', 'content', 'order_index')


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'entry_date', 'am_intent', 'mood_score', 'is_reviewed', 'created_at')
    list_filter = ('entry_date', 'mood_score', 'is_reviewed')
    search_fields = ('user__username', 'am_intent', 'pm_reflection', 'raw_input')
    inlines = [BulletItemInline]


@admin.register(BulletItem)
class BulletItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_type', 'status', 'signifier', 'content', 'created_at')
    list_filter = ('item_type', 'status', 'signifier')
    search_fields = ('content', 'user__username')


@admin.register(MonthlyLog)
class MonthlyLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'year', 'month', 'month_focus', 'created_at')
    list_filter = ('year', 'month')


@admin.register(FutureLogItem)
class FutureLogItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_month', 'content', 'is_migrated', 'created_at')
    list_filter = ('target_month', 'is_migrated')


@admin.register(CustomCollection)
class CustomCollectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at')
