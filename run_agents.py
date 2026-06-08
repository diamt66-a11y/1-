# -*- coding: utf-8 -*-
import os
import json
import requests
import google.generativeai as genai
import time
import shutil

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
    print(f"\n[Planner] 확정된 {series_count}부작 블로그 시리즈 기획안 로드 중 (목차 강제 고정)...")
    
    fixed_plan = {
        "series_title": "1인 기업의 생산성을 극대화하는 IT 자동화 비결",
        "posts": [
            {"part_number": 1, "title": "제1편: 1인 기업 IT 자동화: 지금이 기회! 생산성 10배 달성의 첫걸음", "sections": [{"sub_title": "1인 창업과 자동화의 필연성", "key_points": ["생산성 10배"]}]},
            {"part_number": 2, "title": "제2편: 1인 기업 성공 전략: 자동화 기회 발굴과 ROI 분석 프레임워크", "sections": [{"sub_title": "내 비즈니스에서 자동화 타겟 선별하기", "key_points": ["노코드 로우코드 등급 분류"]}]},
            {"part_number": 3, "title": "제3편: 1인 창업가를 위한 스마트 오피스 자동화: 소통과 협업 효율 높여 생산성 극대화", "sections": [{"sub_title": "협업 도구 자동 연계의 기초", "key_points": ["노션 DB 연동"]}]},
            {"part_number": 4, "title": "제4편: 1인 기업 마케팅/영업 자동화: 고객 유입부터 매출까지, 노코드 실전 전략", "sections": [{"sub_title": "고객 리드 수집 및 퍼널 자동화", "key_points": ["랜딩페이지 고객 수집"]}]},
            {"part_number": 5, "title": "제5편: 1인 창업가를 위한 AI 콘텐츠 생산성 혁명: 기획부터 발행까지", "sections": [{"sub_title": "AI를 활용한 콘텐츠 무한 생성 워크플로우", "key_points": ["Gemini API 활용 기획"]}]},
            {"part_number": 6, "title": "제6편: 1인 기업 재무/세무 자동화: 돈 관리부터 세금 신고까지 노코드/로우코드 솔루션 활용 가이드", "sections": [{"sub_title": "국내 세무 및 운영 자동화 로컬 연동", "key_points": ["홈택스 전자세금계산서 연동"]}]},
            {"part_number": 7, "title": "제7편: AI 비서처럼! 개발 지식 없이 로우코드/노코드 자동화 마스터하기", "sections": [{"sub_title": "개발 지식 없이 AI 비서 부려 코딩하기", "key_points": ["AI 챗봇 프롬프트 코딩 방법"]}]},
            {"part_number": 8, "title": "제8편: 1인 기업 자동화 시스템 완결판: 지속 가능한 성장을 위한 궁극 전략", "sections": [{"sub_title": "3~5년 장기 로드맵의 완성", "key_points": ["자동화 아키텍처 다이어그램"]}]}
        ]
    }
    
    if series_count < 8:
        fixed_plan["posts"] = fixed_plan["posts"][:series_count]
        
    print("-> [Planner] 사용자 확정 8부작 목차 동기화 성공!")
    return fixed_plan

