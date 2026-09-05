import os
import json
import random
import logging
from .default_questions import DEFAULT_SOUL_QUESTIONS

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """你是一本安靜手帳背後的文字抄寫員（The Scribe）與一面溫和誠實的鏡子。
在《04_Story.md》第二章中，探索者每天記錄今天做了什麼、學了什麼、哪裡失敗了、為什麼不想做。人的日子往往比想像中混亂。
請依據使用者今天寫下的零散文字，安靜地完成三件事：
1. 今日簡記 (summary)：用 2~3 句樸素、乾淨、溫和的語言，幫他把瑣碎混亂的文字整理成一段客觀沉澱的今日紀錄，像手帳裡的正式定稿。
2. 頁緣觀察 (blindspot)：用 1~2 句話，溫和但誠實地點出他今天可能在逃避什麼，或指出他在自責中忽略的真實前進。
3. 靈魂提問 (soul_question)：提出 1 句直擊靈魂、發人深省的哲思提問，留給他在夜晚闔上筆記本時帶入沉思。

嚴格輸出合法純 JSON 格式，不要加入 Markdown 代碼塊標籤：
{
  "summary": "...",
  "blindspot": "...",
  "soul_question": "..."
}
"""


class SoulReflectionEngine:
    """
    雙軌靈魂提問與文字沉澱引擎：
    優先嘗試 Google AI (Gemini)，若未配置或異常則無縫降級至 100 句預設題庫。
    """

    @classmethod
    def generate_reflection(cls, did_today='', learned_today='', failed_today='', resistance_today='', raw_content=''):
        """
        傳入四問或自由文本，產出 { summary, blindspot, soul_question, source }
        """
        user_content_parts = []
        if did_today:
            user_content_parts.append(f"【今天做了什麼】\n{did_today}")
        if learned_today:
            user_content_parts.append(f"【今天學到了什麼】\n{learned_today}")
        if failed_today:
            user_content_parts.append(f"【哪裡失敗了】\n{failed_today}")
        if resistance_today:
            user_content_parts.append(f"【為什麼不想做 / 心情】\n{resistance_today}")
        if raw_content:
            user_content_parts.append(f"【自由速寫】\n{raw_content}")

        combined_text = "\n\n".join(user_content_parts).strip()
        if not combined_text:
            combined_text = "今天留下了空白的痕跡。"

        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            try:
                result = cls._call_gemini(api_key, combined_text)
                if result:
                    result['source'] = 'gemini'
                    return result
            except Exception as e:
                logger.warning(f"Google AI 呼叫失敗，降級至預設題庫: {e}")

        return cls._fallback_reflection(did_today, failed_today, resistance_today, combined_text)

    @classmethod
    def _call_gemini(cls, api_key, text):
        from google import genai
        client = genai.Client(api_key=api_key)

        prompt = f"{SYSTEM_PROMPT}\n\n使用者今日日記：\n{text}"
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )

        response_text = response.text.strip()
        # 清理可能夾帶的 ```json 標籤
        if response_text.startswith("```"):
            lines = response_text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            response_text = "\n".join(lines).strip()

        data = json.loads(response_text)
        return {
            'summary': data.get('summary', '').strip(),
            'blindspot': data.get('blindspot', '').strip(),
            'soul_question': data.get('soul_question', '').strip(),
        }

    @classmethod
    def _fallback_reflection(cls, did_today, failed_today, resistance_today, combined_text):
        """
        降級方案：從 100 句經典預設題庫抽取
        """
        question = random.choice(DEFAULT_SOUL_QUESTIONS)

        # 樸素的文字整理
        if did_today:
            first_line = did_today.splitlines()[0][:60]
            summary = f"今天你著手嘗試了：{first_line}。儘管過程中有許多細碎的感受，但你依然把今天的真實留在了紙上。"
        else:
            summary = "今天你花時間停了下來，誠實寫下了心裡的混亂與體會。承認狀態也是生活的一部分。"

        if failed_today or resistance_today:
            blindspot = "你在文字裡誠實地面對了自己的阻礙與不想做。看見抗拒本身，就是走出停滯的第一步。"
        else:
            blindspot = "日子往往比想像中混亂，但你今天留下的每筆墨跡，都在證明你沒有在原地停滯。"

        return {
            'summary': summary,
            'blindspot': blindspot,
            'soul_question': question,
            'source': 'default_pool'
        }
