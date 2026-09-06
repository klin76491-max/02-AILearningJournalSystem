"""
URL configuration for 留下痕跡：手帳學習日誌 (02-AILearningJournalSystem).
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('journal/goals/', include('goals.urls')),
    path('journal/accounts/', include('accounts.urls')),
    path('journal/i18n/', include('django.conf.urls.i18n')),
    path('journal/', include('journal.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('accounts/<path:subpath>', lambda request, subpath: redirect(f'/journal/accounts/{subpath}')),
    path('accounts/', lambda request: redirect('/journal/accounts/login/')),
    path('goals/<path:subpath>', lambda request, subpath: redirect(f'/journal/goals/{subpath}')),
    path('goals/', lambda request: redirect('/journal/goals/setup/')),
    path('', lambda request: redirect('journal:today')),
]

from django.conf import settings
from django.views.static import serve
from django.urls import re_path

urlpatterns += [
    re_path(r'^journal/static/(?P<path>.*)$', serve, {'document_root': settings.STATICFILES_DIRS[0]}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATICFILES_DIRS[0]}),
]


