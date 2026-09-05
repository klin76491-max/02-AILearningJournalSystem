from django.urls import path
from . import views

app_name = 'journal'

urlpatterns = [
    path('', views.JournalCanvasView.as_view(), name='today'),
    path('river/', views.TraceRiverView.as_view(), name='river'),
    path('api/save/', views.SaveTraceApiView.as_view(), name='api_save'),
    path('api/answer/', views.AnswerQuestionApiView.as_view(), name='api_answer'),
]