# ==========================================================================
# 에이전트 2: 집필 에이전트 (Writer Agent)
# ==========================================================================
def run_writer(post_plan, part_number=1, total_parts=8):
    title = post_plan['title']
    sections = post_plan['sections']
    
    print(f"\n[Writer] {title} ({part_number}/{total_parts}) 본문 집필 시작...")
    
    sections_str = ""
    for idx, sec in enumerate(sections):
        sub_title = sec.get('sub_title') or sec.get('title') or f"섹션 {idx+1}"
        key_points = sec.get('key_points') or sec.get('keywords') or []
        sections_str += f"\n{idx+1}. 소제목: {sub_title}\n   - 다룰 키워드: {', '.join(key_points)}\n"
        
    prompt = f"""
    당신은 전문 기술/비즈니스 블로그 집필가입니다.
    기획 에이전트가 생성한 아래 소제목과 키워드를 바탕으로 깊이 있는 블로그 본문을 작성하세요.
    
    글 제목: "{title}"
    글 목차 정보: {sections_str}
    연재 현황: 총 {total_parts}부작 중 제 {part_number}편 글입니다.
    
    규칙:
    1. 글 전체 분량은 최소 공백 제외 1,500자 이상으로 길고 알차게 작성하세요.
    2. 각 소제목은 반드시 HTML의 <h2> 태그로 감싸고, 본문 문단은 <p> 태그를 이용해 단락을 구분하세요.
    3. 문체는 정중하고 신뢰감을 주는 존댓말(~합니다. ~입니다)로 통일하세요.
    4. **(이전 글 연계 및 독자 수준 정의)**: 
       - 제1편 서두에 "본 시리즈는 코딩 경험이 전혀 없는 초보 1인 창업가를 타겟으로 합니다. 7편 등에서 다루는 Python이나 스크래핑, RPA 등의 기술 요소는 독자가 개발을 마스터하는 것이 아니라 AI(Gemini, ChatGPT)를 비서처럼 부려 결과물을 얻어내는 기획자적 관점을 목표로 합니다."를 명시하세요.
       - 제2편 이상일 경우(part_number > 1), 본문 첫 번째 문단에서 "앞서 다루었던 지난 포스트의 핵심 개념을 기반으로, 이번 편에서는 이를 더욱 심화하고 실전에서 적용할 수 있는 디테일한 비결을 알아봅니다"라는 문장을 자연스럽게 연결하세요.
    5. **(제2편 본문 전용 지침)**: 이 글이 제2편일 경우, 글의 서두 혹 본문 시작 시점에 독자를 향해 "이 중에서 내가 바로 따라 할 수 있는 타겟은 어떤 건지 구분되나요?"라는 직접적인 질문을 던지세요.
    6. **(비용의 현실성 및 노코드/로우코드 구분 반영)**:
       - 3편~5편 등 모든 도구(Zapier, Make, HubSpot, Notion 등)를 언급할 때, 반드시 각 도구마다 [노코드] 또는 [로우코드] 등급 분류 태그를 표기해 주세요.
       - 또한 해당 도구가 "무료 제공 범위(Free Tier)가 어느 정도인지, 그리고 유료 결제 시 월 얼마의 예상 비용이 발생하는지(예: 월 $20 선)"를 반드시 구체적으로 1줄 이상 명시하세요.
    7. **(6편 및 7편 한국 현실 특화 지침)**:
       - 제6편(운영/재무 자동화): 단순 해외 QuickBooks 위주 설명은 배제하고, 반드시 국세청 홈택스 전자세금계산서 연동, 캐시노트(Cashnote), 더존/쎔(SSEM) 등 국내 1인 기업가들이 사용하는 로컬 재무/세무 자동화 도구와 연계 방법을 중심으로 현실적으로 작성하세요.
       - 제7편(Python/RPA): Python 학습 곡선에 대한 현실적 대안을 반드시 제시하세요.
    8. **(참고자료 생성 및 이해충돌 배제)**: 
       - 본문 맨 하단에 본문 주제와 완벽히 부합하고 신뢰할 수 있는 공식 사이트 주소 2개를 HTML 형식으로 제공하세요.
       
    9. 출력 결과물은 순수 HTML 본문 텍스트 형태로만 반환하세요.
    """
    
    response = safe_generate("gemini-2.5-flash", prompt)
    print(f"-> [Writer] {part_number}편 본문 집필 완료!")
    return response.text.strip()

