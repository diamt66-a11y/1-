# -*- coding: cp949 -*-
import os
import json
import requests
import google.generativeai as genai
import time

# ==========================================================================
# 1씤 湲곗뾽 뿉씠쟾듃 떆뒪뀥 솚寃 꽕젙 (蹂댁븞긽 .env 뙆씪濡쒕꽣 濡쒕뱶)
# ==========================================================================
GEMINI_API_KEY = ""
WP_URL = ""
WP_USER = ""
WP_APPLICATION_PASSWORD = ""

# .env 뙆씪 뙆떛 泥섎━
if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                # 뵲샂몴 젣嫄
                val = val.strip().strip('"').strip("'")
                key = key.strip()
                if key == "GEMINI_API_KEY":
                    GEMINI_API_KEY = val
                elif key == "WP_URL":
                    WP_URL = val
                elif key == "WP_USER":
                    WP_USER = val
                elif key == "WP_APPLICATION_PASSWORD":
                    WP_APPLICATION_PASSWORD = val

# OS 솚寃쎈닔 諛깆뾽 泥섎━ (Vercel 諛고룷 떆 꽌踰 솚寃쎈닔 쓳슜)
GEMINI_API_KEY = GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
WP_URL = WP_URL or os.environ.get("WP_URL", "")
WP_USER = WP_USER or os.environ.get("WP_USER", "")
WP_APPLICATION_PASSWORD = WP_APPLICATION_PASSWORD or os.environ.get("WP_APPLICATION_PASSWORD", "")
# ==========================================================================

# Gemini API 珥덇린솕 븿닔
def init_gemini():
    if not GEMINI_API_KEY:
        raise ValueError("[ERROR] GEMINI_API_KEY媛 꽕젙릺吏 븡븯뒿땲떎. .env 뙆씪씠굹 솚寃 蹂닔瑜 솗씤빐二쇱꽭슂.")
    genai.configure(api_key=GEMINI_API_KEY)

# 429 뿉윭 쓳슜 븞쟾븳 API 샇異 뿬띁 븿닔 (옄룞 옱떆룄)
def safe_generate(model_name, prompt, max_retries=5, delay_secs=45):
    model = genai.GenerativeModel(model_name)
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response
        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "quota" in err_msg.lower() or "limit" in err_msg.lower():
                if attempt < max_retries - 1:
                    print(f"\n[SYSTEM WARNING] API 븳룄(429) 룄떖. {delay_secs}珥 湲 썑 옱떆룄빀땲떎... (떆룄 {attempt+1}/{max_retries})")
                    time.sleep(delay_secs)
                    delay_secs += 15
                    continue
            raise e

