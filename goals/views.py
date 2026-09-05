import json
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
from .services import GoalService


class GoalSetupView(LoginRequiredMixin, View):
    """
    手帳第一頁：起步目標設定頁
    """
    template_name = 'goals/setup.html'

    def get(self, request):
        current_goal = GoalService.get_active_goal(request.user)
        return render(request, self.template_name, {
            'current_goal': current_goal,
        })

    def post(self, request):
        title = request.POST.get('title', '').strip()
        why = request.POST.get('why', '').strip()

        if not title:
            messages.error(request, "請寫下一句你想嘗試前進的方向。")
            return render(request, self.template_name, {'title': title, 'why': why})

        try:
            GoalService.set_goal(request.user, title=title, why=why)
            messages.success(request, "方向已定，翻開日記開始留下痕跡。")
            return redirect('journal:today')
        except Exception as e:
            messages.error(request, f"設定目標失敗：{str(e)}")
            return render(request, self.template_name, {'title': title, 'why': why})


class SetGoalApiView(LoginRequiredMixin, View):
    """
    更換焦點目標 API (供 Modal 彈窗非同步呼叫)
    """
    def post(self, request):
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                title = data.get('title', '').strip()
                why = data.get('why', '').strip()
            else:
                title = request.POST.get('title', '').strip()
                why = request.POST.get('why', '').strip()

            if not title:
                return JsonResponse({'success': False, 'error': '請填寫新的方向名稱'}, status=400)

            new_goal = GoalService.set_goal(request.user, title=title, why=why)
            return JsonResponse({
                'success': True,
                'goal': {
                    'id': new_goal.id,
                    'title': new_goal.title,
                    'why': new_goal.why
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
