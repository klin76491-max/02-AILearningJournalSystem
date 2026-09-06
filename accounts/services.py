"""
帳號與 Google OAuth 2.0 認證服務
"""

import os
import requests
from django.contrib.auth.models import User
from django.conf import settings
from urllib.parse import urlencode


class GoogleAuthError(Exception):
    pass


class GoogleAuthService:
    @classmethod
    def get_auth_url(cls, state: str = None, redirect_uri: str = None) -> str:
        client_id = getattr(settings, 'GOOGLE_OAUTH_CLIENT_ID', '') or os.getenv('GOOGLE_OAUTH_CLIENT_ID', '')
        if not redirect_uri:
            redirect_uri = getattr(settings, 'GOOGLE_REDIRECT_URI', 'http://127.0.0.1:8002/accounts/google/callback/')
        auth_endpoint = getattr(settings, 'GOOGLE_AUTH_URL', 'https://accounts.google.com/o/oauth2/v2/auth')

        if not client_id:
            raise GoogleAuthError("未設定 GOOGLE_OAUTH_CLIENT_ID。")

        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile',
            'access_type': 'online',
            'prompt': 'select_account',
        }
        if state:
            params['state'] = state

        return f"{auth_endpoint}?{urlencode(params)}"

    @classmethod
    def exchange_code_for_token(cls, code: str, redirect_uri: str = None) -> dict:
        client_id = getattr(settings, 'GOOGLE_OAUTH_CLIENT_ID', '') or os.getenv('GOOGLE_OAUTH_CLIENT_ID', '')
        client_secret = getattr(settings, 'GOOGLE_OAUTH_CLIENT_SECRET', '') or os.getenv('GOOGLE_OAUTH_CLIENT_SECRET', '')
        if not redirect_uri:
            redirect_uri = getattr(settings, 'GOOGLE_REDIRECT_URI', 'http://127.0.0.1:8002/accounts/google/callback/')
        token_endpoint = getattr(settings, 'GOOGLE_TOKEN_URL', 'https://oauth2.googleapis.com/token')

        if not client_id or not client_secret:
            raise GoogleAuthError("未設定 Google OAuth Client ID 或 Client Secret。")

        payload = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }

        try:
            response = requests.post(token_endpoint, data=payload, timeout=10)
            if response.status_code != 200:
                raise GoogleAuthError(f"Token 交換失敗 (HTTP {response.status_code})：{response.text}")
            return response.json()
        except requests.RequestException as e:
            raise GoogleAuthError(f"連線至 Google Token 服務失敗：{str(e)}")

    @classmethod
    def get_user_profile(cls, access_token: str) -> dict:
        userinfo_endpoint = getattr(settings, 'GOOGLE_USERINFO_URL', 'https://www.googleapis.com/oauth2/v2/userinfo')
        headers = {'Authorization': f'Bearer {access_token}'}

        try:
            response = requests.get(userinfo_endpoint, headers=headers, timeout=10)
            if response.status_code != 200:
                raise GoogleAuthError(f"獲取個人資料失敗 (HTTP {response.status_code})")
            return response.json()
        except requests.RequestException as e:
            raise GoogleAuthError(f"連線至 Google UserInfo 服務失敗：{str(e)}")

    @classmethod
    def get_or_create_google_user(cls, profile: dict) -> User:
        email = profile.get('email')
        if not email:
            raise GoogleAuthError("Google Profile 中未包含有效的電子郵件。")

        name = profile.get('name') or profile.get('given_name') or email.split('@')[0]

        try:
            user = User.objects.get(email=email)
            if name and not user.first_name:
                user.first_name = name[:30]
                user.save(update_fields=['first_name'])
            return user
        except User.DoesNotExist:
            username_base = email.split('@')[0]
            username = username_base
            suffix = 1
            while User.objects.filter(username=username).exists():
                username = f"{username_base}_{suffix}"
                suffix += 1

            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=name[:30]
            )
            return user
