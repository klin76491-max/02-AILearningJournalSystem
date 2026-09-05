"""
正宗子彈筆記業務服務層 (JournalService)
處理日誌 (Daily Log)、月誌 (Monthly Log)、未來誌 (Future Log)、晨晚省思與正宗遷移機制 (Migration)
"""

import datetime
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.models import User
from .models import JournalEntry, BulletItem, MonthlyLog, FutureLogItem, CustomCollection
from ai_engine.services import AISummaryService


class JournalService:
    """子彈筆記核心業務操作"""

    @classmethod
    def get_or_create_daily_log(cls, user: User, entry_date: datetime.date = None) -> JournalEntry:
        """獲取或建立指定日期的日誌"""
        if entry_date is None:
            entry_date = timezone.localdate()

        entry, created = JournalEntry.objects.get_or_create(
            user=user,
            entry_date=entry_date,
            defaults={
                'mood_score': 3,
            }
        )
        return entry

    @classmethod
    def save_am_intent(cls, user: User, entry: JournalEntry, am_intent: str) -> None:
        """儲存晨間意圖 (AM Intent)"""
        entry.am_intent = am_intent.strip()
        entry.save(update_fields=['am_intent', 'updated_at'])

    @classmethod
    def save_pm_reflection(cls, user: User, entry: JournalEntry, pm_reflection: str, mood_score: int = 3) -> None:
        """儲存晚間省思 (PM Reflection)"""
        entry.pm_reflection = pm_reflection.strip()
        entry.mood_score = max(1, min(5, mood_score))
        entry.is_reviewed = True
        entry.save(update_fields=['pm_reflection', 'mood_score', 'is_reviewed', 'updated_at'])

    @classmethod
    def create_bullet(cls, user: User, entry: JournalEntry = None, item_type: str = 'task',
                      content: str = '', signifier: str = 'none', status: str = 'open',
                      monthly_log: MonthlyLog = None, goal=None, collection=None) -> BulletItem:
        """建立單一子彈項目"""
        with transaction.atomic():
            order_count = 0
            if entry:
                order_count = BulletItem.objects.filter(entry=entry).count()
            elif monthly_log:
                order_count = BulletItem.objects.filter(monthly_log=monthly_log).count()

            bullet = BulletItem.objects.create(
                user=user,
                entry=entry,
                monthly_log=monthly_log,
                goal=goal,
                collection=collection,
                item_type=item_type,
                content=content.strip(),
                signifier=signifier,
                status=status,
                order_index=order_count
            )
            return bullet

    @classmethod
    def parse_and_save_rapid_log(cls, user: User, entry: JournalEntry, raw_text: str) -> list:
        """
        將速記純文字交由 AI (或降級規則) 解析後建立 BulletItem 清單
        """
        if not raw_text.strip():
            return []

        parsed_items = AISummaryService.parse_raw_text_to_bullets(raw_text)

        created_bullets = []
        with transaction.atomic():
            if entry.raw_input:
                entry.raw_input += f"\n{raw_text}"
            else:
                entry.raw_input = raw_text
            entry.save(update_fields=['raw_input', 'updated_at'])

            start_order = BulletItem.objects.filter(entry=entry).count()
            for i, item_data in enumerate(parsed_items):
                item_type = item_data.get('type', 'task')
                if item_type not in BulletItem.ItemType.values:
                    item_type = 'task'

                content = item_data.get('content', '').strip()
                if not content:
                    continue

                signifier = 'priority' if item_data.get('priority') == 'high' else 'none'
                status = BulletItem.Status.COMPLETED if item_data.get('is_completed') else BulletItem.Status.OPEN

                bullet = BulletItem.objects.create(
                    user=user,
                    entry=entry,
                    item_type=item_type,
                    content=content,
                    signifier=signifier,
                    status=status,
                    order_index=start_order + i
                )
                created_bullets.append(bullet)

        return created_bullets

    @classmethod
    def toggle_bullet_status(cls, user: User, bullet_id: int) -> dict:
        """切換子彈任務狀態 (Open <-> Completed)"""
        try:
            bullet = BulletItem.objects.get(id=bullet_id, user=user)
            if bullet.status == BulletItem.Status.COMPLETED:
                bullet.status = BulletItem.Status.OPEN
            else:
                bullet.status = BulletItem.Status.COMPLETED

            bullet.save(update_fields=['status', 'updated_at'])

            completion_rate = 0
            total_tasks = 0
            completed_tasks = 0
            if bullet.entry:
                total_tasks = bullet.entry.get_total_tasks_count()
                completed_tasks = bullet.entry.get_completed_tasks_count()
                completion_rate = bullet.entry.get_completion_rate()

            return {
                'success': True,
                'bullet_id': bullet.id,
                'status': bullet.status,
                'symbol': bullet.symbol,
                'is_completed': bullet.is_completed,
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'completion_rate': completion_rate
            }
        except BulletItem.DoesNotExist:
            return {'success': False, 'error': '項目不存在。'}

    @classmethod
    def migrate_bullet(cls, user: User, bullet_id: int, target: str) -> dict:
        """
        執行正宗遷移機制 (Migration)
        target:
        - 'tomorrow': 標記當前子彈為 `migrated (>)`，並在明日日誌自動建立一個新待辦
        - 'monthly': 遷移至當月月誌
        - 'future': 標記為 `scheduled (<)` 並寫入未來誌 (Future Log)
        - 'cancel': 標記為 `cancelled (—)` 劃掉不再進行
        """
        try:
            with transaction.atomic():
                bullet = BulletItem.objects.get(id=bullet_id, user=user)

                if target == 'tomorrow':
                    bullet.status = BulletItem.Status.MIGRATED
                    bullet.save(update_fields=['status', 'updated_at'])

                    tomorrow_date = (bullet.entry.entry_date if bullet.entry else timezone.localdate()) + datetime.timedelta(days=1)
                    tomorrow_entry = cls.get_or_create_daily_log(user, tomorrow_date)
                    new_bullet = cls.create_bullet(
                        user=user,
                        entry=tomorrow_entry,
                        item_type=bullet.item_type,
                        content=bullet.content,
                        signifier=bullet.signifier
                    )
                    return {'success': True, 'action': 'migrated_tomorrow', 'new_bullet_id': new_bullet.id, 'symbol': bullet.symbol}

                elif target == 'monthly':
                    bullet.status = BulletItem.Status.MIGRATED
                    bullet.save(update_fields=['status', 'updated_at'])

                    entry_date = bullet.entry.entry_date if bullet.entry else timezone.localdate()
                    monthly_log, _ = MonthlyLog.objects.get_or_create(user=user, year=entry_date.year, month=entry_date.month)
                    cls.create_bullet(
                        user=user,
                        monthly_log=monthly_log,
                        item_type=bullet.item_type,
                        content=bullet.content
                    )
                    return {'success': True, 'action': 'migrated_monthly', 'symbol': bullet.symbol}

                elif target == 'future':
                    bullet.status = BulletItem.Status.SCHEDULED
                    bullet.save(update_fields=['status', 'updated_at'])

                    entry_date = bullet.entry.entry_date if bullet.entry else timezone.localdate()
                    next_month = (entry_date.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
                    FutureLogItem.objects.create(
                        user=user,
                        target_month=next_month,
                        content=bullet.content
                    )
                    return {'success': True, 'action': 'scheduled_future', 'symbol': bullet.symbol}

                elif target == 'cancel':
                    bullet.status = BulletItem.Status.CANCELLED
                    bullet.save(update_fields=['status', 'updated_at'])
                    return {'success': True, 'action': 'cancelled', 'symbol': bullet.symbol}

                return {'success': False, 'error': '未知的遷移目標。'}

        except BulletItem.DoesNotExist:
            return {'success': False, 'error': '項目不存在。'}

    @classmethod
    def get_monthly_log(cls, user: User, year: int, month: int) -> tuple[MonthlyLog, list]:
        """獲取月誌與當月任務清單"""
        monthly_log, _ = MonthlyLog.objects.get_or_create(user=user, year=year, month=month)
        monthly_bullets = monthly_log.monthly_bullets.all()
        return monthly_log, monthly_bullets

    @classmethod
    def get_future_log_items(cls, user: User) -> list:
        """獲取未來誌項目"""
        return FutureLogItem.objects.filter(user=user).order_by('target_month', 'id')
