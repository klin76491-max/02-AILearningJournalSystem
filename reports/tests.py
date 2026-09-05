from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import AISummaryReport
from .services import ReportService
from journal.services import JournalService
from journal.models import BulletItem

class ReportsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='report_tester', email='rep@gmail.com')
        self.client.force_login(self.user)
        self.today = timezone.localdate()

        self.entry = JournalService.get_or_create_daily_log(self.user, self.today)
        JournalService.create_bullet(self.user, self.entry, BulletItem.ItemType.TASK, '週報任務1', status=BulletItem.Status.COMPLETED)
        JournalService.create_bullet(self.user, self.entry, BulletItem.ItemType.NOTE, '週報筆記1')

    def test_generate_weekly_report(self):
        report = ReportService.generate_weekly_report(self.user, self.today)
        self.assertEqual(report.user, self.user)
        self.assertEqual(report.report_type, AISummaryReport.ReportType.WEEKLY)
        self.assertIn('成長週報', report.title)
        self.assertGreaterEqual(report.statistics['total_bullets'], 2)
        self.assertEqual(report.statistics['completed_tasks'], 1)
        self.assertTrue(bool(report.core_learnings))

    def test_report_list_view(self):
        ReportService.generate_weekly_report(self.user, self.today)
        response = self.client.get(reverse('reports:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/report_list.html')
