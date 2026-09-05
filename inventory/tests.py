import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import MentalInventoryItem
from .services import MentalInventoryService

class InventoryTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='inv_user', email='inv@gmail.com')
        self.client.force_login(self.user)

    def test_save_bulk_inventory(self):
        doing = "每天寫程式\n回覆客戶"
        should = "應該去運動"
        want = "想做一個 Web App\n想讀完子彈筆記"

        count = MentalInventoryService.save_bulk_inventory(self.user, doing, should, want)
        self.assertEqual(count, 5)
        self.assertEqual(MentalInventoryItem.objects.filter(user=self.user).count(), 5)

    def test_sift_item(self):
        item = MentalInventoryItem.objects.create(
            user=self.user,
            inventory_type=MentalInventoryItem.InventoryType.SHOULD_DO,
            content='無效社交'
        )
        res = MentalInventoryService.sift_item(
            self.user, item.id,
            test_status=MentalInventoryItem.TestStatus.DISCARDED
        )
        self.assertTrue(res)
        item.refresh_from_db()
        self.assertEqual(item.test_status, MentalInventoryItem.TestStatus.DISCARDED)

    def test_toggle_focus(self):
        item = MentalInventoryItem.objects.create(
            user=self.user,
            inventory_type=MentalInventoryItem.InventoryType.WANT_TO_DO,
            content='開發子彈筆記系統'
        )
        self.assertFalse(item.is_focus)

        res = MentalInventoryService.toggle_focus(self.user, item.id)
        self.assertTrue(res)
        item.refresh_from_db()
        self.assertTrue(item.is_focus)
        self.assertEqual(item.category, MentalInventoryItem.Category.GOAL)

    def test_wizard_step1_view(self):
        response = self.client.get(reverse('inventory:wizard_step1'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/wizard_step1.html')

    def test_wizard_step2_view(self):
        MentalInventoryItem.objects.create(user=self.user, content='項目1')
        response = self.client.get(reverse('inventory:wizard_step2'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/wizard_step2.html')

    def test_wizard_step3_view(self):
        MentalInventoryItem.objects.create(user=self.user, content='項目1', test_status='kept')
        response = self.client.get(reverse('inventory:wizard_step3'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/wizard_step3.html')

    def test_inventory_list_view(self):
        MentalInventoryItem.objects.create(user=self.user, content='項目1')
        response = self.client.get(reverse('inventory:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/list.html')
