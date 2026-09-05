from django.db import models
from django.contrib.auth.models import User


class AnchorGoal(models.Model):
    """
    錨點目標 / 前進方向
    呼應《04_Story.md》：在開始留下痕跡前，為這段日子定一個專注的方向，隨時可以更換。
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='anchor_goals')
    title = models.CharField(max_length=150, verbose_name="目標方向")
    why = models.TextField(blank=True, default='', verbose_name="初心與期待")
    is_active = models.BooleanField(default=True, verbose_name="當前焦點目標")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    archived_at = models.DateTimeField(null=True, blank=True, verbose_name="封存時間")

    class Meta:
        ordering = ['-is_active', '-created_at']
        verbose_name = "錨點目標"
        verbose_name_plural = "錨點目標"

    def __str__(self):
        status = " (當前)" if self.is_active else " (已歸檔)"
        return f"{self.title}{status}"
