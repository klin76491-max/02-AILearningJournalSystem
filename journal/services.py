import datetime
from django.utils import timezone
from django.db import transaction
from goals.services import GoalService
from ai_engine.services import SoulReflectionEngine
from .models import JournalEntry, SoulReflection


class EchoService:
    """
    時間的回音服務
    在寫今日日記時，偶然翻出過去寫下的痕跡。
    """
    STORY_PROLOGUE_QUOTE = {
        'type': 'story',
        'title': '第二章｜留下痕跡',
        'content': '「十四天結束後，我本來以為自己會很有成就感。結果沒有。我只是看著那十四格，然後突然發現——我已經忘了自己前幾天到底做了什麼。於是，我開始每天記一點東西……」',
        'date_str': '故事序言'
    }

    @classmethod
    def get_time_echo(cls, user, current_date=None):
        if current_date is None:
            current_date = timezone.localdate()

        # 優先級 1：14 天前 (呼應第一章 14 天挑戰)
        fourteen_days_ago = current_date - datetime.timedelta(days=14)
        entry_14 = JournalEntry.objects.filter(user=user, entry_date=fourteen_days_ago).first()
        if entry_14:
            snippet = entry_14.raw_content or entry_14.did_today or entry_14.learned_today or entry_14.failed_today
            return {
                'type': '14_days',
                'title': '14 天前的今天 (十四天挑戰的回響)',
                'content': snippet[:120] + ('...' if len(snippet) > 120 else ''),
                'date_str': fourteen_days_ago.strftime('%m月%d日'),
                'full_entry': entry_14
            }

        # 優先級 2：7 天前
        seven_days_ago = current_date - datetime.timedelta(days=7)
        entry_7 = JournalEntry.objects.filter(user=user, entry_date=seven_days_ago).first()
        if entry_7:
            snippet = entry_7.raw_content or entry_7.did_today or entry_7.learned_today or entry_7.failed_today
            return {
                'type': '7_days',
                'title': '7 天前的今天',
                'content': snippet[:120] + ('...' if len(snippet) > 120 else ''),
                'date_str': seven_days_ago.strftime('%m月%d日'),
                'full_entry': entry_7
            }

        # 優先級 3：隨機抽取過往真實掙扎或失敗的紀錄
        past_entries = JournalEntry.objects.filter(user=user, entry_date__lt=current_date).order_by('?')
        for past in past_entries:
            snippet = past.failed_today or past.resistance_today or past.learned_today or past.did_today
            if snippet:
                return {
                    'type': 'past_random',
                    'title': f'{past.entry_date.strftime("%Y年%m月%d日")} 留下的痕跡',
                    'content': snippet[:120] + ('...' if len(snippet) > 120 else ''),
                    'date_str': past.entry_date.strftime('%Y.%m.%d'),
                    'full_entry': past
                }

        # 預設回音：故事原典
        return cls.STORY_PROLOGUE_QUOTE


class JournalService:
    @classmethod
    @transaction.atomic
    def save_trace(cls, user, entry_date=None, did_today='', learned_today='', failed_today='', resistance_today='', raw_content='', weather='sunny', mood='chaos'):
        if entry_date is None:
            entry_date = timezone.localdate()

        active_goal = GoalService.get_active_goal(user)

        entry, created = JournalEntry.objects.update_or_create(
            user=user,
            entry_date=entry_date,
            defaults={
                'goal': active_goal,
                'did_today': did_today.strip(),
                'learned_today': learned_today.strip(),
                'failed_today': failed_today.strip(),
                'resistance_today': resistance_today.strip(),
                'raw_content': raw_content.strip(),
                'weather': weather or 'sunny',
                'mood': mood or 'chaos',
            }
        )

        # 觸發文字沉澱與靈魂提問引擎
        reflection_data = SoulReflectionEngine.generate_reflection(
            did_today=entry.did_today,
            learned_today=entry.learned_today,
            failed_today=entry.failed_today,
            resistance_today=entry.resistance_today,
            raw_content=entry.raw_content
        )

        reflection, _ = SoulReflection.objects.update_or_create(
            entry=entry,
            defaults={
                'summary': reflection_data.get('summary', ''),
                'blindspot': reflection_data.get('blindspot', ''),
                'soul_question': reflection_data.get('soul_question', ''),
                'source': reflection_data.get('source', 'default_pool'),
            }
        )

        return entry, reflection