# ==========================================================================
# 에이전트 3: 편집 에이전트 (Editor Agent)
# ==========================================================================
def run_editor(title, raw_content):
    print(f"\n[Editor] {title} 본문 검수 및 SEO 최적화 메타 추출 진행 중...")
    
    prompt = f"""
    당신은 블로그 수석 에디터이자 SEO 전문가입니다. 
    작성된 원본 글을 분석하여 구글 검색 로봇이 가장 좋아하는 최종 배포 양식으로 정리해 주세요.
    
    원본 제목: "{title}"
    원본 본문(HTML):
    {raw_content}
    
    규칙:
    1. 본문 안에서 어색하거나 AI가 쓴 흔적이 나는 부자연스러운 문맥이 있다면 다듬어 완성도 높은 한국어 텍스트로 보정하세요.
    2. 구글 검색 엔진용 140자 내외의 메타 설명(meta description)을 작성하세요.
    3. 글에 태그로 등록할 만한 핵심 키워드 4~5개를 쉼표(,)로 구분해 추출하세요.
    4. 결과를 반드시 아래 JSON 포맷으로 출력하세요. 마크다운 기호를 포함하지 말고 순수 JSON 문자열만 출력하세요.

    출력 포맷:
    {{
        "final_title": "정돈된 최종 제목",
        "final_content": "보정 완료된 본문 HTML 전체 내용",
        "description": "구글 검색 결과창에 보여질 한 줄 요약 메타설명",
        "tags": ["태그1", "태그2", "태그3", "태그4"]
    }}
    """
    
    import re
    response = safe_generate("gemini-2.5-flash", prompt)
    
    try:
        clean_text = response.text.strip()
        if "```json" in clean_text:
            clean_text = clean_text.split("```json")[1].split("```")[0].strip()
        else:
            clean_text = clean_text.replace("```", "").strip()
            
        clean_text = re.sub(r'\n(?!\s*[{}"\[\]])', '\\n', clean_text)
        
        editor_data = json.loads(clean_text)
        print("-> [Editor] 최종 검수 및 SEO 메타데이터 추출 완료!")
        return editor_data
    except Exception as e:
        print("[ERROR] [Editor] JSON 파싱 오류 발생. 강제 복구 메커니즘을 가동합니다.")
        try:
            raw_txt = response.text.strip()
            desc_match = re.search(r'"description"\s*:\s*"(.*?)"', raw_txt, re.DOTALL)
            title_match = re.search(r'"final_title"\s*:\s*"(.*?)"', raw_txt, re.DOTALL)
            content_match = re.search(r'"final_content"\s*:\s*"(.*?)"', raw_txt, re.DOTALL)
            
            desc_val = desc_match.group(1).replace('\n', ' ') if desc_match else "SEO 최적화 포스팅입니다."
            title_val = title_match.group(1) if title_match else title
            content_val = content_match.group(1) if content_match else raw_content
            
            backup_data = {
                "final_title": title_val,
                "final_content": content_val,
                "description": desc_val,
                "tags": ["IT 자동화", "생산성 향상", "1인 기업"]
            }
            print("-> [Editor] 복구 메커니즘을 통해 최종 데이터 복원 성공!")
            return backup_data
        except Exception as fallback_err:
            print("[CRITICAL] 복구 메커니즘도 실패했습니다.")
            raise e

# ==========================================================================
# 워드프레스 배포 모듈 (WordPress Publisher)
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
        
    # G:\내 드라이브 메인 영역에 존재하며 [Processed]가 들어가지 않은 최신 .txt, .md, .docx 파일 탐색
    txt_files = glob.glob(os.path.join(drive_path, "*.txt"))
    md_files = glob.glob(os.path.join(drive_path, "*.md"))
    docx_files = glob.glob(os.path.join(drive_path, "*.docx"))
    all_files = txt_files + md_files + docx_files
    
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
            for encoding in ['utf-16', 'utf-8', 'cp949', 'euc-kr']:
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
                category = determine_category_folder(basename, content)
                process_drive_file_to_post(file_path, content, category)
            else:
                print(f"-> [AI 판별] SKIP: '{basename}' 은 개인 메모/일반 텍스트로 판별되어 발행을 제외합니다.")
                # 중복 검사를 방지하기 위해 일반 메모도 테마 분류하여 이동합니다.
                archive_and_classify_file(file_path, is_uploaded=False, raw_content=content)
                
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
    당신은 시스템 자동화와 수익 다각화를 연구하는 1인 기업가이자 비즈니스 에디터인 '솔로프레너'입니다.
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
         (예: <li><a href="https://www.mss.go.kr" target="_blank" rel="noopener" rel="noopener">중소벤처기업부 공식 사이트</a></li>)
    
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
            
        # 완료 처리 마킹 (블로그 업로드 완료 전용 폴더 이동)
        archive_and_classify_file(file_path, is_uploaded=True)
    except Exception as e:
        print(f"[AI Pipeline ERROR] '{filename}' 재가공 실패: {e}")

