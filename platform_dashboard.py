# -*- coding: utf-8 -*-
import streamlit as st
import time

# ==========================================================================
# 1. UI 및 앱 설정
# ==========================================================================
st.set_page_config(
    page_title="1인기업 IT 자동화 플라이휠 구축 가이드",
    page_icon="⚙️",
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
    .legal-card {
        background-color: #fef2f2;
        border: 1px solid #ef4444;
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
    .badge-legal { background-color: #fee2e2; color: #991b1b; }
</style>
""", unsafe_allow_html=True)

# Session State 초기화
if 'checklist' not in st.session_state:
    st.session_state['checklist'] = {
        "wp_install": False,
        "wp_adsense": False,
        "naver_blog": False,
        "airtable_schema": False,
        "streamlit_deploy": False,
        "email_signup": False,
        "legal_terms": False,
        "legal_privacy": False
    }

# ==========================================================================
# 2. 메인 화면 타이틀
# ==========================================================================
st.markdown('<h1 class="main-title">⚙️ 1인기업 IT 자동화 플라이휠 설계 대시보드</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">이론을 넘어 실전 학습 플라이휠을 연동하고 구축 현황을 관리하는 1인 창업가 전용 워크스페이스입니다.</p>', unsafe_allow_html=True)

# ==========================================================================
# 3. 레이아웃 분할
# ==========================================================================
col_left, col_right = st.columns([6, 4])

with col_left:
    st.markdown("### 🗺️ 핵심 플랫폼별 역할 및 연동 인프라")
    
    # 워드프레스
    with st.container():
        st.markdown(
            '<div class="platform-card">'
            '<span class="badge badge-wordpress">WordPress</span>'
            '<h4>📝 메인 허브 & 수익화 기지</h4>'
            '<p>애드센스 광고를 탑재하고 신뢰도 높은 기술/자동화 튜토리얼을 축적합니다. SEO 최적화된 글을 통해 유기적인 검색 방문자를 확보합니다.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    # 네이버
    with st.container():
        st.markdown(
            '<div class="platform-card">'
            '<span class="badge badge-naver">Naver Blog</span>'
            '<h4>🟢 트래픽 부스터 & 초기 확산</h4>'
            '<p>네이버는 국내 검색 점유율이 높아 빠른 트래픽 획득에 유리합니다. 워드프레스로 유입시키는 징검다리 역할을 합니다.</p>'
            '</div>',
            unsafe_allow_html=True
        )
        
    st.markdown("---")
    st.markdown("### ⚠️ 한국형 규제 환경 및 법적 필수 사항 (중요)")
    with st.container():
        st.markdown(
            '<div class="legal-card">'
            '<span class="badge badge-legal">Legal Risk & Compliance</span>'
            '<h4>🚨 솔로프레너 필수 준수 법적 리스크</h4>'
            '<ul>'
            '<li><strong>표시광고법 위반 주의:</strong> 과장 광고, 허위 수익 인증 등은 공정거래위원회 제재 대상입니다.</li>'
            '<li><strong>전자상거래법상 청약철회:</strong> 디지털 상품(PDF, 템플릿) 판매 시에도 환불 규정과 청약철회 의무를 명확히 고지해야 합니다.</li>'
            '</ul>'
            '<h4>🔗 참고 및 추가 확인 URL (2026-06-07 기준 유효)</h4>'
            '<ul>'
            '<li><a href="https://stripe.com/pricing" target="_blank">Stripe(글로벌 결제) 최신 수수료 정책</a></li>'
            '<li><a href="https://www.tosspayments.com/support" target="_blank">토스페이먼츠(국내 결제) 가이드</a></li>'
            '<li><a href="https://www.privacy.go.kr" target="_blank">개인정보보호위원회 - 개인정보보호법 가이드</a></li>'
            '<li><a href="https://www.ftc.go.kr" target="_blank">공정거래위원회 - 표시·광고의 공정화에 관한 법률</a></li>'
            '<li><a href="https://www.make.com/en/pricing" target="_blank">Make.com(자동화 툴) 가격 정책</a></li>'
            '</ul>'
            '</div>',
            unsafe_allow_html=True
        )

with col_right:
    st.markdown("### ✅ 구축 체크리스트 및 법적 서류")
    
    # 인터랙티브 체크박스
    st.write("**[ 시스템 구축 ]**")
    wp_install = st.checkbox("WordPress 블로그 개설 및 호스팅 연결", value=st.session_state['checklist']['wp_install'])
    wp_adsense = st.checkbox("구글 애드센스 승인 및 광고 세팅", value=st.session_state['checklist']['wp_adsense'])
    naver_blog = st.checkbox("네이버 블로그 개설 및 세팅", value=st.session_state['checklist']['naver_blog'])
    
    st.write("**[ 법적 필수 서류 템플릿 ]**")
    legal_terms = st.checkbox("이용약관 및 전자상거래 환불/정산 확인서 작성", value=st.session_state['checklist']['legal_terms'])
    legal_privacy = st.checkbox("개인정보 처리방침 제정 및 하단 링크 배치", value=st.session_state['checklist']['legal_privacy'])
    
    # 상태 업데이트
    st.session_state['checklist'].update({
        "wp_install": wp_install, "wp_adsense": wp_adsense, "naver_blog": naver_blog,
        "legal_terms": legal_terms, "legal_privacy": legal_privacy
    })
    
    # 진척도
    completed_tasks = sum(st.session_state['checklist'].values())
    total_tasks = len(st.session_state['checklist'])
    progress_percent = int((completed_tasks / total_tasks) * 100)
    
    st.markdown("---")
    st.markdown(f"**🚀 자동화 및 리스크 대비 완성도: `{progress_percent}%`**")
    st.progress(progress_percent / 100.0)
    
    if progress_percent == 100:
        st.success("🎉 완벽합니다! 시스템 구축 및 법적 리스크 대비가 완료되었습니다.")
    elif progress_percent >= 50:
        st.info("💡 절반 이상 완료되었습니다. 남은 법적 규제 항목을 꼭 챙기세요.")
    else:
        st.warning("⚠️ 아직 초기 단계입니다. 리스크 예방을 위해 체크리스트를 달성하세요.")

    st.write("---")
    st.caption("1인기업 IT 자동화 가이드 v2.0 (Compliance Applied)")
