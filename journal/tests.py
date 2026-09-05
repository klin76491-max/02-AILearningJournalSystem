import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from goals.services import GoalService
from .models import JournalEntry, SoulReflection
from .services import EchoService, JournalService


class JournalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='journaler', password='password123')
        self.client = Client()
        self.client.force_login(self.user)
        self.goal = GoalService.set_goal(self.user, title="十四天探索代碼")

    def test_echo_service_priority(self):
        today = timezone.localdate()

        # 首日無任何紀錄時，應返回故事序章典故
        echo = EchoService.get_time_echo(self.user, today)
        self.assertEqual(echo['type'], 'story')

        # 建立 14 天前的日記
        day_14_ago = today - datetime.timedelta(days=14)
        JournalEntry.objects.create(
            user=self.user,
            entry_date=day_14_ago,
            did_today="十四天前開始寫第一個工具"
        )
        echo_14 = EchoService.get_time_echo(self.user, today)
        self.assertEqual(echo_14['type'], '14_days')

        # 建立 7 天前的日記，14 天前仍優先
        day_7_ago = today - datetime.timedelta(days=7)
        JournalEntry.objects.create(
            user=self.user,
            entry_date=day_7_ago,
            did_today="七天前的一點痕跡"
        )
        echo_priority = EchoService.get_time_echo(self.user, today)
        self.assertEqual(echo_priority['type'], '14_days')

    def test_save_trace_service_and_models(self):
        today = timezone.localdate()
        entry, reflection = JournalService.save_trace(
            user=self.user,
            entry_date=today,
            did_today="完成手帳日誌後端架構重構",
            learned_today="越純粹的系統越有生命力",
            failed_today="最初被子彈筆記術語困擾",
            resistance_today="想偷懶但最後克服了"
        )
        self.assertEqual(entry.user, self.user)
        self.assertEqual(entry.goal, self.goal)
        self.assertIsNotNone(entry.reflection)
        self.assertTrue(len(reflection.soul_question) > 0)
        self.assertTrue(len(reflection.summary) > 0)

    def test_save_trace_api(self):
        # 測試全空提交校驗
        empty_res = self.client.post(
            reverse('journal:api_save'),
            data={'did_today': '', 'learned_today': '', 'failed_today': '', 'resistance_today': ''},
            content_type='application/json'
        )
        self.assertEqual(empty_res.status_code, 400)

        # 正常提交
        valid_res = self.client.post(
            reverse('journal:api_save'),
            data={
                'did_today': '寫下了測試用例',
                'learned_today': '單元測試非常重要',
                'failed_today': '有些邏輯一開始漏掉了',
                'resistance_today': '寫測試要耐心'
            },
            content_type='application/json'
        )
        self.assertEqual(valid_res.status_code, 200)
        data = valid_res.json()
        self.assertTrue(data['success'])
        self.assertIn('soul_question', data['reflection'])
        self.assertIn('summary', data['reflection'])

    def test_answer_question_api(self):
        entry, _ = JournalService.save_trace(
            user=self.user,
            did_today="寫日記"
        )
        res = self.client.post(
            reverse('journal:api_answer'),
            data={'entry_id': entry.id, 'answer': '這是我沉思後寫下的回答'},
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        entry.refresh_from_db()
        self.assertEqual(entry.reflection.user_answer, '這是我沉思後寫下的回答')

    def test_canvas_and_river_views(self):
        # Canvas 正常渲染
        canvas_res = self.client.get(reverse('journal:today'))
        self.assertEqual(canvas_res.status_code, 200)
        self.assertContains(canvas_res, "十四天探索代碼")

        # River 正常渲染
        river_res = self.client.get(reverse('journal:river'))
        self.assertEqual(river_res.status_code, 200)
