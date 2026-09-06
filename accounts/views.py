"""
accounts 視圖
"""

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import login, logout
from django.conf import settings
from .services import GoogleAuthService, GoogleAuthError


class LoginView(TemplateView):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('journal:today')
        return super().get(request, *args, **kwargs)


from django.urls import reverse


class GoogleLoginView(View):
    def get(self, request):
        try:
            redirect_uri = getattr(settings, 'GOOGLE_REDIRECT_URI', '')
            if not redirect_uri:
                redirect_uri = request.build_absolute_uri(reverse('accounts:google_callback'))
            auth_url = GoogleAuthService.get_auth_url(redirect_uri=redirect_uri)
            return redirect(auth_url)
        except GoogleAuthError as e:
            messages.error(request, f"Google 登入暫時不可用：{str(e)}")
            return redirect('accounts:login')


class GoogleCallbackView(View):
    def get(self, request):
        code = request.GET.get('code')
        error = request.GET.get('error')

        if error:
            messages.error(request, f"Google 授權失敗：{error}")
            return redirect('accounts:login')

        if not code:
            messages.error(request, "未收到 Google 授權碼，登入失敗。")
            return redirect('accounts:login')

        try:
            redirect_uri = getattr(settings, 'GOOGLE_REDIRECT_URI', '')
            if not redirect_uri:
                redirect_uri = request.build_absolute_uri(reverse('accounts:google_callback'))

            token_data = GoogleAuthService.exchange_code_for_token(code, redirect_uri=redirect_uri)
            access_token = token_data.get('access_token')

            if not access_token:
                messages.error(request, "無法取得 Google 授權憑證。")
                return redirect('accounts:login')

            profile = GoogleAuthService.get_user_profile(access_token)
            user = GoogleAuthService.get_or_create_google_user(profile)
            login(request, user)
            messages.success(request, f"歡迎回來，{user.first_name or user.username}！已成功使用 Google 帳號登入。")

            return redirect('journal:today')

        except GoogleAuthError as e:
            messages.error(request, f"Google 登入失敗：{str(e)}")
            return redirect('accounts:login')

        except Exception:
            messages.error(request, "登入處理發生未預期錯誤，請稍後再試。")
            return redirect('accounts:login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "您已安全登出。")
        return redirect('accounts:login')

    def post(self, request):
        logout(request)
        messages.info(request, "您已安全登出。")
        return redirect('accounts:login')


class DevLoginView(View):
    """
    僅在 DEBUG=True 時供本機與測試用一鍵登入
    """
    def get(self, request):
        if not settings.DEBUG:
            return redirect('accounts:login')
        from django.contrib.auth.models import User
        user, _ = User.objects.get_or_create(
            username='explorer',
            defaults={'email': 'explorer@example.com', 'first_name': '探索者'}
        )
        login(request, user)
        return redirect('journal:today')
