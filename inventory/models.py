from django.db import models
from django.contrib.auth.models import User

class MentalInventoryItem(models.Model):
    """思想盤點 / 人生清單項目"""
    class InventoryType(models.TextChoices):
        DOING = 'doing', '我正在做的事 (What I am doing)'
        SHOULD_DO = 'should_do', '我應該做的事 (What I should do)'
        WANT_TO_DO = 'want_to_do', '我想做的事 (What I want to do)'

    class TestStatus(models.TextChoices):
        PENDING = 'pending', '待篩選'
        KEPT = 'kept', '保留 (重要或有意義)'
        DISCARDED = 'discarded', '劃掉丟棄 (不重要且無意義)'

    class Category(models.TextChoices):
        NONE = 'none', '未分類'
        OBLIGATION = 'obligation', '責任 (Obligations - 必須做的)'
        GOAL = 'goal', '目標 (Goals - 真正追求的)'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventory_items', verbose_name='使用者')
    inventory_type = models.CharField('盤點維度', max_length=20, choices=InventoryType.choices, default=InventoryType.DOING)
    content = models.CharField('項目內容', max_length=250)
    test_status = models.CharField('篩選測試結果', max_length=15, choices=TestStatus.choices, default=TestStatus.PENDING)
    category = models.CharField('分類屬性', max_length=15, choices=Category.choices, default=Category.NONE)
    is_focus = models.BooleanField('是否為當前最在意的核心項目 (Focus)', default=False, db_index=True)
    created_at = models.DateTimeField('建立時間', auto_now_add=True)
    updated_at = models.DateTimeField('更新時間', auto_now=True)

    class Meta:
        verbose_name = '思想盤點項目'
        verbose_name_plural = '思想盤點項目清單'
        ordering = ['inventory_type', '-is_focus', 'id']

    def __str__(self):
        focus_mark = "★ " if self.is_focus else ""
        return f"{focus_mark}[{self.get_inventory_type_display()}] {self.content}"