# ==========================================================================
# 뿉씠쟾듃 1: 湲고쉷 뿉씠쟾듃 (Planner Agent) - 궗슜옄 8遺옉 紐⑹감 셿踰 怨좎젙
# ==========================================================================
def run_planner(topic, series_count=8):
    print(f"\n[Planner] 솗젙맂 {series_count}遺옉 釉붾줈洹 떆由ъ쫰 湲고쉷븞 濡쒕뱶 以 (紐⑹감 媛뺤젣 怨좎젙)...")
    
    # 꽕씠踰 釉붾줈洹몄뿉 湲곕컻뻾빐 몢떊 8遺옉 紐⑹감 100% 룞씪븯寃 꽕젙
    fixed_plan = {
        "series_title": "1씤 湲곗뾽쓽 깮궛꽦쓣 洹밸솕븯뒗 IT 옄룞솕 鍮꾧껐",
        "posts": [
            {
                "part_number": 1,
                "title": "젣1렪: 1씤 湲곗뾽 IT 옄룞솕: 吏湲덉씠 湲고쉶! 깮궛꽦 10諛 떖꽦쓽 泥リ구쓬",
                "sections": [
                    {"sub_title": "1씤 李쎌뾽怨 옄룞솕쓽 븘뿰꽦", "key_points": ["깮궛꽦 10諛", "떒닚 諛섎났 뾽臾 젣嫄", "肄붿뼱 엫 솗蹂"]},
                    {"sub_title": "옄룞솕 닔떇 떎利앹쟻 洹쇨굅", "key_points": ["二 40떆媛 以 36떆媛 옄룞솕", "ROI 遺꾩꽍 媛쒖슂", "3~5뀈 옣湲 濡쒕뱶留 媛쒖슂"]}
                ]
            },
            {
                "part_number": 2,
                "title": "젣2렪: 1씤 湲곗뾽 꽦怨 쟾왂: 옄룞솕 湲고쉶 諛쒓뎬怨 ROI 遺꾩꽍 봽젅엫썙겕",
                "sections": [
                    {"sub_title": "궡 鍮꾩쫰땲뒪뿉꽌 옄룞솕 寃 꽑蹂꾪븯湲", "key_points": ["끂肄붾뱶 濡쒖슦肄붾뱶 벑湲 遺꾨쪟", "궡媛 諛붾줈 븷 닔 엳뒗 寃 援щ텇"]},
                    {"sub_title": "삁긽 鍮꾩슜 諛 떆媛 솚궛 닔떇", "key_points": ["ROI 遺꾩꽍 봽젅엫썙겕", "떆媛 솚궛", "옄룞솕 궃씠룄 議곗젅"]}
                ]
            },
            {
                "part_number": 3,
                "title": "젣3렪: 1씤 李쎌뾽媛瑜 쐞븳 뒪留덊듃 삤뵾뒪 옄룞솕: 냼넻怨 삊뾽 슚쑉 넂뿬 깮궛꽦 洹밸솕",
                "sections": [
                    {"sub_title": "삊뾽 룄援 옄룞 뿰怨꾩쓽 湲곗큹", "key_points": ["끂뀡 DB 뿰룞", "뒳옓 븣由 꽕젙", "援ш 떆듃 뿰빀"]},
                    {"sub_title": "룄援щ퀎 삁궛 媛씠뱶", "key_points": ["Zapier Make 臾대즺 븳룄", "Airtable Glide 臾대즺 뵆옖", "삁긽 썡 궗슜猷"]}
                ]
            },
            {
                "part_number": 4,
                "title": "젣4렪: 1씤 湲곗뾽 留덉똿/쁺뾽 옄룞솕: 怨좉컼 쑀엯遺꽣 留ㅼ텧源뚯, 끂肄붾뱶 떎쟾 쟾왂",
                "sections": [
                    {"sub_title": "怨좉컼 由щ뱶 닔吏 諛 띁꼸 옄룞솕", "key_points": ["옖뵫럹씠吏 怨좉컼 닔吏", "씠硫붿씪 留덉똿 옄룞솕", "끂肄붾뱶 댋 뿰룞"]},
                    {"sub_title": "씠빐異⑸룎 諛곗젣 怨듭씤 異쒖쿂 由ъ뒪듃", "key_points": ["以묒냼踰ㅼ쿂湲곗뾽遺 옄猷", "븳援뜲씠꽣궛뾽吏꾪씎썝 蹂닿퀬꽌"]}
                ]
            },
            {
                "part_number": 5,
                "title": "젣5렪: 1씤 李쎌뾽媛瑜 쐞븳 AI 肄섑뀗痢 깮궛꽦 쁺紐: 湲고쉷遺꽣 諛쒗뻾源뚯",
                "sections": [
                    {"sub_title": "AI瑜 솢슜븳 肄섑뀗痢 臾댄븳 깮꽦 썙겕뵆濡쒖슦", "key_points": ["Gemini API 솢슜 湲고쉷", "珥덇퀬 옄룞 옉꽦 뀥뵆由", "釉붾줈洹 뾽濡쒕뱶 뿰룞"]},
                    {"sub_title": "肄섑뀗痢 깮궛꽦 룄援 벑湲", "key_points": ["끂肄붾뱶 湲곕컲 뀥뵆由", "썡 삁긽 援щ룆猷"]}
                ]
            },
            {
                "part_number": 6,
                "title": "젣6렪: 1씤 湲곗뾽 옱臾/꽭臾 옄룞솕: 룉 愿由щ꽣 꽭湲 떊怨좉퉴吏 끂肄붾뱶/濡쒖슦肄붾뱶 넄猷⑥뀡 솢슜 媛씠뱶",
                "sections": [
                    {"sub_title": "援궡 꽭臾 諛 슫쁺 옄룞솕 濡쒖뺄 뿰룞", "key_points": ["솃깮뒪 쟾옄꽭湲덇퀎궛꽌 뿰룞", "罹먯떆끂듃 뿰怨 諛⑸쾿", "뜑議 궪姨쒖궪 떎臾"]}
                ]
            },
            {
                "part_number": 7,
                "title": "젣7렪: AI 鍮꾩꽌泥섎읆! 媛쒕컻 吏떇 뾾씠 濡쒖슦肄붾뱶/끂肄붾뱶 옄룞솕 留덉뒪꽣븯湲",
                "sections": [
                    {"sub_title": "媛쒕컻 吏떇 뾾씠 AI 鍮꾩꽌 遺젮 肄붾뵫븯湲", "key_points": ["AI 梨쀫큸 봽濡ы봽듃 肄붾뵫 諛⑸쾿", "10珥덈쭔뿉 肄붾뱶 吏쒓린"]},
                    {"sub_title": "쎒 뒪겕옒븨 踰뺤쟻 二쇱쓽젏", "key_points": ["젙蹂댄넻떊留앸쾿 젣48議 以닔", "옉沅뚮쾿 臾대떒 닔吏 寃쎄퀬", "robots.txt 몴以"]}
                ]
            },
            {
                "part_number": 8,
                "title": "젣8렪: 1씤 湲곗뾽 옄룞솕 떆뒪뀥 셿寃고뙋: 吏냽 媛뒫븳 꽦옣쓣 쐞븳 沅곴레 쟾왂",
                "sections": [
                    {"sub_title": "3~5뀈 옣湲 濡쒕뱶留듭쓽 셿꽦", "key_points": ["옄룞솕 븘궎뀓泥 떎씠뼱洹몃옩", "吏냽 媛뒫븳 鍮꾩쫰땲뒪 꽦옣 쟾왂"]}
                ]
            }
        ]
    }
    
    if series_count < 8:
        fixed_plan["posts"] = fixed_plan["posts"][:series_count]
        
    print("-> [Planner] 궗슜옄 솗젙 8遺옉 紐⑹감 룞湲고솕 꽦怨!")
    return fixed_plan

