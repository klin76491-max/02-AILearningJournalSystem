import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Avg
from .models import AISummaryReport
from journal.models import JournalEntry, BulletItem
from ai_engine.services import AISummaryService

class ReportService:
    @classmethod
    def generate_weekly_report(cls, user: User, end_date: datetime.date = None) -> AISummaryReport:
        if end_date is None:
            end_date = timezone.localdate()
        start_date = end_date - datetime.timedelta(days=6)

        entries = JournalEntry.objects.filter(
            user=user,
            entry_date__gte=start_date,
            entry_date__lte=end_date
        )

        bullets = BulletItem.objects.filter(
            user=user,
            entry__entry_date__gte=start_date,
            entry__entry_date__lte=end_date
        )

        total_bullets = bullets.count()
        task_bullets = bullets.filter(item_type=BulletItem.ItemType.TASK)
        total_tasks = task_bullets.count()
        completed_tasks = task_bullets.filter(status=BulletItem.Status.COMPLETED).count()
        completion_rate = int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0

        note_count = bullets.filter(item_type=BulletItem.ItemType.NOTE).count()
        event_count = bullets.filter(item_type=BulletItem.ItemType.EVENT).count()
        obstacle_count = bullets.filter(item_type=BulletItem.ItemType.OBSTACLE).count()
        reflection_count = bullets.filter(item_type=BulletItem.ItemType.REFLECTION).count()

        avg_mood = entries.aggregate(Avg('mood_score'))['mood_score__avg'] or 3.0

        stats = {
            'total_bullets': total_bullets,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': completion_rate,
            'note_count': note_count,
            'event_count': event_count,
            'obstacle_count': obstacle_count,
            'reflection_count': reflection_count,
            'days_recorded': entries.count(),
            'avg_mood': round(avg_mood, 1)
        }

        sample_bullets = [f"[{b.get_item_type_display()}] {b.content}" for b in bullets[:25]]

        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')

        ai_content = AISummaryService.generate_weekly_report(
            start_date_str=start_str,
            end_date_str=end_str,
            stats=stats,
            sample_bullets=sample_bullets
        )

        report = AISummaryReport.objects.create(
            user=user,
            report_type=AISummaryReport.ReportType.WEEKLY,
            start_date=start_date,
            end_date=end_date,
            title=f"成長週報 ({start_str} ~ {end_str})",
            statistics=stats,
            core_learnings=ai_content.get('core_learnings', ''),
            recurring_obstacles=ai_content.get('recurring_obstacles', ''),
            growth_advice=ai_content.get('growth_advice', '')
        )

        return report
