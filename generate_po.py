# -*- coding: utf-8 -*-
import os, sys

TRANSLATIONS = {
    # Brand / Navigation / Common
    "留下痕跡｜手帳學習日誌": ("留下痕跡｜手帳學習日誌", "The Trace Log | Learning Journal"),
    "留下痕跡｜翻開手帳": ("留下痕跡｜翻開手帳", "The Trace Log | Open Notebook"),
    "留下痕跡｜時間河流": ("留下痕跡｜時間河流", "The Trace Log | River of Time"),
    "翻開第一頁｜設定前進方向": ("翻開第一頁｜設定前進方向", "First Page | Set Focus Direction"),
    "留下痕跡": ("留下痕跡", "The Trace Log"),
    "手帳學習日誌": ("手帳學習日誌", "Learning Journal"),
    "時間河流": ("時間河流", "River of Time"),
    "痕跡長河": ("痕跡長河", "River of Traces"),
    "River of Traces": ("痕跡長河", "River of Traces"),
    "漫步翻看時間河流裡的每日痕跡": ("漫步翻看時間河流裡的每日痕跡", "Wander through daily traces in the river of time"),
    "手帳音效：翻頁、書寫、蓋印": ("手帳音效：翻頁、書寫、蓋印", "Handbook Sound: Page flip, writing, stamping"),
    "音效": ("音效", "Sound"),
    "方向：": ("方向：", "Focus: "),
    "更換前進方向": ("更換前進方向", "Change focus direction"),
    "點擊鉛筆隨時更換前進方向": ("點擊鉛筆隨時更換前進方向", "Click pencil to change focus direction anytime"),
    "當前專注方向，點擊鉛筆可更換": ("當前專注方向，點擊鉛筆可更換", "Current focus direction, click pencil to change"),
    "闔上手帳": ("闔上手帳", "Close Notebook"),
    "登入": ("登入", "Log in"),
    "語言": ("語言", "Language"),
    "繁體中文": ("繁體中文", "繁體中文"),
    "English": ("English", "English"),
    "換個前進的方向": ("換個前進的方向", "Change Your Focus Direction"),
    "「走著走著如果發現走偏了，或者原來的挑戰已經結束，這很正常。換個新方向，之前的每頁痕跡依然會留在時間河流裡。」": (
        "「走著走著如果發現走偏了，或者原來的挑戰已經結束，這很正常。換個新方向，之前的每頁痕跡依然會留在時間河流裡。」",
        "\"If you find yourself drifting off course, or if your previous challenge is complete, that is completely normal. Setting a new direction won't erase the traces you've left in the river of time.\""
    ),
    "這段時間，你想試著專注的一件事是……": ("這段時間，你想試著專注的一件事是……", "During this period, one thing you want to focus on is..."),
    "例如：每天讀一篇短篇、或是每天給自己二十分鐘寫作": ("例如：每天讀一篇短篇、或是每天給自己二十分鐘寫作", "e.g., Read a short essay daily, or write for 20 minutes every day"),
    "為什麼想換這個方向？ (初心，選填)": ("為什麼想換這個方向？ (初心，選填)", "Why choose this direction? (Original intent, optional)"),
    "寫給未來的自己一兩句心裡話": ("寫給未來的自己一兩句心裡話", "A word or two to your future self"),
    "暫時不換": ("暫時不換", "Keep Current"),
    "確定定下新方向": ("確定定下新方向", "Confirm New Focus"),
    "「每天留下一點痕跡。不是為了變得更厲害，只是想知道如果一直記下去，我會變成什麼樣子。」": (
        "「每天留下一點痕跡。不是為了變得更厲害，只是想知道如果一直記下去，我會變成什麼樣子。」",
        "\"Leave a little trace every day. Not to become someone extraordinary, but simply to see who I will become if I keep recording.\""
    ),
    "《04_Story.md》第二章 • A Little Wonder 手作手帳": ("《04_Story.md》第二章 • A Little Wonder 手作手帳", "Chapter 02 • A Little Wonder Handcrafted Notebook"),
    "《04_Story.md》第二章 • A Little Wonder Handcrafted Notebook": ("《04_Story.md》第二章 • A Little Wonder 手作手帳", "Chapter 02 • A Little Wonder Handcrafted Notebook"),

    # Setup Page
    "第一頁 • 定錨前進方向": ("第一頁 • 定錨前進方向", "First Page • Anchor Goal"),
    "First Page • Anchor Goal": ("第一頁 • 定錨前進方向", "First Page • Anchor Goal"),
    "這段日子，你想走向哪裡？": ("這段日子，你想走向哪裡？", "Where do you want to head in the days ahead?"),
    "不用是多麼偉大的誓言。可能只是：十四天完成一個微小工具、每天寫三行程式、或是每天留二十分鐘安靜坐著。": (
        "不用是多麼偉大的誓言。可能只是：十四天完成一個微小工具、每天寫三行程式、或是每天留二十分鐘安靜坐著。",
        "It doesn't have to be a grand vow. Maybe just: completing a tiny tool in 14 days, writing 3 lines of code daily, or sitting quietly for 20 minutes."
    ),
    "走著走著如果迷路或完成了，你隨時可以在頁首換個新方向。": ("走著走著如果迷路或完成了，你隨時可以在頁首換個新方向。", "If you lose your way or complete your quest, you can change direction anytime at the top of the page."),
    "🎯 這段時間，我想試著專注的一件事是……": ("🎯 這段時間，我想試著專注的一件事是……", "🎯 During this time, one thing I want to try focusing on is..."),
    "例如：連續十四天，每天給自己留一點時間寫程式": ("例如：連續十四天，每天給自己留一點時間寫程式", "e.g., For 14 days straight, set aside time each day to code"),
    "簡短一句話即可，這將是這段日記的篇章標題。": ("簡短一句話即可，這將是這段日記的篇章標題。", "A short sentence is enough; this will be the chapter title of this journal."),
    "💡 為什麼想做這件事？ (初心與期待，選填)": ("💡 為什麼想做這件事？ (初心與期待，選填)", "💡 Why do you want to do this? (Original intent & hope, optional)"),
    "例如：想知道想和做之間的距離，到底能不能被拉近一些。": ("例如：想知道想和做之間的距離，到底能不能被拉近一些。", "e.g., Want to see if the distance between thought and action can truly be closed."),
    "寫給未來某一天的自己看。": ("寫給未來某一天的自己看。", "Written for a future day's self to read."),
    "開始翻開日記，留下痕跡 ➔": ("開始翻開日記，留下痕跡 ➔", "Begin Journal, Leave Traces ➔"),

    # Canvas (Journal Writing Area)
    "開啟/退出純淨手帳專注模式 (Esc)": ("開啟/退出純淨手帳專注模式 (Esc)", "Toggle Zen Focus Mode (Esc)"),
    "專注模式": ("專注模式", "Zen Mode"),
    "退出專注 (Esc)": ("退出專注 (Esc)", "Exit Zen (Esc)"),
    "切換為無拘無束的自由手帳模式": ("切換為無拘無束的自由手帳模式", "Switch to freehand sketch mode"),
    "切換為自由速寫": ("切換為自由速寫", "Switch to Freehand"),
    "切換為故事四問": ("切換為故事四問", "Switch to Four Questions"),
    "痕跡已蓋印留存": ("痕跡已蓋印留存", "TRACE SEALED • Preserved"),
    "今天的痕跡": ("今天的痕跡", "Today's Traces"),
    "墨跡已沉澱歸檔": ("墨跡已沉澱歸檔", "Ink settled & archived"),
    "墨水已備好，隨寫即存": ("墨水已備好，隨寫即存", "Ink ready, auto-saving as you write"),
    "今日天候：晴朗日光": ("今日天候：晴朗日光", "Weather: Bright Daylight"),
    "今日天候：濛濛細雨": ("今日天候：濛濛細雨", "Weather: Gentle Rain"),
    "今日天候：寂靜深夜": ("今日天候：寂靜深夜", "Weather: Quiet Midnight"),
    "晴": ("晴", "Sunny"),
    "雨": ("雨", "Rainy"),
    "夜": ("夜", "Night"),
    "心情：捕捉到靈光或小成就": ("心情：捕捉到靈光或小成就", "Mood: Spark or small achievement"),
    "心情：思緒繁雜混亂": ("心情：思緒繁雜混亂", "Mood: Tangled & chaotic thoughts"),
    "心情：有微小萌芽與新起點": ("心情：有微小萌芽與新起點", "Mood: Tiny sprout & fresh start"),
    "微光": ("微光", "Sparks"),
    "混亂": ("混亂", "Chaos"),
    "萌芽": ("萌芽", "Sprout"),
    "1. 今天做了什麼？": ("1. 今天做了什麼？", "1. What did you do today?"),
    "(行動的痕跡，哪怕再微小)": ("(行動的痕跡，哪怕再微小)", "(Traces of action, no matter how small)"),
    "擲骰子換個靈感提示": ("擲骰子換個靈感提示", "Roll dice for an inspiration prompt"),
    "換個提示": ("換個提示", "New Prompt"),
    "• 寫了幾行程式、讀了一篇文章、嘗試解決了一個難題...": ("• 寫了幾行程式、讀了一篇文章、嘗試解決了一個難題...", "• Wrote a few lines of code, read an essay, tried solving a puzzle..."),
    "2. 今天學到了什麼？": ("2. 今天學到了什麼？", "2. What did you learn today?"),
    "(認知、技巧或微小頓悟)": ("(認知、技巧或微小頓悟)", "(Insights, skills, or quiet realizations)"),
    "• 發現了某個新方法、或是明白為什麼過去會卡住...": ("• 發現了某個新方法、或是明白為什麼過去會卡住...", "• Discovered a new method, or understood why you got stuck before..."),
    "3. 哪裡失敗了？": ("3. 哪裡失敗了？", "3. Where did you fail?"),
    "(誠實面對挫折、失控與阻礙)": ("(誠實面對挫折、失控與阻礙)", "(Honestly facing setbacks, chaos, and roadblocks)"),
    "• 原本想做完卻沒搞定、因為煩躁放棄了某件事...": ("• 原本想做完卻沒搞定、因為煩躁放棄了某件事...", "• Planned to finish but didn't, gave up on something out of annoyance..."),
    "4. 為什麼不想做？ / 當下心情": ("4. 為什麼不想做？ / 當下心情", "4. Why didn't you want to do it? / Current Mood"),
    "(誠實傾聽內心的抗拒)": ("(誠實傾聽內心的抗拒)", "(Honestly listening to inner resistance)"),
    "• 覺得疲憊、害怕面對不確定性、心浮氣躁...": ("• 覺得疲憊、害怕面對不確定性、心浮氣躁...", "• Feeling exhausted, fearing uncertainty, feeling restless..."),
    "今日自由手帳隨筆": ("今日自由手帳隨筆", "Freehand Journal Notes Today"),
    "(不拘形式，寫下腦海裡的混亂與文字)": ("(不拘形式，寫下腦海裡的混亂與文字)", "(No rules—pour out raw thoughts, clutter, and words)"),
    "在這裡隨意寫下今天的混亂、牢騷、嘗試或微小頓悟...": ("在這裡隨意寫下今天的混亂、牢騷、嘗試或微小頓悟...", "Write freely about today's clutter, complaints, attempts, or quiet epiphanies..."),
    "即時字數統計與墨水量": ("即時字數統計與墨水量", "Real-time word count & ink level"),
    "字": ("字", "words"),
    "• 誠實寫下即可": ("• 誠實寫下即可", "• Just write honestly"),
    "留下一頁痕跡": ("留下一頁痕跡", "Leave a Page of Traces"),
    "心靈": ("心靈", "SOUL"),
    "郵籤": ("郵籤", "POST"),
    "今日簡記 • 混亂的沉澱": ("今日簡記 • 混亂的沉澱", "Today's Reflection • Settling the Chaos"),
    "今日簡記": ("今日簡記", "Today's Reflection"),
    "頁緣觀察": ("頁緣觀察", "Margin Observation"),
    "靈魂提問": ("靈魂提問", "Soul Question"),
    "靈魂提問：": ("靈魂提問：", "Soul Question: "),
    "🕊️ 靈魂提問：": ("🕊️ 靈魂提問：", "🕊️ Soul Question: "),
    "[今晚隨筆] 在這裡寫下今晚的一點體會（或直接闔上手帳，留給自己一夜沉澱）...": (
        "[今晚隨筆] 在這裡寫下今晚的一點體會（或直接闔上手帳，留給自己一夜沉澱）...",
        "[Tonight's Note] Jot down an impression tonight (or close notebook and let it rest overnight)..."
    ),
    "留下今晚筆記": ("留下今晚筆記", "Seal Tonight's Note"),
    "今晚手寫筆記：": ("今晚手寫筆記：", "Tonight's Note: "),
    "💬 今晚手寫筆記：": ("💬 今晚手寫筆記：", "💬 Tonight's Note: "),
    "時間的回音": ("時間的回音", "Echo of Time"),
    "回望時光": ("回望時光", "Looking Back"),
    "第二章｜留下痕跡": ("第二章｜留下痕跡", "Chapter 02 | The Trace Log"),
    "「回頭看才發現，有些事情我以為自己做了很多，其實根本沒有。有些事情我以為自己一直在失敗，卻已經比以前走遠了一點。」": (
        "「回頭看才發現，有些事情我以為自己做了很多，其實根本沒有。有些事情我以為自己一直在失敗，卻已經比以前走遠了一點。」",
        "\"Looking back, I realize that some things I thought I did a lot of, I actually didn't; and some things where I thought I was constantly failing, I had quietly moved forward.\""
    ),
    "手帳心法：": ("手帳心法：", "Handbook Principle: "),
    "不用強求每天都有豐功偉業。真實寫下抗拒與卡頓，本身就是最深邃的成長痕跡。": (
        "不用強求每天都有豐功偉業。真實寫下抗拒與卡頓，本身就是最深邃的成長痕跡。",
        "No need to force heroic deeds every day. Honestly writing down resistance and bottlenecks is itself the deepest trace of growth."
    ),
    "翻閱時間河流中的過往篇章": ("翻閱時間河流中的過往篇章", "Browse past pages in the River of Time"),

    # Spark tips in canvas JS
    "• 哪怕只是寫了兩行程式、讀了半篇文章，甚至是整理了書桌": (
        "• 哪怕只是寫了兩行程式、讀了半篇文章，甚至是整理了書桌",
        "• Even if it was just writing two lines of code, reading half an article, or tidying the desk"
    ),
    "• 哪怕只是鼓起勇氣打開了那個逃避好幾天的檔案": (
        "• 哪怕只是鼓起勇氣打開了那個逃避好幾天的檔案",
        "• Even if it was just gathering courage to open that file avoided for days"
    ),
    "• 哪怕只是坐在椅子上安靜思考了十分鐘接下來要先做什麼": (
        "• 哪怕只是坐在椅子上安靜思考了十分鐘接下來要先做什麼",
        "• Even if it was just sitting quietly for ten minutes pondering what to do next"
    ),
    "• 發現了某個新工具或快捷鍵、或想通了為什麼之前會卡住": (
        "• 發現了某個新工具或快捷鍵、或想通了為什麼之前會卡住",
        "• Found a new tool or shortcut, or figured out why you were stuck before"
    ),
    "• 學到了：自己什麼時候精神最集中，什麼時候需要放空充電": (
        "• 學到了：自己什麼時候精神最集中，什麼時候需要放空充電",
        "• Learned: when your focus peaks, and when you need quiet recharging"
    ),
    "• 明白了一件事：慢慢做反而比焦急趕工走得更穩": (
        "• 明白了一件事：慢慢做反而比焦急趕工走得更穩",
        "• Realized: pacing steadily takes you further than rushing in panic"
    ),
    "• 原本打算做完卻中途滑了半小時手機，誠實寫下": (
        "• 原本打算做完卻中途滑了半小時手機，誠實寫下",
        "• Intended to finish but scrolled phone for half an hour—write it honestly"
    ),
    "• 試了半天還是報錯，最後感到沮喪關掉了視窗": (
        "• 試了半天還是報錯，最後感到沮喪關掉了視窗",
        "• Tried repeatedly yet got errors, closed the window in frustration"
    ),
    "• 承認自己今天真的沒在狀態，不用給自己道德審判": (
        "• 承認自己今天真的沒在狀態，不用給自己道德審判",
        "• Acknowledge that today wasn't your day—no moral judgment needed"
    ),
    "• 其實是害怕做出來不夠完美，所以遲遲不敢開始": (
        "• 其實是害怕做出來不夠完美，所以遲遲不敢開始",
        "• Really just afraid of imperfection, hence hesitating to begin"
    ),
    "• 只是純粹太疲憊了，大腦像浸了水一樣轉不動": (
        "• 只是純粹太疲憊了，大腦像浸了水一樣轉不動",
        "• Simply drained—brain feels soaked and barely turning"
    ),
    "• 心裡在嘀咕這件事到底有沒有意義，感到盲目": (
        "• 心裡在嘀咕這件事到底有沒有意義，感到盲目",
        "• Questioning whether this has any meaning, feeling a bit lost"
    ),

    # Canvas JS notifications
    "已從本機還原未存草稿": ("已從本機還原未存草稿", "Restored unsaved draft from local storage"),
    "墨水書寫中...": ("墨水書寫中...", "Ink flowing..."),
    "墨跡已自動隱入紙張": ("墨跡已自動隱入紙張", "Ink automatically blended into paper"),
    "【做了什麼】": ("【做了什麼】", "[What I Did]"),
    "【學到了什麼】": ("【學到了什麼】", "[What I Learned]"),
    "【哪裡失敗了】": ("【哪裡失敗了】", "[Where I Failed]"),
    "【失敗與卡住】": ("【失敗與卡住】", "[Failures & Roadblocks]"),
    "【抗拒與心情】": ("【抗拒與心情】", "[Resistance & Mood]"),
    "【手帳隨筆】": ("【手帳隨筆】", "[Journal Notes]"),
    "請至少留下一句今天的微小痕跡。": ("請至少留下一句今天的微小痕跡。", "Please write down at least one tiny trace of today."),
    "墨水風乾中...": ("墨水風乾中...", "Ink drying..."),
    "今日痕跡已歸檔": ("今日痕跡已歸檔", "Today's traces archived"),
    "儲存失敗，請重試": ("儲存失敗，請重試", "Save failed, please try again"),
    "連線失敗，請檢查網路連線": ("連線失敗，請檢查網路連線", "Connection failed, please check network"),
    "今晚手寫筆記已烙印留存。": ("今晚手寫筆記已烙印留存。", "Tonight's handwritten note sealed."),
    "保存失敗：": ("保存失敗：", "Save failed: "),
    "請填寫新的方向名稱": ("請填寫新的方向名稱", "Please enter a name for the new direction"),
    "設定失敗": ("設定失敗", "Setup failed"),
    "連線失敗，請稍後重試": ("連線失敗，請稍後重試", "Connection failed, please try again later"),

    # River Page
    "蓋印於": ("蓋印於", "Sealed at"),
    "上一頁": ("上一頁", "Previous"),
    "下一頁": ("下一頁", "Next"),
    "第": ("第", "Page"),
    "頁 / 共": ("頁 / 共", "of"),
    "時間河流裡還沒有任何痕跡。": ("時間河流裡還沒有任何痕跡。", "There are no traces in the River of Time yet."),
    "「萬事起頭難，只要記下今天的一兩句，這條河就會開始流動。」": (
        "「萬事起頭難，只要記下今天的一兩句，這條河就會開始流動。」",
        "\"All beginnings are hard. Just write down a line or two today, and this river will start flowing.\""
    ),
    "翻開手帳，留下第一筆痕跡": ("翻開手帳，留下第一筆痕跡", "Open notebook & leave your first trace"),
    "重溫隨機一頁": ("重溫隨機一頁", "Relive a Random Page"),
    "返回今日書寫": ("返回今日書寫", "Back to Today's Journal"),
    "章節過濾:": ("章節過濾:", "Filter by Chapter:"),
    "全部痕跡": ("全部痕跡", "All Traces"),
    "當前": ("當前", "Current"),
    "隨機翻開一則過往的記憶痕跡": ("隨機翻開一則過往的記憶痕跡", "Flip to a random memory trace from the past"),

    # Login Page
    "Chapter 02 • The Trace Log": ("第二章 • 留下痕跡", "Chapter 02 • The Trace Log"),
    "第二章 • 留下痕跡": ("第二章 • 留下痕跡", "Chapter 02 • The Trace Log"),
    "留 下 痕 跡": ("留 下 痕 跡", "The Trace Log"),
    "不為變得更厲害，只為看清走過的路": ("不為變得更厲害，只為看清走過的路", "Not to become extraordinary, just to see clearly the path walked"),
    "「十四天結束後，我本來以為自己會很有成就感。結果沒有。": (
        "「十四天結束後，我本來以為自己會很有成就感。結果沒有。",
        "\"After the 14 days ended, I thought I would feel a great sense of accomplishment. But I didn't."
    ),
    "我只是看著那十四格，然後突然發現——我已經忘了自己前幾天到底做了什麼。": (
        "我只是看著那十四格，然後突然發現——我已經忘了自己前幾天到底做了什麼。",
        "I was just looking at those 14 boxes, and suddenly realized—I had already forgotten what I did in the earlier days."
    ),
    "於是，我開始每天記一點東西。今天做了什麼。學了什麼。哪裡失敗了。有時候，連今天為什麼不想做，都記下來。」": (
        "於是，我開始每天記一點東西。今天做了什麼。學了什麼。哪裡失敗了。有時候，連今天為什麼不想做，都記下來。」",
        "So I began to write down a little something every day. What I did. What I learned. Where I failed. Sometimes, even why I didn't feel like doing anything today.\""
    ),
    "使用 Google 帳號翻開手帳": ("使用 Google 帳號翻開手帳", "Open Notebook with Google Account"),
    "[開發測試] 一鍵以探索者帳號翻開手帳": ("[開發測試] 一鍵以探索者帳號翻開手帳", "[Dev Test] Open Notebook with Explorer Account"),
    "純粹紙筆觸感 • 本地私密保存 • 無科技喧囂": ("純粹紙筆觸感 • 本地私密保存 • 無科技喧囂", "Pure tactile paper feel • Private & local • Free of tech noise"),
}

