from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.ReportListView.as_view(), name='list'),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='detail'),
    path('generate-weekly/', views.GenerateWeeklyReportView.as_view(), name='generate_weekly'),
]
