from django.urls import path
from . import views

app_name = 'goals'

urlpatterns = [
    path('setup/', views.GoalSetupView.as_view(), name='setup'),
    path('list/', views.GoalSetupView.as_view(), name='list'),
    path('api/set/', views.SetGoalApiView.as_view(), name='api_set'),
]

