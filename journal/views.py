"""
子彈筆記頁面視圖 (Daily Log, Monthly Log, Future Log, History)
"""

import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from .models import JournalEntry, BulletItem, MonthlyLog, FutureLogItem
from .services import JournalService
from inventory.models import MentalInventoryItem
from goals.models import GoalProject


class TodayJournalView(LoginRequiredMixin, View):
    """今日子彈工作區 (Daily Log)"""

    def get(self, request):
        # 檢查新用戶是否已完成思想盤點
        has_items = MentalInventoryItem.objects.filter(user=request.user).exists()
        if not has_items:
            messages.info(request, "歡迎來到子彈筆記系統！在開始每日日誌前，請先清空大腦，列出你的「人生清單」。")
            return redirect('inventory:wizard_step1')

        today = timezone.localdate()
        entry = JournalService.get_or_create_daily_log(request.user, today)
        bullets = entry.bullets.all().order_by('order_index', 'id')
        
        # 取得使用者最在意的焦點目標與人生清單
        focus_goals = GoalProject.objects.filter(user=request.user, status=GoalProject.Status.ACTIVE)[:3]
        focus_inventory = MentalInventoryItem.objects.filter(user=request.user, is_focus=True)[:5]

        context = {
            'entry': entry,
            'bullets': bullets,
            'today': today,
            'focus_goals': focus_goals,
            'focus_inventory': focus_inventory,
            'total_tasks': entry.get_total_tasks_count(),
            'completed_tasks': entry.get_completed_tasks_count(),
            'completion_rate': entry.get_completion_rate(),
        }
        return render(request, 'journal/today.html', context)

    def post(self, request):
        today = timezone.localdate()
        entry = JournalService.get_or_create_daily_log(request.user, today)

        # 儲存晨間意圖
        if 'save_am' in request.POST:
            am_intent = request.POST.get('am_intent', '')
            JournalService.save_am_intent(request.user, entry, am_intent)
            messages.success(request, "🌅 晨間意圖已儲存，帶著專注開始今天！")
            return redirect('journal:today')

        # 儲存晚間省思
        if 'save_pm' in request.POST:
            pm_reflection = request.POST.get('pm_reflection', '')
            mood_score = int(request.POST.get('mood_score', 3))
            JournalService.save_pm_reflection(request.user, entry, pm_reflection, mood_score)
            messages.success(request, "🌙 今日省思已完成！看見微小累積，安心休息。")
            return redirect('journal:today')

        # 處理快速速記
        if 'rapid_log_submit' in request.POST:
            raw_text = request.POST.get('raw_text', '')
            created = JournalService.parse_and_save_rapid_log(request.user, entry, raw_text)
            messages.success(request, f"成功新增 {len(created)} 個子彈項目！")
            return redirect('journal:today')

        return redirect('journal:today')


class MonthlyLogView(LoginRequiredMixin, View):
    """月誌視圖 (Monthly Log - 日曆頁 + 當月任務)"""

    def get(self, request, year=None, month=None):
        today = timezone.localdate()
        year = int(year) if year else today.year
        month = int(month) if month else today.month

        monthly_log, monthly_bullets = JournalService.get_monthly_log(request.user, year, month)
        
        # 取得該月的所有每日日誌
        month_entries = JournalEntry.objects.filter(
            user=request.user,
            entry_date__year=year,
            entry_date__month=month
        ).order_by('entry_date')

        context = {
            'monthly_log': monthly_log,
            'monthly_bullets': monthly_bullets,
            'month_entries': month_entries,
            'year': year,
            'month': month,
        }
        return render(request, 'journal/monthly.html', context)


class FutureLogView(LoginRequiredMixin, View):
    """未來誌視圖 (Future Log)"""

    def get(self, request):
        future_items = JournalService.get_future_log_items(request.user)
        return render(request, 'journal/future_log.html', {'future_items': future_items})

    def post(self, request):
        target_month_str = request.POST.get('target_month', '')
        content = request.POST.get('content', '')
        if target_month_str and content:
            target_month = datetime.datetime.strptime(target_month_str, '%Y-%m').date().replace(day=1)
            FutureLogItem.objects.create(
                user=request.user,
                target_month=target_month,
                content=content.strip()
            )
            messages.success(request, "成功排入未來誌！")
        return redirect('journal:future_log')


class JournalHistoryView(LoginRequiredMixin, View):
    """歷史生活痕跡與時間軸"""

    def get(self, request):
        entries = JournalEntry.objects.filter(user=request.user).order_by('-entry_date')
        return render(request, 'journal/history.html', {'entries': entries})
