from django.urls import path
from . import views

app_name = 'goals'

urlpatterns = [
    path('', views.GoalListView.as_view(), name='list'),
]
