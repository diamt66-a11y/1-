# -*- coding: utf-8 -*-
import streamlit as st
import time
import json
import run_agents
import os

# ==========================================================================
# UI / 페이지 설정
# ==========================================================================
st.set_page_config(
    page_title="솔로프레너 자동화 콘텐츠 시스템",
    page_icon="🚀",
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
# Sidebar 설정 정보 표시
# ==========================================================================
with st.sidebar:
    st.header("🔧 시스템 정보 확인")
    st.write("---")
    st.success("✅ AI 에이전트 준비 완료 (Gemini-2.5-Flash)")
    st.info(f"🌐 워드프레스 주소:\n{run_agents.WP_URL}")
    st.info(f"👤 사용자 계정:\n{run_agents.WP_USER}")
    st.info(f"📝 네이버 블로그:\nblog.naver.com/agentlabs")

    st.write("---")
    if st.button("🔄 모든 데이터 초기화"):
        st.session_state['series_title'] = ""
        st.session_state['generated_posts'] = []
        st.session_state['is_running'] = False
        st.rerun()

    st.write("---")
    st.caption("1인기업 자동화 시스템 자동화봇 v2.5")

# ==========================================================================
# Main UI 본문
# ==========================================================================
st.markdown('<h1 class="main-title">🚀 솔로프레너 자동화 대시보드</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">워드프레스와 네이버 블로그 투트랙 발행 및 구글 드라이브 자동화 스캔을 통합 관리합니다.</p>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🤖 에이전트 시리즈 생성", "📁 구글 드라이브 스캔 & Vercel 배포", "📝 블로그 게시글 수동 관리"])

# --------------------------------------------------------------------------
# 탭 1: 에이전트 시리즈 생성
# --------------------------------------------------------------------------
with tab1:
    st.markdown("### 자동화 콘텐츠 기획 및 발행")
    
    topic_input = st.text_input(
        "📝 블로그 시리즈 주제를 자유롭게 입력하세요",
        value="1인기업의 수익을 높이는 IT 자동화 전략",
        placeholder="예: 1인기업으로 성공하는 블로그 전략"
    )

    series_count = st.slider("📌 몇 편으로 구성된 시리즈를 생성할까요?", min_value=2, max_value=8, value=8, step=1)

    if st.button("🤖 에이전트 시리즈 작업 시작", type="primary"):
        st.session_state['generated_posts'] = []
        st.session_state['series_title'] = ""
        status_box = st.empty()
        main_progress = st.progress(0)

        try:
            run_agents.init_gemini()
            status_box.info(f"✅ Planner가 {series_count}편 시리즈 주제들을 분석 중입니다...")
            main_progress.progress(15)

            series_plan = run_agents.run_planner(topic_input, series_count)
            st.session_state['series_title'] = series_plan['series_title']

            for idx, post in enumerate(series_plan['posts']):
                part_num = post['part_number']
                percent_complete = 15 + int((idx / series_count) * 80)
                main_progress.progress(percent_complete)
                status_box.info(f"✅ 제{part_num}편 작성 및 SEO 최적화 중..")

                raw_content = run_agents.run_writer(post, part_num, series_count)
                final_post = run_agents.run_editor(post['title'], raw_content)

                import re
                naver_text = final_post['final_content']
                naver_text = re.sub(r'<hr\s*/?>', '\n----------------------------------------\n', naver_text)
                naver_text = re.sub(r'<h2>(.*?)</h2>', r'\n\n[주제] \1\n', naver_text)
                naver_text = re.sub(r'<h3>(.*?)</h3>', r'\n\n[소제목] \1\n', naver_text)
                naver_text = re.sub(r'<li><a href="(.*?)" target="_blank">(.*?)</a></li>', r'▶ \2 (\1)', naver_text)
                naver_text = re.sub(r'<p>(.*?)</p>', r'\1\n', naver_text)
                naver_text = re.sub(r'<.*?>', '', naver_text)
                naver_text = naver_text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')

                naver_intro = f"안녕하세요! 1인기업 IT 자동화 전문 블로그입니다.\n현재 연재하고 있는 {st.session_state['series_title']} 시리즈의 제{part_num}편입니다. 1인기업가로 성공하기 위한 핵심 노하우를 함께 나눠드리니 구독과 응원 부탁드려요!\n\n"
                naver_text = naver_intro + naver_text

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
            status_box.success("🎉 모든 에이전트 작업이 완료되었습니다! 아래에서 확인하시고 수정/발행하세요.")

        except Exception as e:
            main_progress.progress(0)
            status_box.error(f"❌ 작업 실행 중 오류 발생: {str(e)}")

    if st.session_state['generated_posts']:
        st.write("---")
        st.markdown(f"### 📋 '{st.session_state['series_title']}' 시리즈 최종 확인")
        for idx, post in enumerate(st.session_state['generated_posts']):
            part_num = post['part_number']
            with st.container():
                st.markdown(f"#### 📌 제{part_num}편: {post['title']}")
                edited_title = st.text_input(f"제{part_num}편 최종 제목", value=post['title'], key=f"title_part_{part_num}")
                st.session_state['generated_posts'][idx]['title'] = edited_title
                edited_content = st.text_area(f"제{part_num}편 본문 HTML (워드프레스용)", value=post['content'], height=300, key=f"content_part_{part_num}")
                st.session_state['generated_posts'][idx]['content'] = edited_content
                edited_desc = st.text_area(f"제{part_num}편 워드프레스 메타 설명", value=post['description'], height=80, key=f"desc_part_{part_num}")
                st.session_state['generated_posts'][idx]['description'] = edited_desc
                
                with st.expander(f"📄 제{part_num}편 네이버 블로그 글 복사"):
                    st.text_area("네이버용 본문", value=post['naver_content'], height=250, key=f"naver_part_{part_num}")
                
                st.markdown("---")
                st.markdown("##### ✨ AI 내용 맞춤 수정")
                revision_instruction = st.text_input("수정 지시사항 (예: 문체를 부드럽게, 특정 결제 수단 내용 추가)", key=f"revise_input_{part_num}")
                if st.button(f"✨ 제{part_num}편 지시사항 반영하여 다시 쓰기", key=f"revise_btn_{part_num}"):
                    if revision_instruction.strip():
                        with st.spinner("AI가 지시사항을 반영하여 본문을 다시 작성 중입니다..."):
                            try:
                                revised_content = run_agents.run_reviser(post['title'], edited_content, revision_instruction)
                                st.session_state['generated_posts'][idx]['content'] = revised_content
                                
                                import re
                                naver_text = revised_content
                                naver_text = re.sub(r'<hr\s*/?>', '\n----------------------------------------\n', naver_text)
                                naver_text = re.sub(r'<h2>(.*?)</h2>', r'\n\n[주제] \1\n', naver_text)
                                naver_text = re.sub(r'<h3>(.*?)</h3>', r'\n\n[소제목] \1\n', naver_text)
                                naver_text = re.sub(r'<li><a href="(.*?)" target="_blank">(.*?)</a></li>', r'▶ \2 (\1)', naver_text)
                                naver_text = re.sub(r'<p>(.*?)</p>', r'\1\n', naver_text)
                                naver_text = re.sub(r'<.*?>', '', naver_text)
                                naver_text = naver_text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
                                
                                naver_intro = f"안녕하세요! 1인기업 IT 자동화 전문 블로그입니다.\n현재 연재하고 있는 {st.session_state.get('series_title', '')} 시리즈의 제{part_num}편입니다. 1인기업가로 성공하기 위한 핵심 노하우를 함께 나눠드리니 구독과 응원 부탁드려요!\n\n"
                                st.session_state['generated_posts'][idx]['naver_content'] = naver_intro + naver_text.strip()
                                
                                st.success("✅ AI 수정이 완료되었습니다!")
                                time.sleep(1)
                                st.rerun()
                            except Exception as e:
                                st.error(f"AI 수정 중 오류 발생: {str(e)}")
                    else:
                        st.warning("수정 지시사항을 입력해주세요.")
                
                if post['published_link']:
                    st.success(f"✅ 워드프레스 발행 완료: {post['published_link']}")
                else:
                    if st.button(f"📤 제{part_num}편 워드프레스로 최종 발행", key=f"publish_btn_{part_num}", type="primary"):
                        with st.spinner("발행 중..."):
                            wp_payload = {
                                "final_title": edited_title,
                                "final_content": edited_content,
                                "description": edited_desc,
                                "tags": [t.strip() for t in post['tags'].split(",") if t.strip()]
                            }
                            post_link = run_agents.publish_to_wordpress(wp_payload)
                            if post_link:
                                st.session_state['generated_posts'][idx]['published_link'] = post_link
                                st.rerun()
                            else:
                                st.error("워드프레스 연결 오류")

# --------------------------------------------------------------------------
# 탭 2: 구글 드라이브 스캔 & Vercel 배포
# --------------------------------------------------------------------------
with tab2:
    st.markdown("### 📁 실시간 구글 드라이브 스캔 중계")
    st.info("구글 드라이브에 저장된 새로운 메모나 초안을 모니터링하고 Vercel로 자동 배포합니다.")
    
    if st.button("🚀 구글 드라이브 스캔 시작", type="primary"):
        with st.status("구글 드라이브 스캔 중...", expanded=True) as status:
            st.write("1. G:\내 드라이브 경로 모니터링 시작...")
            time.sleep(1)
            st.write("2. 최신 .txt 및 .md 메모 파일 탐색 중...")
            time.sleep(1)
            st.write("3. AI 분류 및 폴더 이동 로직 실행 (진행 중)...")
            
            try:
                # 백그라운드 함수 모방/실행
                run_agents.scan_and_process_google_drive()
                status.update(label="스캔 완료!", state="complete", expanded=False)
                st.success("✅ 구글 드라이브 최신 자료 스캔이 성공적으로 완료되었습니다.")
            except Exception as e:
                status.update(label="스캔 중 오류 발생", state="error")
                st.error(f"오류: {str(e)}")

    st.markdown("---")
    st.markdown("### 🌐 Vercel Git Sync 사용자 편의 및 안전장치")
    st.write("클릭 한 번으로 깃허브(GitHub) 동기화 및 Vercel 실시간 배포가 진행됩니다.")
    if st.button("🔄 Vercel Git Sync 배포하기"):
        with st.spinner("GitHub 연동 및 배포 진행 중..."):
            try:
                run_agents.sync_to_github()
                st.success("🎉 GitHub PUSH 및 Vercel 배포가 성공적으로 예약되었습니다! (약 1~2분 후 라이브 사이트에 반영됩니다)")
            except Exception as e:
                st.error(f"동기화 중 오류 발생: {str(e)}")
            st.markdown("[Vercel 라이브 사이트 바로가기](https://vercel.com) 🚀")

# --------------------------------------------------------------------------
# 탭 3: 블로그 게시글 수동 관리
# --------------------------------------------------------------------------
with tab3:
    st.markdown("### 📝 블로그 게시글 수동 관리 (안전장치 강화)")
    st.info("발행된 콘텐츠 목록을 확인하고 불필요한 글을 삭제합니다. (실수 방지 안전장치 적용)")
    
    posts_path = "posts.json"
    if os.path.exists(posts_path):
        try:
            with open(posts_path, "r", encoding="utf-8") as f:
                posts_data = json.load(f)
                
            if posts_data:
                for p_idx, post_item in enumerate(posts_data):
                    with st.expander(f"[{post_item.get('category', '미분류')}] {post_item.get('title', '제목 없음')}"):
                        st.write(f"**날짜**: {post_item.get('date', '')}")
                        st.write(f"**작성자**: {post_item.get('author', '')}")
                        st.markdown("**요약**:")
                        st.write(post_item.get('excerpt', ''))
                        
                        st.warning("⚠️ 이 글을 삭제하시겠습니까?")
                        confirm_del = st.checkbox(f"네, 삭제에 동의합니다. (ID: {post_item.get('id')})", key=f"del_check_{p_idx}")
                        if st.button("🗑️ 선택한 글 영구 삭제", key=f"del_btn_{p_idx}", disabled=not confirm_del):
                            posts_data.pop(p_idx)
                            with open(posts_path, "w", encoding="utf-8") as wf:
                                json.dump(posts_data, wf, indent=2, ensure_ascii=False)
                            st.success("✅ 삭제 완료되었습니다.")
                            time.sleep(1)
                            st.rerun()
            else:
                st.write("저장된 게시글이 없습니다.")
        except Exception as e:
            st.error(f"데이터를 읽는 중 오류가 발생했습니다: {str(e)}")
    else:
        st.write("posts.json 파일을 찾을 수 없습니다.")
