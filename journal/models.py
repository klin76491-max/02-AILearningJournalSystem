"""
子彈筆記核心集合與日誌數據模型 (Journal, Monthly Log, Future Log, Custom Collections)
根據 SD 文件 Section 2.3
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from goals.models import GoalProject


class CustomCollection(models.Model):
    """自訂主題群組 (Custom Collection，如讀書清單、習慣追蹤)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_collections', verbose_name='使用者')
    title = models.CharField('群組主題', max_length=100)
    description = models.TextField('說明', blank=True)
    created_at = models.DateTimeField('建立時間', auto_now_add=True)

    class Meta:
        verbose_name = '自訂主題群組'
        verbose_name_plural = '自訂主題群組清單'
        ordering = ['title']

    def __str__(self):
        return self.title


class FutureLogItem(models.Model):
    """未來誌 (Future Log) 跨月預定事項"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='future_log_items', verbose_name='使用者')
    target_month = models.DateField('目標月份 (如 2026-10-01)')
    content = models.CharField('預定事項', max_length=300)
    is_migrated = models.BooleanField('是否已遷移至當月月誌', default=False)
    created_at = models.DateTimeField('建立時間', auto_now_add=True)

    class Meta:
        verbose_name = '未來誌項目'
        verbose_name_plural = '未來誌項目清單'
        ordering = ['target_month', 'id']

    def __str__(self):
        migrated_str = " (已遷移)" if self.is_migrated else ""
        return f"[{self.target_month.strftime('%Y/%m')}] {self.content}{migrated_str}"


class MonthlyLog(models.Model):
    """月誌 (Monthly Log - 日曆頁 + 任務頁)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monthly_logs', verbose_name='使用者')
    year = models.PositiveIntegerField('年份')
    month = models.PositiveSmallIntegerField('月份', validators=[MinValueValidator(1), MaxValueValidator(12)])
    month_focus = models.CharField('當月核心焦點', max_length=200, blank=True)
    created_at = models.DateTimeField('建立時間', auto_now_add=True)

    class Meta:
        verbose_name = '月誌'
        verbose_name_plural = '月誌清單'
        unique_together = ('user', 'year', 'month')
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.year} 年 {self.month} 月月誌 - {self.month_focus or '進行中'}"


class JournalEntry(models.Model):
    """每日子彈日誌 (Daily Log)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_entries', verbose_name='使用者')
    entry_date = models.DateField('日誌日期', default=timezone.localdate, db_index=True)
    am_intent = models.CharField('晨間意圖 / 今日焦點 (AM Intent)', max_length=200, blank=True)
    pm_reflection = models.TextField('晚間省思 / 今日覺察 (PM Reflection)', blank=True)
    mood_score = models.PositiveSmallIntegerField('狀態評分 (1-5)', default=3)
    raw_input = models.TextField('快速速記原始文字', blank=True)
    ai_summary = models.TextField('AI 整理摘要', blank=True)
    ai_reflection = models.TextField('AI 溫暖反思', blank=True)
    is_reviewed = models.BooleanField('是否已完成晚間省思', default=False)
    created_at = models.DateTimeField('建立時間', auto_now_add=True)
    updated_at = models.DateTimeField('更新時間', auto_now=True)

    class Meta:
        verbose_name = '每日日誌'
        verbose_name_plural = '每日日誌清單'
        unique_together = ('user', 'entry_date')
        ordering = ['-entry_date']

    def __str__(self):
        return f"{self.user.username} - {self.entry_date} (AM: {self.am_intent[:15] or '無'})"

    def get_total_tasks_count(self):
        return self.bullets.filter(item_type=BulletItem.ItemType.TASK).count()

    def get_completed_tasks_count(self):
        return self.bullets.filter(item_type=BulletItem.ItemType.TASK, status=BulletItem.Status.COMPLETED).count()

    def get_completion_rate(self):
        total = self.get_total_tasks_count()
        if total == 0:
            return 0
        return int((self.get_completed_tasks_count() / total) * 100)


class BulletItem(models.Model):
    """正宗子彈筆記項目 (Bullet Item)"""
    class ItemType(models.TextChoices):
        TASK = 'task', '• 任務 (Task)'
        NOTE = 'note', '- 筆記 (Note)'
        EVENT = 'event', '○ 事件 (Event)'
        REFLECTION = 'reflection', '★ 反思 (Reflection)'
        OBSTACLE = 'obstacle', '! 阻礙 (Obstacle)'

    class Status(models.TextChoices):
        OPEN = 'open', '• 進行中 (Open)'
        COMPLETED = 'completed', 'x 已完成 (Completed)'
        MIGRATED = 'migrated', '> 遷移至明日/下月 (Migrated)'
        SCHEDULED = 'scheduled', '< 排程至未來誌 (Scheduled)'
        CANCELLED = 'cancelled', '— 劃掉取消 (Irrelevant)'

    class Signifier(models.TextChoices):
        NONE = 'none', '無'
        PRIORITY = 'priority', '* 優先重要 (*)'
        INSPIRATION = 'inspiration', '! 靈感 (!)'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bullets', verbose_name='使用者')
    entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, null=True, blank=True, related_name='bullets', verbose_name='所屬日誌')
    monthly_log = models.ForeignKey(MonthlyLog, on_delete=models.SET_NULL, null=True, blank=True, related_name='monthly_bullets', verbose_name='所屬月誌')
    goal = models.ForeignKey(GoalProject, on_delete=models.SET_NULL, null=True, blank=True, related_name='goal_bullets', verbose_name='關聯目標')
    collection = models.ForeignKey(CustomCollection, on_delete=models.SET_NULL, null=True, blank=True, related_name='collection_bullets', verbose_name='關聯群組')
    
    item_type = models.CharField('項目類型', max_length=20, choices=ItemType.choices, default=ItemType.TASK)
    status = models.CharField('子彈狀態', max_length=20, choices=Status.choices, default=Status.OPEN)
    signifier = models.CharField('符號標記', max_length=20, choices=Signifier.choices, default=Signifier.NONE)
    content = models.CharField('項目內容', max_length=500)
    order_index = models.PositiveIntegerField('排序', default=0)
    created_at = models.DateTimeField('建立時間', auto_now_add=True)
    updated_at = models.DateTimeField('更新時間', auto_now=True)

    class Meta:
        verbose_name = '子彈項目'
        verbose_name_plural = '子彈項目清單'
        ordering = ['order_index', 'id']

    def __str__(self):
        return f"[{self.symbol}] {self.content[:30]}"

    @property
    def is_completed(self):
        return self.status == self.Status.COMPLETED

    @property
    def symbol(self):
        """回傳正宗子彈語法符號"""
        if self.item_type == self.ItemType.TASK:
            if self.status == self.Status.COMPLETED:
                return 'x'
            elif self.status == self.Status.MIGRATED:
                return '>'
            elif self.status == self.Status.SCHEDULED:
                return '<'
            elif self.status == self.Status.CANCELLED:
                return '—'
            return '•'
        elif self.item_type == self.ItemType.NOTE:
            return '-'
        elif self.item_type == self.ItemType.EVENT:
            return '○'
        elif self.item_type == self.ItemType.REFLECTION:
            return '★'
        elif self.item_type == self.ItemType.OBSTACLE:
            return '!'
        return '•'
