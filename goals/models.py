from django.db import models
from django.contrib.auth.models import User
from inventory.models import MentalInventoryItem

class GoalProject(models.Model):
    """核心焦點目標與專案集合 (54321 拆解)"""
    class Timeframe(models.TextChoices):
        FIVE_YEARS = '5_years', '5 年長期願景 (5 Years)'
        FOUR_MONTHS = '4_months', '4 個月中期衝刺 (4 Months)'
        THREE_WEEKS = '3_weeks', '3 週短期專案 (3 Weeks)'
        TWO_DAYS = '2_days', '2 天具體行動 (2 Days)'
        ONE_HOUR = '1_hour', '1 小時微小起步 (1 Hour)'

    class Status(models.TextChoices):
        ACTIVE = 'active', '進行中'
        COMPLETED = 'completed', '已達成'
        ARCHIVED = 'archived', '已歸檔'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals', verbose_name='使用者')
    inventory_item = models.ForeignKey(
        MentalInventoryItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='derived_goals',
        verbose_name='關聯人生清單'
    )
    title = models.CharField('目標名稱', max_length=150)
    why_statement = models.TextField('核心動機 (Why)', blank=True, help_text='為什麼這個目標對你至關重要？')
    timeframe = models.CharField('時間跨度', max_length=15, choices=Timeframe.choices, default=Timeframe.FOUR_MONTHS)
    status = models.CharField('狀態', max_length=15, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField('建立時間', auto_now_add=True)
    updated_at = models.DateTimeField('更新時間', auto_now=True)

    class Meta:
        verbose_name = '核心目標'
        verbose_name_plural = '核心目標清單'
        ordering = ['-status', 'created_at']

    def __str__(self):
        return f"[{self.get_timeframe_display()}] {self.title}"
