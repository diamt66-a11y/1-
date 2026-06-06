import os
import json
import requests
import google.generativeai as genai
import time

# ==========================================================================
# 1인 기업 에이전트 시스템 환경 설정 (보안상 .env 파일로부터 로드)
# ==========================================================================
GEMINI_API_KEY = ""
WP_URL = ""
WP_USER = ""
WP_APPLICATION_PASSWORD = ""

# .env 파일 파싱 처리
if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                # 따옴표 제거
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

# OS 환경변수 백업 처리 (Vercel 배포 시 서버 환경변수 대응용)
GEMINI_API_KEY = GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
WP_URL = WP_URL or os.environ.get("WP_URL", "")
WP_USER = WP_USER or os.environ.get("WP_USER", "")
WP_APPLICATION_PASSWORD = WP_APPLICATION_PASSWORD or os.environ.get("WP_APPLICATION_PASSWORD", "")
# ==========================================================================

# Gemini API 초기화 함수
def init_gemini():
    if not GEMINI_API_KEY:
        raise ValueError("[ERROR] GEMINI_API_KEY가 설정되지 않았습니다. .env 파일이나 환경 변수를 확인해주세요.")
    genai.configure(api_key=GEMINI_API_KEY)

# 429 에러 대응용 안전한 API 호출 헬퍼 함수 (자동 재시도)
import time
def safe_generate(model_name, prompt, max_retries=5, delay_secs=45):
    model = genai.GenerativeModel(model_name)
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response
        except Exception as e:
            err_msg = str(e)
            # 429 할당량 한도 도달 오류 감지 시
            if "429" in err_msg or "quota" in err_msg.lower() or "limit" in err_msg.lower():
                if attempt < max_retries - 1:
                    print(f"\n[SYSTEM WARNING] API 한도(429) 도달. {delay_secs}초 대기 후 재시도합니다... (시도 {attempt+1}/{max_retries})")
                    # 대시보드 화면 콘솔에 대기 알림을 띄우기 위해 streamlit이 활성화되어 있으면 텍스트 추가
                    time.sleep(delay_secs)
                    # 대기 시간 점진적 증가
                    delay_secs += 15
                    continue
            raise e


