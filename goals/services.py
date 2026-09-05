from django.utils import timezone
from django.db import transaction
from .models import AnchorGoal


class GoalService:
    @classmethod
    def get_active_goal(cls, user):
        """獲取使用者當前生效的焦點目標"""
        return AnchorGoal.objects.filter(user=user, is_active=True).first()

    @classmethod
    @transaction.atomic
    def set_goal(cls, user, title, why=''):
        """
        設定或更換新目標：
        自動將舊的 active 目標標記為封存，建立並返回新目標。
        """
        title = (title or '').strip()
        if not title:
            raise ValueError("目標方向不能為空")

        # 封存舊目標
        AnchorGoal.objects.filter(user=user, is_active=True).update(
            is_active=False,
            archived_at=timezone.now()
        )

        # 建立新目標
        new_goal = AnchorGoal.objects.create(
            user=user,
            title=title,
            why=(why or '').strip(),
            is_active=True
        )
        return new_goal
