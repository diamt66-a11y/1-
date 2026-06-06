import streamlit as st
import time
import json
import run_agents

# ==========================================================================
# UI / 디자인 설정
# ==========================================================================
st.set_page_config(
    page_title="솔로프레너 시리즈 편집 대시보드",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: #2563eb;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #64748b;
        margin-bottom: 2rem;
    }
    .status-card {
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        background-color: #ffffff;
        margin-bottom: 1.5rem;
    }
    .naver-box {
        background-color: #f0fdf4;
        border: 1px solid #16a34a;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================================================
# Session State 초기화
# ==========================================================================
if 'series_title' not in st.session_state:
    st.session_state['series_title'] = ""
if 'generated_posts' not in st.session_state:
    st.session_state['generated_posts'] = []
if 'is_running' not in st.session_state:
    st.session_state['is_running'] = False

# ==========================================================================
# Sidebar 설정 영역
# ==========================================================================
with st.sidebar:
    st.header("⚙️ 시스템 정보 확인")
    st.write("---")
    st.success("🤖 에이전트 준비 완료 (Gemini-2.5-Flash)")
    st.info(f"🌐 워드프레스 주소:\n{run_agents.WP_URL}")
    st.info(f"👤 사용자 계정:\n{run_agents.WP_USER}")
    st.info(f"🇳 네이버 블로그:\nblog.naver.com/agentlabs")
    
    st.write("---")
    if st.button("🔄 대시보드 데이터 초기화"):
        st.session_state['series_title'] = ""
        st.session_state['generated_posts'] = []
        st.session_state['is_running'] = False
        st.rerun()

    st.write("---")
    st.caption("1인 기업 자동 수익 자동화 도구 v2.5")

# ==========================================================================
# Main UI 디자인
# ==========================================================================
st.markdown('<h1 class="main-title">⚡ 솔로프레너 연재 포스팅 에이전트</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">구글 워드프레스 전송과 함께 네이버 블로그에 최적화된 복사 텍스트를 제공하여 최적의 투 트랙(Two-Track) 브랜딩을 돕습니다.</p>', unsafe_allow_html=True)

# 1. 주제 입력 필드
topic_input = st.text_input(
    "✍️ 블로그 글의 큰 대주제를 자유롭게 입력하세요",
    value="1인 기업의 생산성을 극대화하는 IT 자동화 비결",
    placeholder="예: 1인 기업으로 성공하는 블로그 브랜딩 전략"
)

# 2. 연재 편수 조절 슬라이더
series_count = st.slider(
    "📚 몇 부작 시리즈로 쪼개어 연재 포스팅을 발행할까요?",
    min_value=2,
    max_value=8,
    value=8,
    step=1
)

# 에이전트 가동 버튼
if st.button("🚀 에이전트 연재 집필 시작", type="primary"):
    st.session_state['generated_posts'] = []
    st.session_state['series_title'] = ""
    
    status_box = st.empty()
    main_progress = st.progress(0)
    
    try:
        run_agents.init_gemini()
        
        # 1단계: 기획 (Planner)
        status_box.info(f"🤖 Planner가 {series_count}부작 시리즈 목차와 소제목들을 설계 중입니다...")
        main_progress.progress(15)
        
        series_plan = run_agents.run_planner(topic_input, series_count)
        st.session_state['series_title'] = series_plan['series_title']
        
        # 2~3단계: 순차적 집필 및 편집
        for idx, post in enumerate(series_plan['posts']):
            part_num = post['part_number']
            percent_complete = 15 + int((idx / series_count) * 80)
            main_progress.progress(percent_complete)
            
            status_box.info(f"🤖 제 {part_num}편 글 집필 및 SEO 편집 가공 중...")
            
            # Writer로 본문 작성
            raw_content = run_agents.run_writer(post, part_num, series_count)
            
            # Editor로 검수 및 가공
            final_post = run_agents.run_editor(post['title'], raw_content)
            
            # HTML 코드를 네이버 에디터용 일반 가독성 텍스트로 치환하기 위한 가공
            import re
            naver_text = final_post['final_content']
            # 태그들 제거
            naver_text = re.sub(r'<hr\s*/?>', '\n----------------------------------------\n', naver_text)
            naver_text = re.sub(r'<h2>(.*?)</h2>', r'\n\n[소제목] \1\n', naver_text)
            naver_text = re.sub(r'<h3>(.*?)</h3>', r'\n\n[소주제] \1\n', naver_text)
            naver_text = re.sub(r'<li><a href="(.*?)" target="_blank">(.*?)</a></li>', r'• \2 (\1)', naver_text)
            naver_text = re.sub(r'<p>(.*?)</p>', r'\1\n', naver_text)
            naver_text = re.sub(r'<.*?>', '', naver_text)  # 남은 HTML 태그 소거
            naver_text = naver_text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
            
            # 네이버용 글 소개 오프닝 보정 추가
            naver_intro = f"안녕하세요! 1인 기업 IT 자동화 학습 블로그입니다.\n오늘 업로드하는 글은 {st.session_state['series_title']} 시리즈의 제 {part_num}편 포스팅입니다. 1인 창업가로 생존하기 위한 기술 로드맵을 함께 공부하며 마스터해 봅시다.\n\n"
            naver_text = naver_intro + naver_text
            
            # 세션 스테이트에 편집 가능하도록 임시 보관
            st.session_state['generated_posts'].append({
                "part_number": part_num,
                "title": final_post['final_title'],
                "content": final_post['final_content'],
                "naver_content": naver_text.strip(),
                "description": final_post['description'],
                "tags": ", ".join(final_post['tags']),
                "published_link": None
            })
            
            time.sleep(1.5)
            
        main_progress.progress(100)
        status_box.success("🎉 모든 에이전트 집필이 완료되었습니다! 아래 에디터에서 글을 확인하고 다듬어 보세요.")
        st.rerun()
        
    except Exception as e:
        main_progress.progress(0)
        status_box.error(f"❌ 작업 수행 중 시스템 오류 발생: {str(e)}")

# ==========================================================================
# ✍️ 실시간 대시보드 편집 & 송출 제어 렌더링 영역
# ==========================================================================
if st.session_state['generated_posts']:
    st.write("---")
    st.markdown(f"### 📝 '{st.session_state['series_title']}' 시리즈 편집 대기실")
    st.info("💡 팁: 아래 텍스트 상자 안에서 가독성을 높이기 위해 마음껏 줄바꿈(Enter) 및 오타 교정을 진행한 후, 각 편의 [송출] 버튼을 누르세요.")
    
    for idx, post in enumerate(st.session_state['generated_posts']):
        part_num = post['part_number']
        
        with st.container():
            st.markdown(f"#### 📚 제 {part_num}편: {post['title']}")
            
            # 1. 제목 편집 필드
            edited_title = st.text_input(
                f"제 {part_num}편 최종 제목",
                value=post['title'],
                key=f"title_part_{part_num}"
            )
            st.session_state['generated_posts'][idx]['title'] = edited_title
            
            # 2. 본문(HTML) 편집 필드
            edited_content = st.text_area(
                f"제 {part_num}편 본문 HTML 코드 편집창 (구글 워드프레스용)",
                value=post['content'],
                height=300,
                key=f"content_part_{part_num}"
            )
            st.session_state['generated_posts'][idx]['content'] = edited_content
            
            # 3. 검색 요약문 편집 필드
            edited_desc = st.text_area(
                f"제 {part_num}편 구글 검색 요약(Meta Description) 편집",
                value=post['description'],
                height=80,
                key=f"desc_part_{part_num}"
            )
            st.session_state['generated_posts'][idx]['description'] = edited_desc
            
            # 4. 네이버 블로그 발행용 텍스트 상자 (오로지 텍스트 복사용으로 깔끔하게 구성)
            with st.expander(f"🟢 제 {part_num}편 네이버 블로그 포스팅용 복사 텍스트"):
                st.markdown('<div class="naver-box">', unsafe_allow_html=True)
                st.caption("아래 텍스트 상자 내부를 복사하셔서 네이버 스마트에디터에 바로 붙여넣기하세요!")
                st.text_area(
                    "네이버용 본문 (Ctrl + A 후 Ctrl + C로 전체 복사 가능)",
                    value=post['naver_content'],
                    height=250,
                    key=f"naver_part_{part_num}"
                )
                st.markdown(f'<a href="https://blog.naver.com/agentlabs" target="_blank" style="display: inline-block; padding: 0.5rem 1rem; background-color: #2db400; color: white; border-radius: 6px; font-weight: 600; text-decoration: none; font-size: 0.9rem; margin-top: 0.5rem;">네이버 글쓰기 화면으로 이동 ➔</a>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # 배포 상태 출력 및 제어 단추
            if post['published_link']:
                st.markdown(f'<p style="color: #10b981; font-weight: 600;">✓ 구글 워드프레스 전송 완료! <a href="{post["published_link"]}" target="_blank">워드프레스에서 예약/편집하기 ➔</a></p>', unsafe_allow_html=True)
            else:
                col1, col2 = st.columns([3, 7])
                with col1:
                    if st.button(f"📤 제 {part_num}편 워드프레스로 최종 송출", key=f"publish_btn_{part_num}", type="primary"):
                        with st.spinner("워드프레스 서버에 안전하게 업로드 중..."):
                            wp_payload = {
                                "final_title": edited_title,
                                "final_content": edited_content,
                                "description": edited_desc,
                                "tags": [t.strip() for t in post['tags'].split(",") if t.strip()]
                            }
                            
                            post_link = run_agents.publish_to_wordpress(wp_payload)
                            
                            if post_link:
                                st.session_state['generated_posts'][idx]['published_link'] = post_link
                                st.success(f"🎉 제 {part_num}편 송출 완료!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("워드프레스 전송 도중 오류가 발생했습니다. 사이트 연결이나 응용프로그램 비밀번호 설정을 재확인해 주세요.")
            
            st.write("---")