# ==========================================================================
# 에이전트 1: 기획 에이전트 (Planner Agent) - N부작 시리즈 기획 지원
# ==========================================================================
def run_planner(topic, series_count=3):
    print(f"\n[Planner] {topic} 주제로 {series_count}부작 블로그 시리즈 포스트 기획 중...")
    
    prompt = f"""
    당신은 구글 SEO 분석기입니다. 
    제시된 블로그 대주제 "{topic}"에 대해 깊이 있는 구글 검색 의도를 파악하고,
    총 {series_count}부작의 '시리즈 연재물' 전체 기획서를 잡으세요.
    
    각 편마다 완전히 독립적이면서도 내용상 긴밀히 연계되는 제목과 개별 목차(H2/H3 용)가 구성되어야 합니다.
    
    규칙:
    1. 총 {series_count}개의 포스트 정보를 도출하세요.
    2. 각 포스트마다 구체적인 소제목 2~3개를 도출하세요.
    3. **(필수 - 전체 논리 일관성 및 뼈대 설계 규칙)**:
       - **[구축 로드맵 선배치]**: 제1편과 제2편의 소제목 영역에 1인 창업 전체를 관통하는 '3~5년 장기 로드맵 수립 가이드' 및 'ROI 분석 프레임워크' 내용을 개요 형태로 선배치하여 8편과의 일관성을 잡으세요.
       - **[예고 모순 방지 및 편 번호 엇갈림 방지]**: 각 편의 기획 설계 시, 마지막 단락에 들어갈 '다음 편 예고' 키워드를 명확하게 선언하여 콘텐츠 신규 삽입이나 순서 변경에 따라 편 번호와 주제 예고가 모순되지 않도록 정확한 빌드업 정보를 설계에 포함하세요.
       - **[국내 세무 6편 고정]**: 5편에서 예고한 캐시노트, 홈택스, 더존 등의 한국 세무 자동화 실무는 반드시 **제6편(운영/재무 자동화)**에서 심도 있게 다뤄지도록 설계하세요. (기타 콘텐츠 자동화 편이 추가되더라도 6편 세무 약속이 깨지지 않게 하세요.)
       - **[생산성 10배 실증 근거]**: "생산성 10배"라는 타이틀의 합리성을 위해, 1편과 2편 본문 구성에 **"주 40시간 중 단순 반복 업무 36시간을 자동화하여 코어 업무에 4시간만 집중함으로써 효율을 10배 높이는 구체적인 시간 환산 수식 및 실증적 산출 근거"**를 포함하도록 키 포인트를 강제 지정하세요.
       - **[난이도 완충]**: 7편과 같이 개발 지식이 요하는 부분(Python, RPA 등)도 기획 단계부터 "개발을 직접 하는 것이 아닌 비서로서 AI를 다루는 1인 창업가의 자세" 관점으로 구성되도록 소제목 및 핵심 포인트를 조정하세요.
    4. 본인 의견이나 서술은 배제하고, 반드시 아래 구조의 JSON 포맷으로만 출력하세요. 마크다운 기호(```json)를 포함하지 말고 순수 JSON 문자열만 출력하세요.

    출력 포맷 예시 ({series_count}부작 기준):
    {{
        "series_title": "전체 시리즈를 관통하는 통합 대주제 제목",
        "posts": [
            {{
                "part_number": 1,
                "title": "제1편: 1편의 구체적인 제목",
                "sections": [
                    {{"sub_title": "첫 번째 소제목", "key_points": ["다룰 핵심 키워드 1", "다룰 핵심 키워드 2"]}},
                    {{"sub_title": "두 번째 소제목", "key_points": ["다룰 핵심 키워드 1", "다룰 핵심 키워드 2"]}}
                ]
            }},
            {{
                "part_number": 2,
                "title": "제2편: 2편의 구체적인 제목",
                "sections": [
                    {{"sub_title": "첫 번째 소제목", "key_points": ["키워드"]}}
                ]
            }}
        ]
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
        
        plan_data = json.loads(clean_text)
        print("-> [Planner] 시리즈 기획안 생성 완료!")
        return plan_data
    except Exception as e:
        print("[ERROR] [Planner] JSON 파싱 오류 발생. 원시 텍스트 클리닝 처리로 우회를 시도합니다.")
        try:
            # 수동 정규식 파싱 시도 (시리즈 제목 및 최소 뼈대 복구)
            raw_txt = response.text.strip()
            series_title_match = re.search(r'"series_title"\s*:\s*"(.*?)"', raw_txt)
            series_title = series_title_match.group(1) if series_title_match else "1인 기업 자동화 연재 시리즈"
            
            # 최소 포스트 2개부터 최대 8개까지 동적으로 기획 복구 뼈대 제공
            posts_backup = []
            for i in range(1, series_count + 1):
                posts_backup.append({
                    "part_number": i,
                    "title": f"제{i}편: {topic}의 실전 마스터 전략 Part {i}",
                    "sections": [
                        {"sub_title": f"파트 {i} 핵심 단계별 실습", "key_points": ["도구 활용", "과제 해결", "비즈니스 적용"]}
                    ]
                })
            backup_plan = {
                "series_title": series_title,
                "posts": posts_backup
            }
            print("-> [Planner] 기획 복구 메커니즘 성공!")
            return backup_plan
        except Exception as fe:
            print("[CRITICAL] Planner 기획 복구 실패:")
            print(response.text)
            raise e

# ==========================================================================
# 에이전트 2: 집필 에이전트 (Writer Agent) - 참고자료 자동 삽입 지원
# ==========================================================================
def run_writer(post_plan, part_number=1, total_parts=3):
    title = post_plan['title']
    sections = post_plan['sections']
    
    print(f"\n[Writer] {title} ({part_number}/{total_parts}) 본문 집필 시작...")
    
    sections_str = ""
    for idx, sec in enumerate(sections):
        sections_str += f"\n{idx+1}. 소제목: {sec['sub_title']}\n   - 다룰 키워드: {', '.join(sec['key_points'])}\n"
        
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
    4. **(필수 - 이전 글 연계 및 독자 수준 정의)**: 
       - 제1편 서두에 **"본 시리즈는 코딩 경험이 전혀 없는 초보 1인 창업가를 타겟으로 합니다. 7편 등에서 다루는 Python이나 스크래핑, RPA 등의 기술 요소는 독자가 개발을 마스터하는 것이 아니라 AI(Gemini, ChatGPT)를 비서처럼 부려 결과물을 얻어내는 기획자적 관점을 목표로 합니다."**를 명시하세요.
       - 제2편 이상일 경우(part_number > 1), 본문 첫 번째 문단에서 **"앞서 다루었던 지난 포스트의 핵심 개념을 기반으로, 이번 편에서는 이를 더욱 심화하고 실전에서 적용할 수 있는 디테일한 비결을 알아봅니다"**라는 문장을 자연스럽게 연결하세요.
    5. **(필수 - 제2편 본문 전용 지침)**: 이 글이 **제2편**일 경우, 글의 서두 혹은 본문 시작 시점에 독자를 향해 **"이 중에서 내가 바로 따라 할 수 있는 게 어떤 건지 구분되나요?"**라는 직관적인 질문을 던지세요. 이어서 글을 읽는 가이드라인으로 **"[노코드(No-Code)] 항목은 혼자서 즉시 실행하여 '할 수 있다'는 수준으로, [로우코드(Low-Code)] 항목은 기술 전문가나 자동화 시스템 에이전트의 '도움이 필요하다'는 수준"**으로 명확히 등급을 나누어 본문을 상세 서술해 주세요.
    6. **(필수 - 비용의 현실성 및 노코드/로우코드 구분 반영)**:
       - 3편~5편 등 모든 도구(Zapier, Make, HubSpot, Notion 등)를 언급할 때, 반드시 각 도구마다 **[노코드]** 또는 **[로우코드]** 등급 분류 태그를 표기해 주세요.
       - 또한 해당 도구가 **"무료 제공 범위(Free Tier)가 어느 정도인지, 그리고 유료 결제 시 월 얼마의 예상 비용이 발생하는지(예: 월 $20 선)"**를 반드시 구체적으로 1줄 이상 명시하세요. (무작정 비싼 대기업형 도구만 나열하지 말고 Notion DB나 구글 시트 같은 1인 창업가 맞춤형 무료/저가 대안도 함께 제시하세요.)
    7. **(필수 - 6편 및 7편 한국 현실 특화 지침)**:
       - **제6편(운영/재무 자동화):** 단순 해외 QuickBooks 위주 설명은 배제하고, 반드시 **국세청 홈택스 전자세금계산서 연동, 캐시노트(Cashnote), 더존/삼쩜삼** 등 국내 1인 기업가들이 사용하는 로컬 재무/세무 자동화 도구와 연계 방법을 중심으로 논리적으로 작성하세요.
       - **제7편(Python/RPA):** Python 학습 곡선에 대해 현실적 대안(예: '직접 코딩하지 않고 AI 챗봇에게 프롬프트를 줘서 10초 만에 코드를 짜오게 시키기')을 반드시 제시하세요. 아울러 웹 스크래핑을 다룰 시 국내법적 테두리인 **"정보통신망법 제48조(정보통신망 침해) 및 저작권법 무단 수집 이슈"**에 저촉되지 않도록 이용 약관과 로봇 배제 표준(robots.txt)을 준수하라는 강력한 경고 문구를 반드시 삽입하세요.
    8. **(필수 - 참고자료 생성 및 이해충돌 배제)**: 
       - 본문 맨 하단에 본문 주제와 완벽히 부합하고 신뢰할 수 있는 공식 사이트 주소 2개를 아래 HTML 형식으로 제공하세요.
       - 3편을 제외한 타 포스트에서는 Zapier, Make 등 상업적/이해충돌 요소를 완전히 배제하고, 대신 **공신력 있는 비즈니스 연구소, 중소벤처기업부, 한국데이터산업진흥원, W3C 표준 가이드(마케팅일 경우 W3C 대신 마케팅 표준 협회나 신뢰도 높은 연구소 블로그)** 등 객관적 출처만 사용해야 합니다.
       - 본문 내용과 매칭되지 않는 작위적 출처(예: 마케팅 자동화 글에 W3C 웹접근성 링크 넣기)는 절대 금지합니다.
       
       *(예외: 만약 현재 쓰는 글이 **제3편**일 경우, 글 하단의 참고자료 영역에 아래 7개의 목록을 정확히 출력하세요)*
         
       제3편 전용 출처 목록 마크업 규격:
       <ul>
           <li><a href="https://zapier.com/blog/" target="_blank">Zapier 공식 블로그 - Zapier Blog</a></li>
           <li><a href="https://make.com/en/help" target="_blank">Make 공식 가이드 및 도움말 - Make Help Center</a></li>
           <li><a href="https://www.notion.so/help" target="_blank">Notion 사용자 가이드 센터 - Notion Help Center</a></li>
           <li><a href="https://airtable.com/guides" target="_blank">Airtable 공식 활용 가이드 - Airtable Guides</a></li>
           <li><a href="https://bubble.io/blog" target="_blank">Bubble 공식 개발 블로그 - Bubble Blog</a></li>
           <li><a href="https://glideapps.com/blog" target="_blank">Glide 공식 튜토리얼 블로그 - Glide Blog</a></li>
           <li><a href="https://wordpress.org/support/" target="_blank">WordPress 공식 지원 가이드 - WordPress Support</a></li>
       </ul>

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
    작성된 원본 글을 분석하여 구글 검색 봇이 가장 좋아하는 최종 배포 양식으로 정리해 주세요.
    
    원본 제목: "{title}"
    원본 본문(HTML):
    {raw_content}
    
    규칙:
    1. 본문 안에서 어색하거나 AI가 쓴 흔적이 나는 부자연스러운 문맥이 있다면 다듬어 완성도 높은 한국어 텍스트로 보정하세요. (특히 참고자료 링크 HTML 구조가 깨지지 않게 보존하세요.)
    2. 구글 검색 엔진용 140자 내외의 메타 설명(meta description)을 작성하세요.
    3. 글에 태그로 등록할 만한 핵심 키워드 4~5개를 쉼표(,)로 구분해 추출하세요.
    4. 결과를 반드시 아래 JSON 포맷으로 출력하세요. 마크다운 기호(```json)를 포함하지 말고 순수 JSON 문자열만 출력하세요.

    출력 포맷:
    {{
        "final_title": "정돈된 최종 제목",
        "final_content": "보정 완료된 본문 HTML 전체 내용",
        "description": "구글 검색 결과창에 보여질 한 줄 요약 메타설명",
        "tags": ["태그1", "태그2", "태그3", "태그4"]
    }}
    """
    
    response = safe_generate("gemini-2.5-flash", prompt)
    
    try:
        clean_text = response.text.strip()
        if "```json" in clean_text:
            clean_text = clean_text.split("```json")[1].split("```")[0].strip()
        else:
            clean_text = clean_text.replace("```", "").strip()
            
        # JSON 내부에 에러를 유발할 수 있는 이스케이프되지 않은 실제 줄바꿈 문자들 보정
        import re
        # 문장 중간에 들어간 위험한 뉴라인 제어
        clean_text = re.sub(r'\n(?!\s*[{}"\[\]])', '\\n', clean_text)
        
        editor_data = json.loads(clean_text)
        print("-> [Editor] 최종 검수 및 SEO 메타데이터 추출 완료!")
        return editor_data
    except Exception as e:
        print("[ERROR] [Editor] JSON 파싱 오류 발생. 문자열 강제 복구 메커니즘을 가동합니다.")
        # 파싱 오류 발생 시 정교한 정규식으로 복구 시도
        try:
            # 특수 기호 클리닝
            raw_txt = response.text.strip()
            # 메타 설명 추출 목적으로 텍스트 파싱 처리 우회법 적용
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
            print("[CRITICAL] 복구 메커니즘도 실패했습니다. 원본 텍스트:")
            print(response.text)
            raise e

