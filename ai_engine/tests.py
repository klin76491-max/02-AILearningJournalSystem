from django.test import TestCase
from .services import AISummaryService

class AIEngineTests(TestCase):
    def test_fallback_rule_parse(self):
        raw_text = """
        • 研讀 Django ORM 查詢優化
        - 筆記：select_related 用於 Foreign key
        ! 踩坑：忘記加 db_index 導致查詢很慢
        ★ 反思：基礎扎實比寫得快更重要
        ○ 晚上 8:00 線上讀書會
        """
        items = AISummaryService.parse_raw_text_to_bullets(raw_text)
        self.assertEqual(len(items), 5)

        types = [item['type'] for item in items]
        self.assertIn('task', types)
        self.assertIn('note', types)
        self.assertIn('obstacle', types)
        self.assertIn('reflection', types)
        self.assertIn('event', types)

    def test_fallback_daily_reflection(self):
        bullets = [
            {'type': 'task', 'content': '完成 SA 文件', 'is_completed': True},
            {'type': 'note', 'content': '學習新架構', 'is_completed': False}
        ]
        res = AISummaryService.generate_daily_reflection('2026-08-15', bullets, mood_score=4)
        self.assertIn('summary', res)
        self.assertIn('reflection', res)