# ==========================================================================
# 뿉씠쟾듃 2: 吏묓븘 뿉씠쟾듃 (Writer Agent)
# ==========================================================================
def run_writer(post_plan, part_number=1, total_parts=8):
    title = post_plan['title']
    sections = post_plan['sections']
    
    print(f"\n[Writer] {title} ({part_number}/{total_parts}) 蹂몃Ц 吏묓븘 떆옉...")
    
    sections_str = ""
    for idx, sec in enumerate(sections):
        sub_title = sec.get('sub_title') or sec.get('title') or f"꽮뀡 {idx+1}"
        key_points = sec.get('key_points') or sec.get('keywords') or []
        sections_str += f"\n{idx+1}. 냼젣紐: {sub_title}\n   - 떎猷 궎썙뱶: {', '.join(key_points)}\n"
        
    prompt = f"""
    떦떊 쟾臾 湲곗닠/鍮꾩쫰땲뒪 釉붾줈洹 吏묓븘媛엯땲떎.
    湲고쉷 뿉씠쟾듃媛 깮꽦븳 븘옒 냼젣紐⑷낵 궎썙뱶瑜 諛뷀깢쑝濡 源딆씠 엳뒗 釉붾줈洹 蹂몃Ц쓣 옉꽦븯꽭슂.
    
    湲 젣紐: "{title}"
    湲 紐⑹감 젙蹂: {sections_str}
    뿰옱 쁽솴: 珥 {total_parts}遺옉 以 젣 {part_number}렪 湲엯땲떎.
    
    洹쒖튃:
    1. 湲 쟾泥 遺꾨웾 理쒖냼 怨듬갚 젣쇅 1,500옄 씠긽쑝濡 湲멸퀬 븣李④쾶 옉꽦븯꽭슂.
    2. 媛 냼젣紐⑹ 諛섎뱶떆 HTML쓽 <h2> 깭洹몃줈 媛먯떥怨, 蹂몃Ц 臾몃떒 <p> 깭洹몃 씠슜빐 떒씫쓣 援щ텇븯꽭슂.
    3. 臾몄껜뒗 젙以묓븯怨 떊猶곌컧쓣 二쇰뒗 議대뙎留(~빀땲떎. ~엯땲떎)濡 넻씪븯꽭슂.
    4. **(씠쟾 湲 뿰怨 諛 룆옄 닔以 젙쓽)**: 
       - 젣1렪 꽌몢뿉 "蹂 떆由ъ쫰뒗 肄붾뵫 寃쏀뿕씠 쟾 뾾뒗 珥덈낫 1씤 李쎌뾽媛瑜 寃잛쑝濡 빀땲떎. 7렪 벑뿉꽌 떎猷⑤뒗 Python씠굹 뒪겕옒븨, RPA 벑쓽 湲곗닠 슂냼뒗 룆옄媛 媛쒕컻쓣 留덉뒪꽣븯뒗 寃껋씠 븘땲씪 AI(Gemini, ChatGPT)瑜 鍮꾩꽌泥섎읆 遺젮 寃곌낵臾쇱쓣 뼸뼱궡뒗 湲고쉷옄쟻 愿젏쓣 紐⑺몴濡 빀땲떎."瑜 紐낆떆븯꽭슂.
       - 젣2렪 씠긽씪 寃쎌슦(part_number > 1), 蹂몃Ц 泥 踰덉㎏ 臾몃떒뿉꽌 "븵꽌 떎猷⑥뿀뜕 吏궃 룷뒪듃쓽 빑떖 媛쒕뀗쓣 湲곕컲쑝濡, 씠踰 렪뿉꽌뒗 씠瑜 뜑슧 떖솕븯怨 떎쟾뿉꽌 쟻슜븷 닔 엳뒗 뵒뀒씪븳 鍮꾧껐쓣 븣븘遊낅땲떎"씪뒗 臾몄옣쓣 옄뿰뒪읇寃 뿰寃고븯꽭슂.
    5. **(젣2렪 蹂몃Ц 쟾슜 吏移)**: 씠 湲씠 젣2렪씪 寃쎌슦, 湲쓽 꽌몢 샊 蹂몃Ц 떆옉 떆젏뿉 룆옄瑜 뼢빐 "씠 以묒뿉꽌 궡媛 諛붾줈 뵲씪 븷 닔 엳뒗 寃 뼱뼡 嫄댁 援щ텇릺굹슂?"씪뒗 吏곴쟻씤 吏덈Ц쓣 뜕吏꽭슂. 씠뼱꽌 湲쓣 씫뒗 媛씠뱶씪씤쑝濡 "[끂肄붾뱶(No-Code)] 빆紐⑹ 샎옄꽌 利됱떆 떎뻾븯뿬 '븷 닔 엳떎'뒗 닔以쑝濡, [濡쒖슦肄붾뱶(Low-Code)] 빆紐⑹ 湲곗닠 쟾臾멸굹 옄룞솕 떆뒪뀥 뿉씠쟾듃쓽 '룄씠 븘슂븯떎'뒗 닔以"쑝濡 紐낇솗엳 벑湲됱쓣 굹늻뼱 蹂몃Ц쓣 긽꽭 꽌닠빐 二쇱꽭슂.
    6. **(鍮꾩슜쓽 쁽떎꽦 諛 끂肄붾뱶/濡쒖슦肄붾뱶 援щ텇 諛섏쁺)**:
       - 3렪~5렪 벑 紐⑤뱺 룄援(Zapier, Make, HubSpot, Notion 벑)瑜 뼵湲됲븷 븣, 諛섎뱶떆 媛 룄援щ쭏떎 [끂肄붾뱶] 삉뒗 [濡쒖슦肄붾뱶] 벑湲 遺꾨쪟 깭洹몃 몴湲고빐 二쇱꽭슂.
       - 삉븳 빐떦 룄援ш "臾대즺 젣怨 踰붿쐞(Free Tier)媛 뼱뒓 젙룄씤吏, 洹몃━怨 쑀猷 寃곗젣 떆 썡 뼹留덉쓽 삁긽 鍮꾩슜씠 諛쒖깮븯뒗吏(삁: 썡 $20 꽑)"瑜 諛섎뱶떆 援ъ껜쟻쑝濡 1以 씠긽 紐낆떆븯꽭슂. (Notion DB굹 援ш 떆듃 媛숈 1씤 李쎌뾽媛 留욎땄삎 臾대즺/媛 븞룄 븿猿 젣떆븯꽭슂.)
    7. **(6렪 諛 7렪 븳援 쁽떎 듅솕 吏移)**:
       - 젣6렪(슫쁺/옱臾 옄룞솕): 떒닚 빐쇅 QuickBooks 쐞二 꽕紐낆 諛곗젣븯怨, 諛섎뱶떆 援꽭泥 솃깮뒪 쟾옄꽭湲덇퀎궛꽌 뿰룞, 罹먯떆끂듃(Cashnote), 뜑議/궪姨쒖궪 벑 援궡 1씤 湲곗뾽媛뱾씠 궗슜븯뒗 濡쒖뺄 옱臾/꽭臾 옄룞솕 룄援ъ 뿰怨 諛⑸쾿쓣 以묒떖쑝濡 끉由ъ쟻쑝濡 옉꽦븯꽭슂.
       - 젣7렪(Python/RPA): Python 븰뒿 怨≪꽑뿉 빐 쁽떎쟻 븞(삁: '吏곸젒 肄붾뵫븯吏 븡怨 AI 梨쀫큸뿉寃 봽濡ы봽듃瑜 以섏꽌 10珥 留뚯뿉 肄붾뱶瑜 吏쒖삤寃 떆궎湲')쓣 諛섎뱶떆 젣떆븯꽭슂. 븘슱윭 쎒 뒪겕옒븨쓣 떎猷 떆 援궡踰뺤쟻 뀒몢由ъ씤 "젙蹂댄넻떊留앸쾿 젣48議(젙蹂댄넻떊留 移⑦빐) 諛 옉沅뚮쾿 臾대떒 닔吏 씠뒋"뿉 珥됰릺吏 븡룄濡 씠슜 빟愿怨 濡쒕큸 諛곗젣 몴以(robots.txt)쓣 以닔븯씪뒗 媛뺣젰븳 寃쎄퀬 臾멸뎄瑜 諛섎뱶떆 궫엯븯꽭슂.
    8. **(李멸퀬옄猷 깮꽦 諛 씠빐異⑸룎 諛곗젣)**: 
       - 蹂몃Ц 留 븯떒뿉 蹂몃Ц 二쇱젣 셿踰쏀엳 遺빀븯怨 떊猶고븷 닔 엳뒗 怨듭떇 궗씠듃 二쇱냼 2媛쒕 븘옒 HTML 삎떇쑝濡 젣怨듯븯꽭슂.
       - 3렪쓣 젣쇅븳  룷뒪듃뿉꽌뒗 Zapier, Make 벑 긽뾽쟻/씠빐異⑸룎 슂냼瑜 셿쟾엳 諛곗젣븯怨, 떊 怨듭떊젰 엳뒗 鍮꾩쫰땲뒪 뿰援ъ냼, 以묒냼踰ㅼ쿂湲곗뾽遺, 븳援뜲씠꽣궛뾽吏꾪씎썝, W3C 몴以 媛씠뱶 벑 媛앷쟻 異쒖쿂留 궗슜빐빞 빀땲떎.
       - 蹂몃Ц 궡슜怨 留ㅼ묶릺吏 븡뒗 옉쐞쟻 異쒖쿂뒗 젅 湲덉빀땲떎.
       
       *(삁쇅: 留뚯빟 쁽옱 벐뒗 湲씠 젣3렪씪 寃쎌슦, 湲 븯떒쓽 李멸퀬옄猷 쁺뿭뿉 븘옒 7媛쒖쓽 紐⑸줉쓣 젙솗엳 異쒕젰븯꽭슂)*
         
       젣3렪 쟾슜 異쒖쿂 紐⑸줉 留덊겕뾽 洹쒓꺽:
       <ul>
           <li><a href="https://zapier.com/blog/" target="_blank">Zapier 怨듭떇 釉붾줈洹 - Zapier Blog</a></li>
           <li><a href="https://make.com/en/help" target="_blank">Make 怨듭떇 媛씠뱶 諛 룄留 - Make Help Center</a></li>
           <li><a href="https://www.notion.so/help" target="_blank">Notion 궗슜옄 媛씠뱶 꽱꽣 - Notion Help Center</a></li>
           <li><a href="https://airtable.com/guides" target="_blank">Airtable 怨듭떇 솢슜 媛씠뱶 - Airtable Guides</a></li>
           <li><a href="https://bubble.io/blog" target="_blank">Bubble 怨듭떇 媛쒕컻 釉붾줈洹 - Bubble Blog</a></li>
           <li><a href="https://glideapps.com/blog" target="_blank">Glide 怨듭떇 뒠넗由ъ뼹 釉붾줈洹 - Glide Blog</a></li>
           <li><a href="https://wordpress.org/support/" target="_blank">WordPress 怨듭떇 吏썝 媛씠뱶 - WordPress Support</a></li>
       </ul>

    9. 異쒕젰 寃곌낵臾쇱 닚닔 HTML 蹂몃Ц 뀓뒪듃 삎깭濡쒕쭔 諛섑솚븯꽭슂.
    """
    
    response = safe_generate("gemini-2.5-flash", prompt)
    print(f"-> [Writer] {part_number}렪 蹂몃Ц 吏묓븘 셿猷!")
    return response.text.strip()

