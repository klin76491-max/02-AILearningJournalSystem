"""
AJAX / REST API 視圖控制器 - 子彈速記、狀態切換與正宗遷移機制
"""

import json
import datetime
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .models import JournalEntry, BulletItem
from .services import JournalService
from ai_engine.services import AISummaryService


class ParseBulletsAPIView(LoginRequiredMixin, View):
    """接收速記文字，透過 AI 結構化拆解並儲存子彈清單"""

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except Exception:
            data = request.POST

        raw_text = data.get('raw_text', '').strip()
        date_str = data.get('date', '')

        if not raw_text:
            return JsonResponse({'success': False, 'error': '請提供速記內容。'}, status=400)

        target_date = timezone.localdate()
        if date_str:
            try:
                target_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        entry = JournalService.get_or_create_daily_log(request.user, target_date)
        bullets = JournalService.parse_and_save_rapid_log(request.user, entry, raw_text)

        bullets_data = [
            {
                'id': b.id,
                'type': b.item_type,
                'type_display': b.get_item_type_display(),
                'symbol': b.symbol,
                'content': b.content,
                'is_completed': b.is_completed,
                'status': b.status,
                'signifier': b.signifier,
            }
            for b in bullets
        ]

        return JsonResponse({
            'success': True,
            'count': len(bullets),
            'bullets': bullets_data,
            'total_tasks': entry.get_total_tasks_count(),
            'completed_tasks': entry.get_completed_tasks_count(),
            'completion_rate': entry.get_completion_rate(),
        })


class ToggleBulletAPIView(LoginRequiredMixin, View):
    """切換子彈任務勾選狀態 (Open <-> Completed)"""

    def post(self, request, bullet_id):
        res = JournalService.toggle_bullet_status(request.user, bullet_id)
        status_code = 200 if res.get('success') else 400
        return JsonResponse(res, status=status_code)


class MigrateBulletAPIView(LoginRequiredMixin, View):
    """執行正宗子彈筆記遷移機制 (tomorrow / monthly / future / cancel)"""

    def post(self, request, bullet_id):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except Exception:
            data = request.POST

        target = data.get('target', 'tomorrow')
        res = JournalService.migrate_bullet(request.user, bullet_id, target)
        status_code = 200 if res.get('success') else 400
        return JsonResponse(res, status=status_code)


class DeleteBulletAPIView(LoginRequiredMixin, View):
    """刪除單一子彈項目"""

    def post(self, request, bullet_id):
        try:
            bullet = BulletItem.objects.get(id=bullet_id, user=request.user)
            bullet.delete()
            return JsonResponse({'success': True, 'bullet_id': bullet_id})
        except BulletItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': '項目不存在。'}, status=404)


class GenerateReflectionAPIView(LoginRequiredMixin, View):
    """觸發 AI 生成今日摘要與溫暖反思"""

    def post(self, request, date_str):
        try:
            target_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            target_date = timezone.localdate()

        entry = JournalService.get_or_create_daily_log(request.user, target_date)
        bullets = entry.bullets.all()
        bullets_data = [
            {'type': b.item_type, 'content': b.content, 'is_completed': b.is_completed}
            for b in bullets
        ]

        result = AISummaryService.generate_daily_reflection(date_str, bullets_data, entry.mood_score)
        entry.ai_summary = result.get('summary', '')
        entry.ai_reflection = result.get('reflection', '')
        entry.save(update_fields=['ai_summary', 'ai_reflection', 'updated_at'])

        return JsonResponse({
            'success': True,
            'summary': result.get('summary', ''),
            'reflection': result.get('reflection', ''),
        })
