from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('google/login/', views.GoogleLoginView.as_view(), name='google_login'),
    path('google/callback/', views.GoogleCallbackView.as_view(), name='google_callback'),
    path('dev-login/', views.DevLoginView.as_view(), name='dev_login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
