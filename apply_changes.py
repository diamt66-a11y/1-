import os

# 1. Modify run_agents.py
with open('run_agents.py', 'r', encoding='utf-8') as f:
    text = f.read()

# determine_category_folder replacement
old_cat = '''def determine_category_folder(filename, content):
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
        print(f"[AI Category WARNING] 분류 실패로 기본폴더(일반_메모)를 부여합니다. 에러: {e}")
        return "일반_메모"'''

new_cat = '''def determine_category_folder(filename, content):
    prompt = f"""
    당신은 구글 드라이브 파일 정리 비서입니다.
    제시된 텍스트 내용 및 파일명을 분석하여, 이 파일의 주제에 가장 잘 어울리는 폴더명을 한글로 결정하세요.
    
    [분류 가이드]
    - IT 자동화 관련: IT 자동화 기획
    - 비즈니스 전략, 1인 창업 관련: 비즈니스 전략
    - 애드센스, 수익화 관련: 디지털 수익화
    - 기타 일반 주제, 개인 메모, 낙서, 철학, 에세이: 기타 가이드
    
    [대상 문서]
    파일명: {filename}
    본문 내용 일부:
    {content[:1000]}
    
    [출력 규칙]
    반드시 위에 나열된 4가지 폴더명("IT 자동화 기획", "비즈니스 전략", "디지털 수익화", "기타 가이드") 중 하나만 응답하세요. 다른 부가 설명은 절대 하지 마세요.
    """
    try:
        response = safe_generate("gemini-2.5-flash", prompt)
        result = response.text.strip().replace("`", "").replace('"', "").strip()
        valid_folders = ["IT 자동화 기획", "비즈니스 전략", "디지털 수익화", "기타 가이드"]
        for vf in valid_folders:
            if vf in result:
                return vf
        return "기타 가이드"
    except Exception as e:
        print(f"[AI Category WARNING] 분류 실패로 기본 카테고리(기타 가이드)를 부여합니다. 에러: {e}")
        return "기타 가이드"'''

text = text.replace(old_cat, new_cat)

# process_drive_file_to_post signature and prompt
old_writer = '''def process_drive_file_to_post(file_path, raw_content):
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
    """'''

new_writer = '''def process_drive_file_to_post(file_path, raw_content, category):
    filename = os.path.basename(file_path)
    print(f"[AI Writer] '{filename}' 원본 소스를 바탕으로 아티클 집필 재가공 중... (카테고리: {category})")
    
    if category == "기타 가이드":
        style_guide = """
    [집필 스타일 가이드 - 에세이/가이드]
    1. 이 글은 IT 자동화나 기술 도구를 설명하는 글이 아닙니다. 자연스러운 일반 정보, 에세이, 철학 등의 내용을 다룹니다.
    2. 본문 안에 억지로 [노코드], [로우코드], 활용 툴, 예상 비용 등을 절대 넣지 마세요.
    3. 가독성을 극대화하기 위해 2~3개 문단마다 HTML <h2> 또는 <h3> 소제목으로 아티클을 정갈하게 분할하세요.
    4. 핵심 장점이나 워크플로우 단계는 불릿 포인트(Bullet point) 목록을 사용해 시각적으로 일목요연하게 정리하세요.
        """
    else:
        style_guide = """
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
        """
        
    prompt = f"""
    당신은 시스템 자동화와 수익 다각화를 연구하는 1인 기업가이자 비즈니스 에디터인 '솔로프레너'입니다.
    제시된 구글 드라이브(NotebookLM) 소스 문서를 읽고, 독자들에게 실질적인 실행 기회를 주는 고품질 블로그 아티클을 완성해 주세요.
    
    [원본 정보 소스]
    {raw_content}
    {style_guide}
    """'''

text = text.replace(old_writer, new_writer)

old_eval = '''            if is_valuable:
                print(f"-> [AI 판별] SUCCESS: '{basename}' 은 블로그 발행 가치가 높은 양질의 지식 소스로 확인되었습니다!")
                
                # 2. AI 자동 집필 및 Vercel/워드프레스 배포 파이프라인 개시
                process_drive_file_to_post(file_path, content)'''

new_eval = '''            if is_valuable:
                print(f"-> [AI 판별] SUCCESS: '{basename}' 은 블로그 발행 가치가 높은 양질의 지식 소스로 확인되었습니다!")
                
                # 2. AI 자동 집필 및 Vercel/워드프레스 배포 파이프라인 개시
                category = determine_category_folder(basename, content)
                process_drive_file_to_post(file_path, content, category)'''

text = text.replace(old_eval, new_eval)

old_run_editor = '''        # Editor Agent를 통해 SEO 최적화 및 최종 형식 교정
        editor_data = run_editor(title_temp, raw_html)'''

new_run_editor = '''        # Editor Agent를 통해 SEO 최적화 및 최종 형식 교정
        editor_data = run_editor(title_temp, raw_html)
        editor_data["category"] = category'''

text = text.replace(old_run_editor, new_run_editor)

with open('run_agents.py', 'w', encoding='utf-8') as f:
    f.write(text)

# 2. Modify dashboard.py
with open('dashboard.py', 'r', encoding='utf-8') as f:
    dtext = f.read()

# Add Category widget in tab 3
old_tab3 = '''with tab3:
    st.markdown("### 🛠️ 블로그 게시글 수동 관리 (posts.json)")
    
    if os.path.exists("posts.json"):'''

new_tab3 = '''with tab3:
    st.markdown("### 🛠️ 블로그 게시글 수동 관리 (posts.json)")
    
    if os.path.exists("posts.json"):
        import collections
        cat_counts = collections.Counter([p.get('category', '기타') for p in generated_posts])
        st.markdown("**📊 분류별 포스트 통계:** " + " | ".join([f"{k}: {v}개" for k, v in cat_counts.items()]))
        st.markdown("---")'''

dtext = dtext.replace(old_tab3, new_tab3)

# Add category selectbox inside edit modal
old_edit = '''                new_title = st.text_input("제목 수정", post.get("title", ""))
                new_desc = st.text_area("메타 설명 수정", post.get("description", ""))
                new_tags = st.text_input("태그 수정 (쉼표로 구분)", ", ".join(post.get("tags", [])))
                new_content = st.text_area("본문 HTML 수정", post.get("content", ""), height=300)'''

new_edit = '''                new_title = st.text_input("제목 수정", post.get("title", ""))
                cat_options = ["비즈니스 전략", "디지털 수익화", "IT 자동화 기획", "기타 가이드"]
                current_cat = post.get("category", "비즈니스 전략")
                if current_cat not in cat_options: current_cat = "비즈니스 전략"
                new_category = st.selectbox("카테고리 수정", cat_options, index=cat_options.index(current_cat))
                new_desc = st.text_area("메타 설명 수정", post.get("description", ""))
                new_tags = st.text_input("태그 수정 (쉼표로 구분)", ", ".join(post.get("tags", [])))
                new_content = st.text_area("본문 HTML 수정", post.get("content", ""), height=300)'''

dtext = dtext.replace(old_edit, new_edit)

old_save = '''                if st.button("저장하기", key=f"save_edit_{i}"):
                    post["title"] = new_title
                    post["description"] = new_desc'''

new_save = '''                if st.button("저장하기", key=f"save_edit_{i}"):
                    post["title"] = new_title
                    post["category"] = new_category
                    post["description"] = new_desc'''

dtext = dtext.replace(old_save, new_save)

with open('dashboard.py', 'w', encoding='utf-8') as f:
    f.write(dtext)

print("Scripts updated successfully.")