# ==========================================================================
# 뿉씠쟾듃 3: 렪吏 뿉씠쟾듃 (Editor Agent)
# ==========================================================================
def run_editor(title, raw_content):
    print(f"\n[Editor] {title} 蹂몃Ц 寃닔 諛 SEO 理쒖쟻솕 硫뷀 異붿텧 吏꾪뻾 以...")
    
    prompt = f"""
    떦떊 釉붾줈洹 닔꽍 뿉뵒꽣씠옄 SEO 쟾臾멸엯땲떎. 
    옉꽦맂 썝蹂 湲쓣 遺꾩꽍븯뿬 援ш 寃깋 遊뉗씠 媛옣 醫뗭븘븯뒗 理쒖쥌 諛고룷 뼇떇쑝濡 젙由ы빐 二쇱꽭슂.
    
    썝蹂 젣紐: "{title}"
    썝蹂 蹂몃Ц(HTML):
    {raw_content}
    
    洹쒖튃:
    1. 蹂몃Ц 븞뿉꽌 뼱깋븯嫄곕굹 AI媛 벖 쓷쟻씠 굹뒗 遺옄뿰뒪윭슫 臾몃㎘씠 엳떎硫 떎벉뼱 셿꽦룄 넂 븳援뼱 뀓뒪듃濡 蹂댁젙븯꽭슂. (듅엳 李멸퀬옄猷 留곹겕 HTML 援ъ“媛 源⑥吏 븡寃 蹂댁〈븯꽭슂.)
    2. 援ш 寃깋 뿏吏꾩슜 140옄 궡쇅쓽 硫뷀 꽕紐(meta description)쓣 옉꽦븯꽭슂.
    3. 湲뿉 깭洹몃줈 벑濡앺븷 留뚰븳 빑떖 궎썙뱶 4~5媛쒕 돹몴(,)濡 援щ텇빐 異붿텧븯꽭슂.
    4. 寃곌낵瑜 諛섎뱶떆 븘옒 JSON 룷留룹쑝濡 異쒕젰븯꽭슂. 留덊겕떎슫 湲고샇(```json)瑜 룷븿븯吏 留먭퀬 닚닔 JSON 臾몄옄뿴留 異쒕젰븯꽭슂.

    異쒕젰 룷留:
    {{
        "final_title": "젙룉맂 理쒖쥌 젣紐",
        "final_content": "蹂댁젙 셿猷뚮맂 蹂몃Ц HTML 쟾泥 궡슜",
        "description": "援ш 寃깋 寃곌낵李쎌뿉 蹂댁뿬吏 븳 以 슂빟 硫뷀꽕紐",
        "tags": ["깭洹1", "깭洹2", "깭洹3", "깭洹4"]
    }}
    """
    
    response = safe_generate("gemini-2.5-flash", prompt)
    
    try:
        clean_text = response.text.strip()
        if "```json" in clean_text:
            clean_text = clean_text.split("```json")[1].split("```")[0].strip()
        else:
            clean_text = clean_text.replace("```", "").strip()
            
        import re
        clean_text = re.sub(r'\n(?!\s*[{}"\[\]])', '\\n', clean_text)
        
        editor_data = json.loads(clean_text)
        print("-> [Editor] 理쒖쥌 寃닔 諛 SEO 硫뷀뜲씠꽣 異붿텧 셿猷!")
        return editor_data
    except Exception as e:
        print("[ERROR] [Editor] JSON 뙆떛 삤瑜 諛쒖깮. 臾몄옄뿴 媛뺤젣 蹂듦뎄 硫붿빱땲利섏쓣 媛룞빀땲떎.")
        try:
            import re
            raw_txt = response.text.strip()
            desc_match = re.search(r'"description"\s*:\s*"(.*?)"', raw_txt, re.DOTALL)
            title_match = re.search(r'"final_title"\s*:\s*"(.*?)"', raw_txt, re.DOTALL)
            content_match = re.search(r'"final_content"\s*:\s*"(.*?)"', raw_txt, re.DOTALL)
            
            desc_val = desc_match.group(1).replace('\n', ' ') if desc_match else "SEO 理쒖쟻솕 룷뒪똿엯땲떎."
            title_val = title_match.group(1) if title_match else title
            content_val = content_match.group(1) if content_match else raw_content
            
            backup_data = {
                "final_title": title_val,
                "final_content": content_val,
                "description": desc_val,
                "tags": ["IT 옄룞솕", "깮궛꽦 뼢긽", "1씤 湲곗뾽"]
            }
            print("-> [Editor] 蹂듦뎄 硫붿빱땲利섏쓣 넻빐 理쒖쥌 뜲씠꽣 蹂듭썝 꽦怨!")
            return backup_data
        except Exception as fallback_err:
            print("[CRITICAL] 蹂듦뎄 硫붿빱땲利섎룄 떎뙣뻽뒿땲떎. 썝蹂 뀓뒪듃:")
            print(response.text)
            raise e

