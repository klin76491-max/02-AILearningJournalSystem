from django.db import models
from django.contrib.auth.models import User

class AISummaryReport(models.Model):
    """AI 週期成長與反思報告 (週報 / 月報)"""
    class ReportType(models.TextChoices):
        WEEKLY = 'weekly', '週報 (Weekly Digest)'
        MONTHLY = 'monthly', '月報 (Monthly Retrospective)'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='summary_reports',
        verbose_name='所屬使用者'
    )
    report_type = models.CharField('報表類型', max_length=10, choices=ReportType.choices, db_index=True)
    start_date = models.DateField('統計起始日', db_index=True)
    end_date = models.DateField('統計結束日', db_index=True)
    title = models.CharField('報告標題', max_length=150)
    statistics = models.JSONField('統計分析數據 (JSON)', default=dict, blank=True)
    core_learnings = models.TextField('核心收穫與累積')
    recurring_obstacles = models.TextField('重複出現的盲點與混亂')
    growth_advice = models.TextField('AI 下一階段行動建議')
    created_at = models.DateTimeField('生成時間', auto_now_add=True)

    class Meta:
        verbose_name = 'AI 週期報告'
        verbose_name_plural = 'AI 週期報告清單'
        ordering = ['-end_date']

    def __str__(self):
        return f"{self.user.username} - {self.get_report_type_display()} ({self.start_date} ~ {self.end_date})"
