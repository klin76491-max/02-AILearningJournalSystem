from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import GoalProject
from inventory.models import MentalInventoryItem

class GoalsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='goal_user', email='goal@gmail.com')
        self.client.force_login(self.user)

    def test_create_goal_project(self):
        item = MentalInventoryItem.objects.create(
            user=self.user,
            content='做完專案',
            is_focus=True
        )
        goal = GoalProject.objects.create(
            user=self.user,
            inventory_item=item,
            title='專案衝刺',
            why_statement='為了累積作品',
            timeframe=GoalProject.Timeframe.FOUR_MONTHS
        )
        self.assertEqual(goal.title, '專案衝刺')
        self.assertEqual(goal.status, GoalProject.Status.ACTIVE)

    def test_goal_list_view(self):
        response = self.client.get(reverse('goals:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goals/goal_list.html')
