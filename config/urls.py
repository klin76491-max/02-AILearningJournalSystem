"""
URL configuration for AI 學習日誌系統（子彈筆記） (The Bullet Journal Method System).
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('inventory/', include('inventory.urls')),
    path('goals/', include('goals.urls')),
    path('journal/', include('journal.urls')),
    path('reports/', include('reports.urls')),
    path('', lambda request: redirect('journal:today')),
]
