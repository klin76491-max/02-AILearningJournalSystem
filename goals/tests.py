from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import AnchorGoal
from .services import GoalService


class GoalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='password123')
        self.client = Client()
        self.client.force_login(self.user)

    def test_set_and_switch_goal(self):
        # 設定第一個目標
        goal1 = GoalService.set_goal(self.user, title="十四天挑戰", why="想試試看")
        self.assertTrue(goal1.is_active)
        self.assertEqual(AnchorGoal.objects.filter(user=self.user, is_active=True).count(), 1)

        # 更換第二個目標
        goal2 = GoalService.set_goal(self.user, title="學好英文會話", why="探索新世界")
        self.assertTrue(goal2.is_active)
        goal1.refresh_from_db()
        self.assertFalse(goal1.is_active)
        self.assertIsNotNone(goal1.archived_at)
        self.assertEqual(GoalService.get_active_goal(self.user), goal2)

    def test_goal_setup_view(self):
        response = self.client.get(reverse('goals:setup'))
        self.assertEqual(response.status_code, 200)

        post_response = self.client.post(reverse('goals:setup'), {
            'title': '每天寫三行程式',
            'why': '拉近想與做'
        })
        self.assertEqual(post_response.status_code, 302)
        active_goal = GoalService.get_active_goal(self.user)
        self.assertIsNotNone(active_goal)
        self.assertEqual(active_goal.title, '每天寫三行程式')

    def test_set_goal_api(self):
        response = self.client.post(
            reverse('goals:api_set'),
            data={'title': '新 API 目標', 'why': '測試用'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['goal']['title'], '新 API 目標')