# AI가 주제별로 드라이브 폴더명을 결정하는 함수
def determine_category_folder(filename, content):
    prompt = f"""
    당신은 구글 드라이브 파일 정리 비서입니다.
    제시된 텍스트 내용 및 파일명을 분석하여, 이 파일의 주제에 가장 잘 어울리는 폴더명을 한글로 결정하세요.
    
    [분류 가이드]
    - IT 자동화 관련: IT_자동화
    - 비즈니스 전략, 1인 창업 관련: 비즈니스_전략
    - 애드센스, 수익화 관련: 디지털_수익화
    - 기타 일반 주제, 개인 메모, 낙서: 일반_메모
    
    [대상 문서]
    파일명: {filename}
    본문 내용 일부:
    {content[:1000]}
    
    [출력 규칙]
    반드시 위에 나열된 4가지 폴더명(IT_자동화, 비즈니스_전략, 디지털_수익화, 일반_메모) 중 하나만 응답하세요. 다른 부가 설명은 절대 하지 마세요.
    """
    try:
        response = safe_generate("gemini-2.5-flash", prompt)
        result = response.text.strip().replace("`", "").replace(" ", "").strip()
        valid_folders = ["IT_자동화", "비즈니스_전략", "디지털_수익화", "일반_메모"]
        for vf in valid_folders:
            if vf in result:
                return vf
        return "일반_메모"
    except Exception as e:
        print(f"[AI Category Folder Selector WARNING] {e}")
        return "일반_메모"

# 업로드 완료된 파일 및 일반 메모 분류 이동 함수
def archive_and_classify_file(file_path, is_uploaded=False, raw_content=""):
    drive_path = "G:\\내 드라이브"
    if not os.path.exists(drive_path):
        print("[Drive Organizer WARNING] 구글 드라이브 경로가 존재하지 않아 분류 이동을 건너뜁니다.")
        return
        
    base_name = os.path.basename(file_path)
    
    try:
        if is_uploaded:
            target_folder = os.path.join(drive_path, "블로그_업로드_완료")
        else:
            folder_name = determine_category_folder(base_name, raw_content)
            target_folder = os.path.join(drive_path, folder_name)
            
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            
        target_path = os.path.join(target_folder, base_name)
        
        # 파일명 중복 회피
        if os.path.exists(target_path):
            name, ext = os.path.splitext(base_name)
            target_path = os.path.join(target_folder, f"{name}_{int(time.time())}{ext}")
            
        if os.path.exists(file_path):
            shutil.move(file_path, target_path)
            print(f"[Drive Organizer] '{base_name}' 파일을 '{os.path.basename(target_folder)}' 폴더로 분류 이동 완료했습니다.")
    except Exception as e:
        print(f"[Drive Organizer WARNING] '{base_name}' 파일 분류 이동 실패: {e}")

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

def run_reviser(title, raw_content, instructions):
    print(f"\n[Reviser] {title} 사용자 맞춤 수정 진행 중...")
    
    prompt = f"""
    당신은 전문 콘텐츠 에디터입니다.
    사용자의 특별한 수정 지시사항을 반영하여 기존 블로그 본문을 다시 작성해 주세요.
    
    원본 제목: "{title}"
    사용자 수정 지시사항: "{instructions}"
    
    원본 본문(HTML):
    {raw_content}
    
    규칙:
    1. 사용자의 수정 지시사항을 완벽하게 반영하세요.
    2. HTML 태그 구조를 최대한 유지하되, 내용 수정에 필요한 부분은 자연스럽게 변경하세요.
    3. 결과물은 순수 HTML 본문 텍스트 형태로만 반환하세요.
    """
    
    response = safe_generate("gemini-2.5-flash", prompt)
    clean_text = response.text.strip()
    if clean_text.startswith("```html"):
        clean_text = clean_text[7:]
    if clean_text.startswith("```"):
        clean_text = clean_text[3:]
    if clean_text.endswith("```"):
        clean_text = clean_text[:-3]
        
    return clean_text.strip()

if __name__ == "__main__":
    main()
