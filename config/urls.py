"""
URL configuration for 留下痕跡：手帳學習日誌 (02-AILearningJournalSystem).
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('accounts/', include('accounts.urls')),
    path('goals/', include('goals.urls')),
    path('journal/', include('journal.urls')),
    path('', lambda request: redirect('journal:today')),
]