# ==========================================================================
# 썙뱶봽젅뒪 諛고룷 紐⑤뱢 (WordPress Publisher)
# ==========================================================================
def publish_to_wordpress(editor_data):
    if WP_USER == "YOUR_WP_USERNAME" or not WP_USER:
        print("\n[INFO] 썙뱶봽젅뒪 젙蹂닿 삁떆 긽깭엯땲떎. 諛고룷瑜 깮왂븯怨 寃곌낵 뙆씪留 濡쒖뺄뿉 옣빀땲떎.")
        return None
        
    print(f"\n[WordPress] '{editor_data['final_title']}' 썙뱶봽젅뒪 釉붾줈洹몄뿉 諛고룷 以...")
    
    api_endpoint = f"{WP_URL}/wp-json/wp/v2/posts"
    headers = {
        "Content-Type": "application/json"
    }
    
    import base64
    credentials = f"{WP_USER}:{WP_APPLICATION_PASSWORD}"
    token = base64.b64encode(credentials.encode()).decode("utf-8")
    headers["Authorization"] = f"Basic {token}"
    
    post_payload = {
        "title": editor_data["final_title"],
        "content": editor_data["final_content"],
        "status": "draft",
        "excerpt": editor_data["description"]
    }
    
    try:
        response = requests.post(api_endpoint, json=post_payload, headers=headers, timeout=15)
        if response.status_code == 201:
            post_info = response.json()
            print("SUCCESS 썙뱶봽젅뒪뿉 엫떆湲濡 벑濡앸릺뿀뒿땲떎!")
            return post_info['link']
        else:
            print(f"FAILED 썙뱶봽젅뒪 API 쓳떟 肄붾뱶: {response.status_code}")
            return None
    except Exception as e:
        print(f"FAILED 썙뱶봽젅뒪 꽌踰 뿰寃 떎뙣: {str(e)}")
        return None

