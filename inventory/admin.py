from django.contrib import admin
from .models import MentalInventoryItem

@admin.register(MentalInventoryItem)
class MentalInventoryItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'inventory_type', 'content', 'test_status', 'category', 'is_focus', 'created_at')
    list_filter = ('inventory_type', 'test_status', 'category', 'is_focus')
    search_fields = ('content', 'user__username')