ZH_PO_PATH = r"c:\Users\zxzxzxzx6666\Downloads\FWM_English\IT\App\02-AILearningJournalSystem\locale\zh_Hant\LC_MESSAGES\django.po"
EN_PO_PATH = r"c:\Users\zxzxzxzx6666\Downloads\FWM_English\IT\App\02-AILearningJournalSystem\locale\en\LC_MESSAGES\django.po"

zh_header = """# Traditional Chinese translations for AI Learning Journal System.
msgid ""
msgstr ""
"Project-Id-Version: AI Learning Journal System 1.0\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2026-09-06 07:00+0800\\n"
"PO-Revision-Date: 2026-09-06 07:00+0800\\n"
"Last-Translator: Antigravity\\n"
"Language-Team: Traditional Chinese\\n"
"Language: zh_Hant\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=1; plural=0;\\n"

"""

en_header = """# English translations for AI Learning Journal System.
msgid ""
msgstr ""
"Project-Id-Version: AI Learning Journal System 1.0\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2026-09-06 07:00+0800\\n"
"PO-Revision-Date: 2026-09-06 07:00+0800\\n"
"Last-Translator: Antigravity\\n"
"Language-Team: English\\n"
"Language: en\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\\n"

"""

def escape_po(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n"\n"')

def write_po(filepath, header, lang_index):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header)
        for msgid, pair in TRANSLATIONS.items():
            msgstr = pair[lang_index]
            f.write(f'msgid "{escape_po(msgid)}"\n')
            f.write(f'msgstr "{escape_po(msgstr)}"\n\n')

write_po(ZH_PO_PATH, zh_header, 0)
write_po(EN_PO_PATH, en_header, 1)

print("Generated po files successfully!")