# 寃곌낵 濡쒖뺄 諛깆뾽 諛 뜲씠꽣 蹂댁〈 蹂댁옣
def save_local_file(data, filename="posts.json"):
    posts_filepath = "posts.json"
    
    existing_posts = []
    if os.path.exists(posts_filepath):
        try:
            with open(posts_filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    existing_posts = json.loads(content)
        except Exception as e:
            print(f"[WARNING] 湲곗〈 {posts_filepath} 뙆씪 濡쒕뱶 떎뙣: {e}")

    new_id = 1
    if existing_posts:
        new_id = max([p.get('id', 0) for p in existing_posts]) + 1

    # 썙뱶봽젅뒪슜 理쒖쥌 뜲씠꽣瑜 뵆옯뤌 洹쒓꺽뿉 留ㅽ븨
    category_mapped = "鍮꾩쫰땲뒪"
    if "2렪" in data.get("final_title", ""):
        category_mapped = "닔씡솕"
    elif "3렪" in data.get("final_title", "") or "4렪" in data.get("final_title", ""):
        category_mapped = "湲고쉷"
    elif "5렪" in data.get("final_title", "") or "7렪" in data.get("final_title", ""):
        category_mapped = "씪諛"

    new_post = {
        "id": new_id,
        "category": category_mapped,
        "title": data.get("final_title", "젣紐 뾾쓬"),
        "date": time.strftime("%Y-%m-%d"),
        "author": "넄濡쒗봽젅꼫",
        "excerpt": data.get("description", "룷뒪듃 슂빟씠 뾾뒿땲떎."),
        "content": data.get("final_content", ""),
        "themeColor": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    }

    # 以묐났 씠 泥댄겕 썑 異붽/뜮뼱벐湲
    is_duplicate = any(p.get('title') == new_post['title'] for p in existing_posts)
    if not is_duplicate:
        existing_posts.append(new_post)
        print(f"-> [SYSTEM] posts.json뿉 '{new_post['title']}' 湲씠 븞쟾븯寃 쁺援 湲곕줉릺뿀뒿땲떎.")
    else:
        for idx, p in enumerate(existing_posts):
            if p.get('title') == new_post['title']:
                existing_posts[idx] = new_post
                print(f"-> [SYSTEM] posts.json뿉 湲곗〈 '{new_post['title']}' 湲쓣 꽦怨듭쟻쑝濡 뾽뜲씠듃뻽뒿땲떎.")
                break

    temp_filepath = posts_filepath + ".tmp"
    try:
        with open(temp_filepath, "w", encoding="utf-8") as f:
            json.dump(existing_posts, f, ensure_ascii=False, indent=2)
        
        if os.path.exists(posts_filepath):
            os.remove(posts_filepath)
        os.rename(temp_filepath, posts_filepath)
        print(f"LOCAL BACKUP 理쒖쥌 룷뒪듃 쟾泥 뜲씠꽣媛 븞쟾븯寃 '{posts_filepath}'뿉 늻쟻 蹂댁〈릺뿀뒿땲떎.")
        
        # GitHub 옣냼 옄룞 룞湲고솕 (Vercel 諛고룷 듃由ш굅)
        sync_to_github()
    except Exception as e:
        print(f"[CRITICAL] posts.json 뜲씠꽣 蹂댁〈 떎뙣: {e}")
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)

