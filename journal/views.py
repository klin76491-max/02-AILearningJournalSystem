import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from goals.services import GoalService
from goals.models import AnchorGoal
from .models import JournalEntry, SoulReflection
from .services import EchoService, JournalService


class JournalCanvasView(LoginRequiredMixin, View):
    """
    今日書寫畫布 (手帳雙頁)
    """
    template_name = 'journal/canvas.html'

    def get(self, request):
        active_goal = GoalService.get_active_goal(request.user)
        if not active_goal:
            return redirect('goals:setup')

        today = timezone.localdate()
        today_entry = JournalEntry.objects.filter(user=request.user, entry_date=today).first()
        time_echo = EchoService.get_time_echo(request.user, today)

        return render(request, self.template_name, {
            'active_goal': active_goal,
            'today': today,
            'entry': today_entry,
            'reflection': getattr(today_entry, 'reflection', None) if today_entry else None,
            'time_echo': time_echo,
        })


class SaveTraceApiView(LoginRequiredMixin, View):
    """
    保存今日痕跡並觸發文字沉澱與靈魂提問
    """
    def post(self, request):
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            did_today = data.get('did_today', '').strip()
            learned_today = data.get('learned_today', '').strip()
            failed_today = data.get('failed_today', '').strip()
            resistance_today = data.get('resistance_today', '').strip()
            raw_content = data.get('raw_content', '').strip()
            weather = data.get('weather', 'sunny').strip()
            mood = data.get('mood', 'chaos').strip()

            if not any([did_today, learned_today, failed_today, resistance_today, raw_content]):
                return JsonResponse({'success': False, 'error': '請至少留下一句今天的微小痕跡。'}, status=400)

            entry, reflection = JournalService.save_trace(
                user=request.user,
                entry_date=timezone.localdate(),
                did_today=did_today,
                learned_today=learned_today,
                failed_today=failed_today,
                resistance_today=resistance_today,
                raw_content=raw_content,
                weather=weather,
                mood=mood
            )

            return JsonResponse({
                'success': True,
                'entry_id': entry.id,
                'reflection': {
                    'summary': reflection.summary,
                    'blindspot': reflection.blindspot,
                    'soul_question': reflection.soul_question,
                    'source': reflection.source,
                    'user_answer': reflection.user_answer,
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


class AnswerQuestionApiView(LoginRequiredMixin, View):
    """
    記錄對靈魂提問的心得回答
    """
    def post(self, request):
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            entry_id = data.get('entry_id')
            answer = data.get('answer', '').strip()

            if not entry_id:
                return JsonResponse({'success': False, 'error': '未提供日記識別碼'}, status=400)

            entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
            if hasattr(entry, 'reflection'):
                entry.reflection.user_answer = answer
                entry.reflection.save(update_fields=['user_answer'])

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


class TraceRiverView(LoginRequiredMixin, View):
    """
    時間河流：翻閱過去的痕跡
    """
    template_name = 'journal/river.html'

    def get(self, request):
        entries = JournalEntry.objects.filter(user=request.user).select_related('goal', 'reflection').order_by('-entry_date')

        goal_id = request.GET.get('goal')
        if goal_id:
            entries = entries.filter(goal_id=goal_id)

        all_goals = AnchorGoal.objects.filter(user=request.user).order_by('-created_at')

        paginator = Paginator(entries, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {
            'page_obj': page_obj,
            'all_goals': all_goals,
            'current_goal_filter': int(goal_id) if goal_id and goal_id.isdigit() else None,
        })
