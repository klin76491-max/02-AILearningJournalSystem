"""
journal 路由規劃
"""

from django.urls import path
from . import views, api_views

app_name = 'journal'

urlpatterns = [
    # 頁面路由
    path('today/', views.TodayJournalView.as_view(), name='today'),
    path('monthly/', views.MonthlyLogView.as_view(), name='monthly'),
    path('monthly/<int:year>/<int:month>/', views.MonthlyLogView.as_view(), name='monthly_detail'),
    path('future-log/', views.FutureLogView.as_view(), name='future_log'),
    path('history/', views.JournalHistoryView.as_view(), name='history'),

    # AJAX API 端點
    path('api/parse-bullets/', api_views.ParseBulletsAPIView.as_view(), name='api_parse_bullets'),
    path('api/bullets/<int:bullet_id>/toggle/', api_views.ToggleBulletAPIView.as_view(), name='api_toggle_bullet'),
    path('api/bullets/<int:bullet_id>/migrate/', api_views.MigrateBulletAPIView.as_view(), name='api_migrate_bullet'),
    path('api/bullets/<int:bullet_id>/delete/', api_views.DeleteBulletAPIView.as_view(), name='api_delete_bullet'),
    path('api/entry/<str:date_str>/reflection/', api_views.GenerateReflectionAPIView.as_view(), name='api_generate_reflection'),
]