# 濡쒖뺄 Git 蹂寃 궗빆 옄룞 而ㅻ컠/뫖떆 븿닔
def sync_to_github():
    import subprocess
    print("\n[Git Sync] GitHub 옣냼뿉 蹂寃 뜲씠꽣 룞湲고솕 떆룄 以...")
    try:
        if not os.path.exists(".git"):
            print("[Git Sync WARNING] 濡쒖뺄 뤃뜑뿉 Git 옣냼媛 珥덇린솕릺뼱 엳吏 븡뒿땲떎. 룞湲고솕 떒怨꾨 嫄대꼫쐛땲떎.")
            return
            
        subprocess.run(["git", "add", "posts.json"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        commit_res = subprocess.run(["git", "commit", "-m", f"Auto-update posts database: {time.strftime('%Y-%m-%d %H:%M:%S')}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if commit_res.returncode == 0:
            print("[Git Sync] 꽦怨듭쟻쑝濡 而ㅻ컠쓣 留뚮뱾뿀뒿땲떎.")
        else:
            if "nothing to commit" in commit_res.stdout.decode('utf-8', errors='ignore') or "nothing added" in commit_res.stdout.decode('utf-8', errors='ignore'):
                print("[Git Sync] 蹂寃쎈맂 궡슜씠 뾾뼱 而ㅻ컠쓣 깮왂빀땲떎.")
                return
            else:
                print(f"[Git Sync WARNING] 而ㅻ컠 떎뙣: {commit_res.stderr.decode('utf-8', errors='ignore')}")
                return

        subprocess.run(["git", "push"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("SUCCESS [Git Sync] GitHub濡 뫖떆 셿猷! 빟 30珥 궡濡 Vercel뿉 諛섏쁺맗땲떎.")
    except Exception as e:
        print(f"[Git Sync ERROR] GitHub 룞湲고솕 以 삤瑜 諛쒖깮: {e}")

# ==========================================================================
# 硫붿씤 젣뼱 猷⑦봽
# ==========================================================================

# ==========================================================================
# 구글 드라이브 연동 스마트 수집 및 자동 분류 모듈 (Google Drive Organizer)
# ==========================================================================
def scan_and_process_google_drive():
    import glob
    print("\n[Drive Scan] 구글 드라이브(G:\\내 드라이브) 실시간 모니터링 및 스캔 중...")
    
    drive_path = "G:\\내 드라이브"
    if not os.path.exists(drive_path):
        print(f"[Drive Scan WARNING] 구글 드라이브 경로('{drive_path}')가 인식되지 않습니다. 가상 드라이브 상태를 확인하세요.")
        return
        
    # G:\내 드라이브 메인 영역에 존재하며 [Processed]가 들어가지 않은 최신 .txt 및 .md 파일 탐색
    txt_files = glob.glob(os.path.join(drive_path, "*.txt"))
    md_files = glob.glob(os.path.join(drive_path, "*.md"))
    all_files = txt_files + md_files
    
    target_files = []
    for fp in all_files:
        basename = os.path.basename(fp)
        # 이미 처리 완료된 파일이나 임시 파일 등은 배제
        if "[Processed]" not in basename and not basename.startswith("~$") and "posts.json" not in basename:
            target_files.append(fp)
            
    if not target_files:
        print("[Drive Scan] 구글 드라이브에 새로 들어온 미처리 NotebookLM 메모가 없습니다.")
        return
        
    print(f"[Drive Scan] 미처리 대상 문서 {len(target_files)}개 발견! 분석 및 스마트 분류를 시작합니다.")
    
    for file_path in target_files:
        basename = os.path.basename(file_path)
        print(f"\n[Drive Scan] 대상 파일 읽는 중: '{basename}'")
        
        try:
            # 안전하게 인코딩 처리하며 파일 읽기
            content = ""
            for encoding in ['utf-8', 'cp949', 'euc-kr']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read().strip()
                    break
                except UnicodeDecodeError:
                    continue
                    
            if not content:
                print(f"[Drive Scan WARNING] '{basename}' 파일이 비어있어 처리를 건너뜁니다.")
                continue
                
            # 1. AI 기반 가치 판별기 (Valuator) 구동
            is_valuable = evaluate_content_value(basename, content)
            
            if is_valuable:
                print(f"-> [AI 판별] SUCCESS: '{basename}' 은 블로그 발행 가치가 높은 양질의 지식 소스로 확인되었습니다!")
                
                # 2. AI 자동 집필 및 Vercel/워드프레스 배포 파이프라인 개시
                process_drive_file_to_post(file_path, content)
            else:
                print(f"-> [AI 판별] SKIP: '{basename}' 은 개인 메모/일반 텍스트로 판별되어 발행을 제외합니다.")
                # 중복 검사를 방지하기 위해 일반 메모도 Processed 처리하여 마킹해둡니다.
                mark_file_as_processed(file_path)
                
        except Exception as e:
            print(f"[Drive Scan ERROR] '{basename}' 처리 중 에러 발생: {e}")

# Gemini API를 통해 정보성 가치 여부(블로그 포스팅용 요약본/지식글인가)를 판별하는 함수
def evaluate_content_value(filename, content):
    print(f"[AI Valuator] '{filename}'의 내용 분석 및 가치 분류 평가 중...")
    
    prompt = f"""
    당신은 1인 비즈니스 및 기술 전문 에디터입니다.
    제시된 텍스트 내용과 파일명을 기반으로, 이 문서가 "1인 창업, IT 자동화, 비즈니스 전략, 마케팅, 지식 콘텐츠 상품화, 자기계발"에 관련된 유익한 정보성 메모/NotebookLM 요약 문서인지 정확히 분석하세요.
    
    [판별 대상 문서]
    파일명: {filename}
    본문 내용 일부:
    {content[:1500]}
    
    [판별 규칙]
    - 만약 단순 일상 기록, 개인 구매 영수증, 비즈니스와 무관한 단순 코드 조각, 낙서, 빈 문서인 경우 가치가 없다고 분류하세요.
    - 블로그 독자(솔로프레너)에게 실질적인 비즈니스 노하우나 IT 자동화 팁으로 유용한 지식성 메모라면 가치가 높다고 분류하세요.
    
    출력 형식:
    반드시 아래와 같이 단 한 단어만 응답하세요. 서술은 절대 금지합니다.
    VALUABLE 또는 UNVALUABLE
    """
    
    try:
        response = safe_generate("gemini-2.5-flash", prompt)
        result = response.text.strip().upper()
        if "VALUABLE" in result and "UNVALUABLE" not in result:
            return True
        return False
    except Exception as e:
        print(f"[AI Valuator WARNING] 분류기 호출 실패로 기본값(True)을 부여합니다. 에러: {e}")
        return True

# 선별된 정보를 바탕으로 최종 본문을 AI로 집필해 posts.json 및 워드프레스에 배포하는 함수
def process_drive_file_to_post(file_path, raw_content):
    filename = os.path.basename(file_path)
    print(f"[AI Writer] '{filename}' 원본 소스를 바탕으로 Zapier Blog 스타일의 아티클로 집필 재가공 중...")
    
    prompt = f"""
    당신은 전 세계 업무 자동화 트렌드를 이끄는 'Zapier 공식 블로그의 시니어 에반젤리스트'이자 기술 비즈니스 전문 칼럼니스트입니다.
    제시된 구글 드라이브(NotebookLM) 소스 문서를 읽고, 독자들에게 실질적인 실행 기회를 주는 고품질 블로그 아티클을 완성해 주세요.
    
    [원본 정보 소스]
    {raw_content}
    
    [집필 스타일 가이드 - Zapier Blog 벤치마킹]
    1. **구체적인 난이도 분류 (필수)**:
       - 본문 안에서 특정 기법이나 도구를 언급할 때마다 반드시 **[노코드]** 또는 **[로우코드]** 등급 분류 태그를 표기해 주세요.
         * [노코드]: 혼자서 클릭 몇 번으로 즉시 따라할 수 있는 비기술적 영역
         * [로우코드]: 개발 지식이 필요하거나 AI 비서의 코드 생성이 필요한 영역
    2. **비용 및 리소스의 현실성 명시 (필수)**:
       - 본문에서 다루는 각 소프트웨어/RPA 도구마다 무료 제공 혜택 범위(Free Tier)와 유료 결제 시 예상되는 현실적 비용(예: 월 $15 선 등)을 무조건 구체적으로 1줄 이상 명확히 기재하세요. Notion DB나 구글 시트 같은 무자본 초저가 대안도 항상 곁들이세요.
    3. **가독성을 극대화하는 서식**:
       - 텍스트 덩어리가 빽빽하지 않도록 2~3개 문단마다 HTML <h2> 또는 <h3> 소제목으로 아티클을 정갈하게 분할하세요.
       - 핵심 장점이나 워크플로우 단계는 불릿 포인트(Bullet point) 목록을 사용해 시각적으로 일목요연하게 정리하세요.
    4. **한국 비즈니스 특화 및 신뢰성**:
       - 한국 기업 현실에 어울리는 설명으로 각색하고, 본문 맨 아래에는 공신력 있는 공식 사이트 및 연구소 주소 2개를 아래 HTML 예시 형식으로 제공하세요.
         (예: <li><a href="https://www.mss.go.kr" target="_blank">중소벤처기업부 공식 사이트</a></li>)
    
    출력 결과물은 순수 HTML 본문으로만 반환하세요.
    """
    
    try:
        response = safe_generate("gemini-2.5-flash", prompt)
        raw_html = response.text.strip()
        
        # 에디터 검수 가동
        title_temp = f"[자동화 가이드] {filename.split('.')[0]}"
        editor_data = run_editor(title_temp, raw_html)
        
        # 워드프레스 배포는 후순위 작업으로 미루고, 동기적 로컬 뷰어 저장에 전력합니다.
        print("[WordPress] 워드프레스 배포가 비활성화 상태입니다. 다음 단계로 넘어갑니다.")
        
        # 로컬 posts.json 누적 및 깃허브 실시간 동기화 (Vercel 반영)
        save_local_file(editor_data, "posts.json")
        print(f"-> [AI Pipeline SUCCESS] '{filename}'이 성공적으로 가공되어 Vercel 라이브 뷰에 즉시 반영되었습니다!")
            
        # 완료 처리 마킹
        mark_file_as_processed(file_path)
    except Exception as e:
        print(f"[AI Pipeline ERROR] '{filename}' 재가공 실패: {e}")
def mark_file_as_processed(file_path):
    dir_name = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    
    new_name = f"{name} [Processed]{ext}"
    new_file_path = os.path.join(dir_name, new_name)
    
    try:
        # 파일 이름 변경
        if os.path.exists(file_path):
            os.rename(file_path, new_file_path)
            print(f"[Drive Sync] 원본 파일이 안전하게 '{new_name}'으로 이름 변경 완료(마킹완료)되었습니다.")
    except Exception as e:
        print(f"[Drive Sync WARNING] 파일 마킹 실패: {e}")
def main():
    print("==================================================")
    print("[SYSTEM] 구글 애드센스 승인 타겟 에이전트 시스템 가동")
    print("[SYSTEM] 구글 드라이브(NotebookLM) 최신 자료 스캔 및 Vercel 발행 우선 모드")
    print("==================================================")
    
    try:
        init_gemini()
    except Exception as e:
        print(e)
        return
        
    # [1순위 핵심 과업] 구글 드라이브(NotebookLM) 최신자료 스캔 및 Vercel 동적 발행 즉시 가동!
    scan_and_process_google_drive()
    
    # [2순위 연재물 과업] 8부작 고정 연재물은 1순위 완료 후에 돌거나 대기하도록 미룸
    print("\n[SYSTEM] 구글 드라이브 스캔 완료. 8부작 연재 검사를 보조적으로 대기합니다...")
    
    topic = "1인 기업의 생산성을 극대화하는 IT 자동화 비결"
    series_count = 8
    series_plan = run_planner(topic, series_count)
    
    # 기존 8부작 작성 이력 확인
    existing_titles = []
    if os.path.exists("posts.json"):
        try:
            with open("posts.json", "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    existing_posts = json.loads(content)
                    existing_titles = [p.get('title', '') for p in existing_posts]
        except Exception as e:
            print(f"[SYSTEM] 기존 posts.json 확인 불가: {e}")

    for post in series_plan['posts']:
        part_num = post['part_number']
        post_title_draft = post['title']
        
        part_prefix = f"제{part_num}편:"
        already_done = False
        for t in existing_titles:
            if part_prefix in t or post_title_draft in t or t in post_title_draft:
                already_done = True
                break
                
        if already_done:
            # 연재물 스킵 출력 최소화
            continue
            
        raw_content = run_writer(post, part_num, series_count)
        final_post_data = run_editor(post['title'], raw_content)
        post_link = publish_to_wordpress(final_post_data)
        save_local_file(final_post_data, "posts.json")
        
        if post_link:
            print(f"-> {part_num}편 워드프레스 배포 성공! 주소: {post_link}")
        else:
            print(f"-> {part_num}편 로컬 포스팅 뷰에 정상 업데이트 완료!")
            
    print("\n==================================================")
    print("SUCCESS 모든 에이전트 프로세스가 안전하게 성공적으로 완료되었습니다!")
    print("==================================================")

if __name__ == "__main__":
    main()
