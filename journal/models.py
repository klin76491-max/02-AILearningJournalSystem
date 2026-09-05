from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class JournalEntry(models.Model):
    """
    每日痕跡手帳主表
    呼應《04_Story.md》第二章：今天做了什麼、學了什麼、哪裡失敗了、為什麼不想做。
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_entries')
    goal = models.ForeignKey(
        'goals.AnchorGoal',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='journal_entries',
        verbose_name="當前方向"
    )
    entry_date = models.DateField(default=timezone.localdate, verbose_name="記錄日期")
    did_today = models.TextField(blank=True, default='', verbose_name="今天做了什麼")
    learned_today = models.TextField(blank=True, default='', verbose_name="今天學到了什麼")
    failed_today = models.TextField(blank=True, default='', verbose_name="哪裡失敗了")
    resistance_today = models.TextField(blank=True, default='', verbose_name="為什麼不想做 / 當下心情")
    raw_content = models.TextField(blank=True, default='', verbose_name="自由速寫純文字")
    weather = models.CharField(max_length=20, default='sunny', blank=True, verbose_name="今日天氣")
    mood = models.CharField(max_length=20, default='chaos', blank=True, verbose_name="今日心情戳記")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最後修改時間")

    class Meta:
        ordering = ['-entry_date']
        unique_together = ('user', 'entry_date')
        verbose_name = "手帳日誌"
        verbose_name_plural = "手帳日誌"

    def __str__(self):
        return f"{self.user.username} - {self.entry_date}"


class SoulReflection(models.Model):
    """
    文字沉澱與靈魂提問
    """
    entry = models.OneToOneField(JournalEntry, on_delete=models.CASCADE, related_name='reflection')
    summary = models.TextField(blank=True, default='', verbose_name="今日簡記 (AI幫忙整理的客觀記錄)")
    blindspot = models.TextField(blank=True, default='', verbose_name="頁緣觀察 (照見盲點與真實)")
    soul_question = models.TextField(blank=True, default='', verbose_name="靈魂提問")
    source = models.CharField(max_length=20, default='default_pool', verbose_name="來源 (gemini / default_pool)")
    user_answer = models.TextField(blank=True, default='', verbose_name="今晚隨筆筆記/回答")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="生成時間")

    class Meta:
        verbose_name = "靈魂反思與提問"
        verbose_name_plural = "靈魂反思與提問"

    def __str__(self):
        return f"Reflection for {self.entry}"
