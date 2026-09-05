from django.test import TestCase
from .services import SoulReflectionEngine
from .default_questions import DEFAULT_SOUL_QUESTIONS


class AIEngineTests(TestCase):
    def test_default_questions_pool_count(self):
        # 驗證內建預設題庫不少於 100 句
        self.assertGreaterEqual(len(DEFAULT_SOUL_QUESTIONS), 100)

    def test_fallback_reflection_generation(self):
        # 測試無 API key 或降級時，能正確產出 summary, blindspot, soul_question
        result = SoulReflectionEngine.generate_reflection(
            did_today="寫了資料庫遷移測試代碼",
            learned_today="學會了 Django atomic 事務",
            failed_today="最初忘了更新 admin",
            resistance_today="有點困想睡覺"
        )
        self.assertIn('summary', result)
        self.assertIn('blindspot', result)
        self.assertIn('soul_question', result)
        self.assertIn('source', result)
        self.assertIn(result['soul_question'], DEFAULT_SOUL_QUESTIONS)
