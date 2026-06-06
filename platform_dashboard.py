import streamlit as st
import time

# ==========================================================================
# 1. UI 및 스타일링 설정
# ==========================================================================
st.set_page_config(
    page_title="1인 기업 IT 자동화 플랫폼 구축 가이드 대시보드",
    page_icon="🏗️",
    layout="wide"
)

st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: #1e3a8a;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #475569;
        margin-bottom: 2rem;
    }
    .platform-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        font-size: 0.75rem;
        font-weight: 700;
        border-radius: 9999px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .badge-wordpress { background-color: #dbeafe; color: #1e40af; }
    .badge-naver { background-color: #dcfce7; color: #166534; }
    .badge-airtable { background-color: #ffedd5; color: #9a3412; }
    .badge-streamlit { background-color: #fce7f3; color: #9d174d; }
</style>
""", unsafe_allow_html=True)

# Session State 초기화 (구축 체크리스트 상태 유지용)
if 'checklist' not in st.session_state:
    st.session_state['checklist'] = {
        "wp_install": False,
        "wp_adsense": False,
        "naver_blog": False,
        "airtable_schema": False,
        "streamlit_deploy": False,
        "email_signup": False
    }

# ==========================================================================
# 2. 메인 화면 타이틀
# ==========================================================================
st.markdown('<h1 class="main-title">🏗️ 1인 기업 IT 자동화 플랫폼 설계 대시보드</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">이론을 넘어 실전 학습 플랫폼을 연동하고 구축 현황을 관리하는 1인 창업가 전용 워크스페이스입니다.</p>', unsafe_allow_html=True)

# ==========================================================================
# 3. 레이아웃 분할
# ==========================================================================
col_left, col_right = st.columns([6, 4])

with col_left:
    st.markdown("### 🌐 플랫폼 트래픽 및 데이터 흐름도")
    
    # Mermaid 다이어그램 렌더링
    st.markdown("""
    ```mermaid
    graph TD
        A[독자 유입: 네이버 블로그 / SNS] -->|링크 클릭| B(워드프레스 메인 블로그)
        B -->|구글 애드센스 광고 노출| B1[수익 자동화]
        B -->|이론 & 가이드 학습| B2[8부작 시리즈 포스팅]
        B -->|실습 템플릿 복제| C[Airtable / Notion 실습 DB]
        B -->|직접 테스트| D[Streamlit 실습 대시보드]
        D -->|에러 질문 및 커뮤니티 소통| E[네이버 카페 / 커뮤니티]
    ```
    """)
    
    st.markdown("---")
    
    st.markdown("### 🧰 핵심 플랫폼별 역할 및 연동 노하우")
    
    # 워드프레스
    with st.container():
        st.markdown(
            '<div class="platform-card">'
            '<span class="badge badge-wordpress">WordPress</span>'
            '<h4>📝 메인 허브 & 수익화 기지</h4>'
            '<p>애드센스 광고를 탑재하고 신뢰도 높은 기술/자동화 튜토리얼을 축적합니다. SEO 최적화된 글을 통해 유기적인 검색 방문자를 자석처럼 끌어당기는 역할을 합니다.</p>'
            '<strong>🔑 연동 꿀팁:</strong> REST API를 활성화하여 에이전트 및 외부 툴에서 자동으로 임시글을 밀어 넣을 수 있도록 구성하세요.'
            '</div>',
            unsafe_allow_html=True
        )

    # 네이버
    with st.container():
        st.markdown(
            '<div class="platform-card">'
            '<span class="badge badge-naver">Naver Blog</span>'
            '<h4>🟢 트래픽 부스터 & 초기 확산</h4>'
            '<p>네이버는 국내 검색 점유율이 가장 높아 이웃 소통과 빠른 트래픽 획득에 유리합니다. 글 요약이나 실습 후기 등을 올려 자연스럽게 워드프레스로 유입시킵니다.</p>'
            '<strong>🔑 연동 꿀팁:</strong> 네이버 스마트에디터에 바로 붙여넣을 수 있도록 이모지, 아코디언, 특수 태그가 클리닝된 본문을 활용하세요.'
            '</div>',
            unsafe_allow_html=True
        )

    # 에어테이블
    with st.container():
        st.markdown(
            '<div class="platform-card">'
            '<span class="badge badge-airtable">Airtable / Notion</span>'
            '<h4>📊 실습용 가상 데이터베이스</h4>'
            '<p>독자들이 복사해서 바로 쓸 수 있는 템플릿을 제공하고, 데이터 수집/가공 실습을 진행할 때 무료 데이터베이스 역할을 담당합니다.</p>'
            '<strong>🔑 연동 꿀팁:</strong> "Base share link"를 활성화하여 독자들이 클릭 한 번으로 본인의 워크스페이스로 데이터를 복제해 갈 수 있게 유도하세요.'
            '</div>',
            unsafe_allow_html=True
        )

    # 스트림릿
    with st.container():
        st.markdown(
            '<div class="platform-card">'
            '<span class="badge badge-streamlit">Streamlit / Glide</span>'
            '<h4>⚡ 인터랙티브 프로토타입 앱</h4>'
            '<p>파이썬 또는 노코드 툴로 빠르게 만드는 독자 실습용 모니터링 대시보드입니다. 눈으로 확인하는 재미를 주어 독자 이탈을 막습니다.</p>'
            '<strong>🔑 연동 꿀팁:</strong> Streamlit Cloud를 활용하면 깃허브 레포지토리와 연동하여 몇 초 만에 무료 웹 도메인으로 배포할 수 있습니다.'
            '</div>',
            unsafe_allow_html=True
        )

with col_right:
    st.markdown("### 🎯 실습 플랫폼 구축 체크리스트")
    st.write("나만의 자동화 학습 플랫폼을 완성해 나가는 진행 상태를 점검해 보세요.")
    
    # 인터랙티브 체크박스
    wp_install = st.checkbox("WordPress 블로그 개설 및 호스팅 연결 완료", value=st.session_state['checklist']['wp_install'])
    wp_adsense = st.checkbox("구글 애드센스 승인 신청 또는 광고 코드 삽입", value=st.session_state['checklist']['wp_adsense'])
    naver_blog = st.checkbox("네이버 브랜딩 블로그 개설 및 첫 글 등록", value=st.session_state['checklist']['naver_blog'])
    airtable_schema = st.checkbox("Airtable 실습용 가상 DB 테이블 설계", value=st.session_state['checklist']['airtable_schema'])
    streamlit_deploy = st.checkbox("Streamlit 대시보드/앱 로컬 서버 가동 및 확인", value=st.session_state['checklist']['streamlit_deploy'])
    email_signup = st.checkbox("리드 획득용 이메일 구독 폼 및 마그넷 설계", value=st.session_state['checklist']['email_signup'])
    
    # 상태 업데이트
    st.session_state['checklist'] = {
        "wp_install": wp_install,
        "wp_adsense": wp_adsense,
        "naver_blog": naver_blog,
        "airtable_schema": airtable_schema,
        "streamlit_deploy": streamlit_deploy,
        "email_signup": email_signup
    }
    
    # 진척률 계산 및 시각화
    completed_tasks = sum(st.session_state['checklist'].values())
    total_tasks = len(st.session_state['checklist'])
    progress_percent = int((completed_tasks / total_tasks) * 100)
    
    st.markdown("---")
    st.markdown(f"**🏗️ 플랫폼 완성도: `{progress_percent}%`**")
    st.progress(progress_percent / 100.0)
    
    if progress_percent == 100:
        st.balloons()
        st.success("🎉 축하합니다! 1인 기업 자동화 학습 및 수익화 플랫폼 구축 준비가 모두 끝났습니다! 이제 본격적으로 트래픽을 모아보세요.")
    elif progress_percent >= 50:
        st.info("👍 아주 잘하고 계십니다! 핵심 기능들이 절반 이상 연결되었어요.")
    else:
        st.warning("🧗 이제 시작입니다! 차근차근 체크리스트를 달성하며 플랫폼을 구축해 보아요.")
        
    st.write("---")
    st.markdown("### 📅 3단계 구축 실행 가이드")
    
    with st.expander("1단계: 콘텐츠 빌드업 (콘텐츠 허브 구축)"):
        st.write("""
        - **목표:** 검색 방문자가 들어와 학습할 가치가 있는 8부작 시리즈 포스팅 발행.
        - **액션:** 지금 구동 중인 대시보드(`dashboard.py`)를 통해 시리즈를 생성하고 워드프레스에 draft(임시글)로 송출하여 예약 세팅하세요.
        """)
        
    with st.expander("2단계: 리드 마그넷 제공 (잠재 고객 락인)"):
        st.write("""
        - **목표:** 방문자가 일회성으로 나가버리지 않도록 이메일 구독자 정보 수집.
        - **액션:** 에어테이블 실습 템플릿 주소를 공개하고, '추가 고급 자동화 소스코드'를 무료로 받기 위해 이메일을 입력하도록 폼을 연동하세요.
        """)
        
    with st.expander("3단계: 실습 앱 배포 (체험형 브랜딩)"):
        st.write("""
        - **목표:** 독자가 직접 실습하고 신뢰를 쌓을 수 있는 공간 배포.
        - **액션:** Streamlit이나 Glide 웹앱 링크를 글 내부 배너로 노출하여 흥미를 유발하세요.
        """)

    st.write("---")
    st.markdown("### 🕒 실습 참고: 업무 목록화 및 타임 트래킹 가이드 인포그래픽")
    st.image(
        r"C:\Users\diamt\.gemini\antigravity\brain\934e1b88-24dc-4d4d-ba25-e7670d7f1d11\time_tracking_infographic_1780739970065.png",
        caption="1인 기업 생산성 극대화를 위한 타임 트래킹 마스터클래스 인포그래픽",
        use_container_width=True
    )
    
    st.write("---")
    st.caption("1인 기업 IT 자동화 가이드 v1.1")