# ==========================================================================
# 워드프레스 배포 모듈 (WordPress Publisher)
# ==========================================================================
def publish_to_wordpress(editor_data):
    if WP_USER == "YOUR_WP_USERNAME" or not WP_USER:
        print("\n[INFO] 워드프레스 정보가 예시 상태입니다. 배포를 생략하고 결과 파일만 로컬에 저장합니다.")
        save_local_file(editor_data)
        return None
        
    print(f"\n[WordPress] '{editor_data['final_title']}' 워드프레스 블로그에 배포 중...")
    
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
            print("SUCCESS 워드프레스에 임시글로 등록되었습니다!")
            return post_info['link']
        else:
            print(f"FAILED 워드프레스 API 응답 코드: {response.status_code}")
            return None
    except Exception as e:
        print(f"FAILED 워드프레스 서버 연결 실패: {str(e)}")
        return None

# 결과 로컬 백업 함수 (독자 플랫폼 posts.json 연동 및 데이터 보존 보장)
def save_local_file(data, filename="posts.json"):
    # posts.json 이라는 메인 데이터베이스 파일에 데이터를 누적함
    posts_filepath = "posts.json"
    
    # 1. 기존 데이터 읽어오기
    existing_posts = []
    if os.path.exists(posts_filepath):
        try:
            with open(posts_filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    existing_posts = json.loads(content)
        except Exception as e:
            print(f"[WARNING] 기존 {posts_filepath} 파일 로드 실패. 새 파일로 갱신합니다. 에러: {e}")

    # 2. 고유 ID 부여 및 구조 변환
    new_id = 1
    if existing_posts:
        new_id = max([p.get('id', 0) for p in existing_posts]) + 1

    # 워드프레스용 최종 에디터 데이터 포맷을 플랫폼 규격에 맞게 매핑
    new_post = {
        "id": new_id,
        "category": data.get("tags", ["비즈니스"])[0] if data.get("tags") else "비즈니스",
        "title": data.get("final_title", "제목 없음"),
        "date": time.strftime("%Y-%m-%d"),
        "author": "솔로프레너",
        "excerpt": data.get("description", "포스트 요약이 없습니다."),
        "content": data.get("final_content", ""),
        "themeColor": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    }

    # 중복 타이틀 체크 후 추가 (중복이 아니면 누적)
    is_duplicate = any(p.get('title') == new_post['title'] for p in existing_posts)
    if not is_duplicate:
        existing_posts.append(new_post)
        print(f"-> [SYSTEM] posts.json에 '{new_post['title']}' 글이 안전하게 영구 기록되었습니다.")
    else:
        # 이미 동일 제목이 있으면 덮어쓰기
        for idx, p in enumerate(existing_posts):
            if p.get('title') == new_post['title']:
                existing_posts[idx] = new_post
                print(f"-> [SYSTEM] posts.json에 기존 '{new_post['title']}' 글을 성공적으로 업데이트했습니다.")
                break

    # 3. 실시간으로 영구 저장 파일 쓰기 (안정성을 위해 임시 파일 작성 후 교체 방식 적용)
    temp_filepath = posts_filepath + ".tmp"
    try:
        with open(temp_filepath, "w", encoding="utf-8") as f:
            json.dump(existing_posts, f, ensure_ascii=False, indent=2)
        
        # 안전하게 원본 파일로 리네임하여 덮어쓰기
        if os.path.exists(posts_filepath):
            os.remove(posts_filepath)
        os.rename(temp_filepath, posts_filepath)
        print(f"LOCAL BACKUP 최종 포스트 전체 데이터가 안전하게 '{posts_filepath}'에 누적 보존되었습니다.")
        
        # 4. GitHub 저장소와 실시간 동기화 (Vercel 자동 배포 트리거)
        sync_to_github()
    except Exception as e:
        print(f"[CRITICAL] posts.json 데이터 보존 실패: {e}")
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)

