import json
import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from journal.models import JournalEntry, BulletItem, MonthlyLog, FutureLogItem
from journal.services import JournalService
from inventory.models import MentalInventoryItem


class JournalTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='bujo_tester', email='bujo@gmail.com')
        self.client.force_login(self.user)
        self.today = timezone.localdate()

        # 模擬使用者已完成思想盤點
        MentalInventoryItem.objects.create(
            user=self.user,
            content='核心目標盤點',
            is_focus=True
        )
        self.entry = JournalService.get_or_create_daily_log(self.user, self.today)

    def test_am_intent_and_pm_reflection(self):
        """測試晨間意圖與晚間省思儲存"""
        JournalService.save_am_intent(self.user, self.entry, '今日專注於寫完單元測試')
        self.assertEqual(self.entry.am_intent, '今日專注於寫完單元測試')

        JournalService.save_pm_reflection(self.user, self.entry, '今天雖然遇到 bug，但順利解決', mood_score=4)
        self.assertEqual(self.entry.pm_reflection, '今天雖然遇到 bug，但順利解決')
        self.assertEqual(self.entry.mood_score, 4)
        self.assertTrue(self.entry.is_reviewed)

    def test_create_and_toggle_bullet(self):
        """測試正宗子彈項目符號與狀態切換"""
        bullet = JournalService.create_bullet(
            user=self.user,
            entry=self.entry,
            item_type=BulletItem.ItemType.TASK,
            content='測試子彈任務'
        )
        self.assertEqual(bullet.symbol, '•')
        self.assertEqual(bullet.status, BulletItem.Status.OPEN)

        res = JournalService.toggle_bullet_status(self.user, bullet.id)
        self.assertTrue(res['success'])
        self.assertEqual(res['symbol'], 'x')
        self.assertEqual(res['status'], BulletItem.Status.COMPLETED)

    def test_migration_to_tomorrow(self):
        """測試子彈遷移至明日 (Migrated >)"""
        bullet = JournalService.create_bullet(
            user=self.user,
            entry=self.entry,
            item_type=BulletItem.ItemType.TASK,
            content='未完成的大任務'
        )
        res = JournalService.migrate_bullet(self.user, bullet.id, target='tomorrow')
        self.assertTrue(res['success'])
        bullet.refresh_from_db()
        self.assertEqual(bullet.status, BulletItem.Status.MIGRATED)
        self.assertEqual(bullet.symbol, '>')

        # 驗證明日日誌中已自動新增該項目
        tomorrow_date = self.today + datetime.timedelta(days=1)
        tomorrow_entry = JournalEntry.objects.get(user=self.user, entry_date=tomorrow_date)
        tomorrow_bullets = tomorrow_entry.bullets.filter(content='未完成的大任務')
        self.assertEqual(tomorrow_bullets.count(), 1)

    def test_migration_to_future_log(self):
        """測試子彈排程至未來誌 (Scheduled <)"""
        bullet = JournalService.create_bullet(
            user=self.user,
            entry=self.entry,
            item_type=BulletItem.ItemType.TASK,
            content='下個月再做的規劃'
        )
        res = JournalService.migrate_bullet(self.user, bullet.id, target='future')
        self.assertTrue(res['success'])
        bullet.refresh_from_db()
        self.assertEqual(bullet.status, BulletItem.Status.SCHEDULED)
        self.assertEqual(bullet.symbol, '<')
        self.assertTrue(FutureLogItem.objects.filter(user=self.user, content='下個月再做的規劃').exists())

    def test_migration_cancel(self):
        """測試子彈取消放手 (Cancelled —)"""
        bullet = JournalService.create_bullet(
            user=self.user,
            entry=self.entry,
            item_type=BulletItem.ItemType.TASK,
            content='不重要的雜訊'
        )
        res = JournalService.migrate_bullet(self.user, bullet.id, target='cancel')
        self.assertTrue(res['success'])
        bullet.refresh_from_db()
        self.assertEqual(bullet.status, BulletItem.Status.CANCELLED)
        self.assertEqual(bullet.symbol, '—')

    def test_today_view(self):
        """測試今日工作區正常渲染"""
        response = self.client.get(reverse('journal:today'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/today.html')

    def test_monthly_log_view(self):
        """測試月誌頁面視圖"""
        response = self.client.get(reverse('journal:monthly'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/monthly.html')

    def test_future_log_view(self):
        """測試未來誌頁面視圖"""
        response = self.client.get(reverse('journal:future_log'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/future_log.html')
