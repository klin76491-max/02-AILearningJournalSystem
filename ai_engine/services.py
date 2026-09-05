"""
AI 服務層 (AISummaryService)
"""

import os
import json
import re
import logging
from django.conf import settings
from .prompts import (
    BULLET_PARSING_SYSTEM_PROMPT,
    DAILY_REFLECTION_PROMPT_TEMPLATE,
    WEEKLY_REPORT_PROMPT_TEMPLATE
)

logger = logging.getLogger(__name__)


class AISummaryService:
    @classmethod
    def get_api_key(cls) -> str:
        return getattr(settings, 'GEMINI_API_KEY', '') or os.getenv('GEMINI_API_KEY', '')

    @classmethod
    def get_client(cls):
        api_key = cls.get_api_key()
        if not api_key or api_key.startswith('mock-') or api_key == 'your-google-gemini-api-key':
            return None
        try:
            from google import genai
            return genai.Client(api_key=api_key)
        except Exception as e:
            logger.warning(f"無法初始化 Google GenAI Client：{e}")
            return None

    @classmethod
    def _clean_json_response(cls, text: str) -> str:
        cleaned = text.strip()
        if cleaned.startswith('```json'):
            cleaned = cleaned[7:]
        elif cleaned.startswith('```'):
            cleaned = cleaned[3:]
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]
        return cleaned.strip()

    @classmethod
    def parse_raw_text_to_bullets(cls, raw_text: str) -> list:
        if not raw_text or not raw_text.strip():
            return []

        client = cls.get_client()
        if not client:
            return cls._fallback_rule_parse(raw_text)

        try:
            from google.genai import types
            prompt = f"{BULLET_PARSING_SYSTEM_PROMPT}\n\n【使用者輸入文字】：\n{raw_text}"
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2
                )
            )
            cleaned_text = cls._clean_json_response(response.text)
            data = json.loads(cleaned_text)
            if isinstance(data, list):
                validated = []
                for item in data:
                    if isinstance(item, dict) and 'content' in item:
                        validated.append({
                            'type': item.get('type', 'task'),
                            'content': str(item.get('content', '')).strip(),
                            'is_completed': bool(item.get('is_completed', False)),
                            'priority': item.get('priority', 'none')
                        })
                return validated if validated else cls._fallback_rule_parse(raw_text)
            return cls._fallback_rule_parse(raw_text)
        except Exception as e:
            logger.error(f"Gemini 子彈解析錯誤，切換至降級規則：{e}")
            return cls._fallback_rule_parse(raw_text)

    @classmethod
    def generate_daily_reflection(cls, entry_date_str: str, bullets_data: list, mood_score: int = 3) -> dict:
        client = cls.get_client()
        if not client or not bullets_data:
            return cls._fallback_daily_reflection(bullets_data, mood_score)

        bullets_text = "\n".join([
            f"- [{b.get('type', 'item')}] {'[x]' if b.get('is_completed') else '[ ]'} {b.get('content', '')}"
            for b in bullets_data
        ])

        prompt = DAILY_REFLECTION_PROMPT_TEMPLATE.format(
            entry_date=entry_date_str,
            mood_score=mood_score,
            bullets_text=bullets_text
        )

        try:
            from google.genai import types
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.7
                )
            )
            cleaned_text = cls._clean_json_response(response.text)
            result = json.loads(cleaned_text)
            if isinstance(result, dict) and 'summary' in result and 'reflection' in result:
                return result
            return cls._fallback_daily_reflection(bullets_data, mood_score)
        except Exception as e:
            logger.error(f"Gemini 反思生成錯誤，切換至降級生成：{e}")
            return cls._fallback_daily_reflection(bullets_data, mood_score)

    @classmethod
    def generate_weekly_report(cls, start_date_str: str, end_date_str: str, stats: dict, sample_bullets: list) -> dict:
        client = cls.get_client()
        if not client:
            return cls._fallback_weekly_report(stats)

        bullets_str = "\n".join([f"- {b}" for b in sample_bullets[:20]])
        prompt = WEEKLY_REPORT_PROMPT_TEMPLATE.format(
            start_date=start_date_str,
            end_date=end_date_str,
            total_bullets=stats.get('total_bullets', 0),
            total_tasks=stats.get('total_tasks', 0),
            completed_tasks=stats.get('completed_tasks', 0),
            completion_rate=stats.get('completion_rate', 0),
            note_count=stats.get('note_count', 0),
            obstacle_count=stats.get('obstacle_count', 0),
            reflection_count=stats.get('reflection_count', 0),
            sample_bullets=bullets_str or '無明細'
        )

        try:
            from google.genai import types
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.6
                )
            )
            cleaned_text = cls._clean_json_response(response.text)
            result = json.loads(cleaned_text)
            if isinstance(result, dict) and 'core_learnings' in result:
                return result
            return cls._fallback_weekly_report(stats)
        except Exception as e:
            logger.error(f"Gemini 週報生成失敗，使用降級內容：{e}")
            return cls._fallback_weekly_report(stats)

    @classmethod
    def _fallback_rule_parse(cls, raw_text: str) -> list:
        items = []
        for line in raw_text.splitlines():
            line = line.strip()
            if not line:
                continue

            clean_content = re.sub(r'#\w+', '', line).strip()

            if line.startswith(('•', '*', '[ ]', '1.', '2.', '3.', '4.', '5.')):
                items.append({
                    'type': 'task',
                    'content': clean_content.lstrip('•*[]1234567890. '),
                    'is_completed': False,
                    'priority': 'none'
                })
            elif line.startswith(('[x]', '[X]', 'v ', 'V ')):
                items.append({
                    'type': 'task',
                    'content': clean_content.lstrip('[xXvV] '),
                    'is_completed': True,
                    'priority': 'none'
                })
            elif line.startswith(('!', '！', '踩坑', '卡點', '錯誤', 'bug', 'Bug')):
                items.append({
                    'type': 'obstacle',
                    'content': clean_content.lstrip('!！ '),
                    'is_completed': False,
                    'priority': 'high'
                })
            elif line.startswith(('★', '★', '反思', '心得', '感覺', '思考')):
                items.append({
                    'type': 'reflection',
                    'content': clean_content.lstrip('★ '),
                    'is_completed': False,
                    'priority': 'medium'
                })
            elif line.startswith(('○', 'o', 'O', '事件', '會議', '聚會')):
                items.append({
                    'type': 'event',
                    'content': clean_content.lstrip('○oO. '),
                    'is_completed': False,
                    'priority': 'none'
                })
            else:
                items.append({
                    'type': 'note',
                    'content': clean_content.lstrip('-— '),
                    'is_completed': False,
                    'priority': 'none'
                })
        return items

    @classmethod
    def _fallback_daily_reflection(cls, bullets_data: list, mood_score: int) -> dict:
        total = len(bullets_data)
        completed = len([b for b in bullets_data if b.get('is_completed')])
        return {
            "summary": f"今天共記錄了 {total} 個項目，完成了 {completed} 項待辦任務。",
            "reflection": "每天留下一點痕跡，發現自己的日子其實比想像中混亂，但看見這些混亂，就是前進的開始。明天試著做完最想做的一件小事。"
        }

    @classmethod
    def _fallback_weekly_report(cls, stats: dict) -> dict:
        total = stats.get('total_bullets', 0)
        rate = stats.get('completion_rate', 0)
        return {
            "core_learnings": f"本週累計留下了 {total} 條生活與學習痕跡，任務完成率達到 {rate}%。持續記錄本身就是最具價值的累積。",
            "recurring_obstacles": "有時在面對較大或較模糊的任務時容易產生猶豫與停滯。",
            "growth_advice": "下週建議嘗試在速記時將大任務拆解成 2~3 個可在 20 分鐘內完成的小子彈項目。"
        }
