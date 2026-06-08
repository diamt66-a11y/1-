import os
import json

with open('run_agents.py', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('def run_planner')
end_idx = content.find('def publish_to_wordpress')

if start_idx != -1 and end_idx != -1:
    new_code = '''def run_planner(topic, series_count=8):
    print(f"\\n[Planner] 확정된 {series_count}부작 블로그 시리즈 기획안 로드 중 (목차 강제 고정)...")
    
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
    
    print(f"\\n[Writer] {title} ({part_number}/{total_parts}) 본문 집필 시작...")
    
    sections_str = ""
    for idx, sec in enumerate(sections):
        sub_title = sec.get('sub_title') or sec.get('title') or f"섹션 {idx+1}"
        key_points = sec.get('key_points') or sec.get('keywords') or []
        sections_str += f"\\n{idx+1}. 소제목: {sub_title}\\n   - 다룰 키워드: {', '.join(key_points)}\\n"
        
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
    print(f"\\n[Editor] {title} 본문 검수 및 SEO 최적화 메타 추출 진행 중...")
    
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
            
        clean_text = re.sub(r'\\n(?!\\s*[{}"\\[\\]])', '\\\\n', clean_text)
        
        editor_data = json.loads(clean_text)
        print("-> [Editor] 최종 검수 및 SEO 메타데이터 추출 완료!")
        return editor_data
    except Exception as e:
        print("[ERROR] [Editor] JSON 파싱 오류 발생. 강제 복구 메커니즘을 가동합니다.")
        try:
            raw_txt = response.text.strip()
            desc_match = re.search(r'"description"\\s*:\\s*"(.*?)"', raw_txt, re.DOTALL)
            title_match = re.search(r'"final_title"\\s*:\\s*"(.*?)"', raw_txt, re.DOTALL)
            content_match = re.search(r'"final_content"\\s*:\\s*"(.*?)"', raw_txt, re.DOTALL)
            
            desc_val = desc_match.group(1).replace('\\n', ' ') if desc_match else "SEO 최적화 포스팅입니다."
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
'''
    
    final_content = content[:start_idx] + new_code + content[end_idx:]
    with open('run_agents.py', 'w', encoding='utf-8') as f:
        f.write(final_content)
    print('Encoding fixed for AI Prompts!')
else:
    print('Target not found')