# 로컬 Git 변경 사항을 자동으로 GitHub에 Commit & Push 하는 함수
def sync_to_github():
    import subprocess
    print("\n[Git Sync] GitHub 저장소에 변경 데이터 동기화 시도 중...")
    try:
        # Git 저장소인지 확인
        if not os.path.exists(".git"):
            print("[Git Sync WARNING] 로컬 폴더에 Git 저장소가 초기화되어 있지 않습니다. 동기화 단계를 건너뜁니다.")
            return
            
        # 1. git add posts.json
        subprocess.run(["git", "add", "posts.json"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 2. git commit -m "Auto-update posts database"
        # 변경 사항이 없을 때는 에러가 나지 않도록 처리하기 위해 check=False로 설정 후 상태 검사
        commit_res = subprocess.run(["git", "commit", "-m", f"Auto-update posts database: {time.strftime('%Y-%m-%d %H:%M:%S')}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if commit_res.returncode == 0:
            print("[Git Sync] 성공적으로 커밋을 만들었습니다.")
        else:
            if "nothing to commit" in commit_res.stdout.decode('utf-8', errors='ignore') or "nothing added" in commit_res.stdout.decode('utf-8', errors='ignore'):
                print("[Git Sync] 변경된 내용이 없어 커밋을 생략합니다.")
                return
            else:
                print(f"[Git Sync WARNING] 커밋 실패: {commit_res.stderr.decode('utf-8', errors='ignore')}")
                return

        # 3. git push
        # 원격 저장소 이름이나 브랜치 확인 후 푸시 실행 (기본 origin main 또는 master)
        push_res = subprocess.run(["git", "push"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("SUCCESS [Git Sync] GitHub로 푸시 완료! 약 30초 내로 Vercel에 반영됩니다.")
    except Exception as e:
        print(f"[Git Sync ERROR] GitHub 동기화 중 오류 발생: {e}")

# ==========================================================================
# 메인 제어 루프 (로컬 단독 테스트 구동용)
# ==========================================================================
def main():
    print("==================================================")
    print("[SYSTEM] 구글 애드센스 승인 타겟 에이전트 시스템 가동 (시리즈 모드)")
    print("==================================================")
    
    try:
        init_gemini()
    except Exception as e:
        print(e)
        return
        
    topic = "1인 기업의 생산성을 극대화하는 IT 자동화 비결"
    series_count = 3
    print(f"[SYSTEM] 주제 결정: {topic} ({series_count}부작)")
        
    # 1. 기획 에이전트 작동
    series_plan = run_planner(topic, series_count)
    
    # 2. 기존 작성 이력 확인 (체크포인트 이어 쓰기 구현)
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

    # 각 시리즈 글 작성 및 순차 배포
    for post in series_plan['posts']:
        part_num = post['part_number']
        post_title_draft = post['title']
        
        # 이미 이 편과 이름이 같거나 비슷한 글이 posts.json에 존재한다면 에이전트 생략(이어하기)
        already_done = any(post_title_draft in t or t in post_title_draft for t in existing_titles)
        if already_done:
            print(f"\n[SKIP] 제 {part_num}편 ('{post_title_draft}')은 이미 이전에 작성 완료되어 보존되어 있습니다. 다음으로 넘어갑니다.")
            continue
            
        raw_content = run_writer(post, part_num, series_count)
        final_post_data = run_editor(post['title'], raw_content)
        
        # 워드프레스 전송 시도
        post_link = publish_to_wordpress(final_post_data)
        
        # 워드프레스에 정상 배포가 되었든 안되었든 간에, '무조건' 로컬 posts.json 에도 실시간 누적하여 데이터 유실을 완전 방어합니다.
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

