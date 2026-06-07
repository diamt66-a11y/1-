import streamlit as st
import time

# ==========================================================================
# 1. UI 諛??ㅽ??쇰쭅 ?ㅼ젙
# ==========================================================================
st.set_page_config(
    page_title="1??湲곗뾽 IT ?먮룞???뚮옯??援ъ텞 媛?대뱶 ??쒕낫??,
    page_icon="?룛截?,
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

# Session State 珥덇린??(援ъ텞 泥댄겕由ъ뒪???곹깭 ?좎???
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
# 2. 硫붿씤 ?붾㈃ ??댄?
# ==========================================================================
st.markdown('<h1 class="main-title">?룛截?1??湲곗뾽 IT ?먮룞???뚮옯???ㅺ퀎 ??쒕낫??/h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">?대줎???섏뼱 ?ㅼ쟾 ?숈뒿 ?뚮옯?쇱쓣 ?곕룞?섍퀬 援ъ텞 ?꾪솴??愿由ы븯??1??李쎌뾽媛 ?꾩슜 ?뚰겕?ㅽ럹?댁뒪?낅땲??</p>', unsafe_allow_html=True)

# ==========================================================================
# 3. ?덉씠?꾩썐 遺꾪븷
# ==========================================================================
col_left, col_right = st.columns([6, 4])

with col_left:
    st.markdown("### ?뙋 ?뚮옯???몃옒??諛??곗씠???먮쫫??)
    
    # Mermaid ?ㅼ씠?닿렇???뚮뜑留?
    st.markdown("""
    ```mermaid
    graph TD
        A[?낆옄 ?좎엯: ?ㅼ씠踰?釉붾줈洹?/ SNS] -->|留곹겕 ?대┃| B(?뚮뱶?꾨젅??硫붿씤 釉붾줈洹?
        B -->|援ш? ?좊뱶?쇱뒪 愿묎퀬 ?몄텧| B1[?섏씡 ?먮룞??
        B -->|?대줎 & 媛?대뱶 ?숈뒿| B2[8遺???쒕━利??ъ뒪??
        B -->|?ㅼ뒿 ?쒗뵆由?蹂듭젣| C[Airtable / Notion ?ㅼ뒿 DB]
        B -->|吏곸젒 ?뚯뒪?? D[Streamlit ?ㅼ뒿 ??쒕낫??
        D -->|?먮윭 吏덈Ц 諛?而ㅻ??덊떚 ?뚰넻| E[?ㅼ씠踰?移댄럹 / 而ㅻ??덊떚]
    ```
    """)
    
    st.markdown("---")
    
    st.markdown("### ?㎞ ?듭떖 ?뚮옯?쇰퀎 ??븷 諛??곕룞 ?명븯??)
    
    # ?뚮뱶?꾨젅??
    with st.container():
        st.markdown(
            '<div class="platform-card">'
            '<span class="badge badge-wordpress">WordPress</span>'
            '<h4>?뱷 硫붿씤 ?덈툕 & ?섏씡??湲곗?</h4>'
            '<p>?좊뱶?쇱뒪 愿묎퀬瑜??묒옱?섍퀬 ?좊ː???믪? 湲곗닠/?먮룞???쒗넗由ъ뼹??異뺤쟻?⑸땲?? SEO 理쒖쟻?붾맂 湲???듯빐 ?좉린?곸씤 寃??諛⑸Ц?먮? ?먯꽍泥섎읆 ?뚯뼱?밴린????븷???⑸땲??</p>'
            '<strong>?뵎 ?곕룞 轅??</strong> REST API瑜??쒖꽦?뷀븯???먯씠?꾪듃 諛??몃? ?댁뿉???먮룞?쇰줈 ?꾩떆湲??諛???ｌ쓣 ???덈룄濡?援ъ꽦?섏꽭??'
            '</div>',
            unsafe_allow_html=True
        )

    # ?ㅼ씠踰?
    with st.container():
        st.markdown(
            '<div class="platform-card">'
            '<span class="badge badge-naver">Naver Blog</span>'
            '<h4>?윟 ?몃옒??遺?ㅽ꽣 & 珥덇린 ?뺤궛</h4>'
            '<p>?ㅼ씠踰꾨뒗 援?궡 寃???먯쑀?⑥씠 媛???믪븘 ?댁썐 ?뚰넻怨?鍮좊Ⅸ ?몃옒???띾뱷???좊━?⑸땲?? 湲 ?붿빟?대굹 ?ㅼ뒿 ?꾧린 ?깆쓣 ?щ젮 ?먯뿰?ㅻ읇寃??뚮뱶?꾨젅?ㅻ줈 ?좎엯?쒗궢?덈떎.</p>'
            '<strong>?뵎 ?곕룞 轅??</strong> ?ㅼ씠踰??ㅻ쭏?몄뿉?뷀꽣??諛붾줈 遺숈뿬?ｌ쓣 ???덈룄濡??대え吏, ?꾩퐫?붿뼵, ?뱀닔 ?쒓렇媛 ?대━?앸맂 蹂몃Ц???쒖슜?섏꽭??'
            '</div>',
            unsafe_allow_html=True
        )

    # ?먯뼱?뚯씠釉?
    with st.container():
        st.markdown(
            '<div class="platform-card">'
            '<span class="badge badge-airtable">Airtable / Notion</span>'
            '<h4>?뱤 ?ㅼ뒿??媛???곗씠?곕쿋?댁뒪</h4>'
            '<p>?낆옄?ㅼ씠 蹂듭궗?댁꽌 諛붾줈 ?????덈뒗 ?쒗뵆由우쓣 ?쒓났?섍퀬, ?곗씠???섏쭛/媛怨??ㅼ뒿??吏꾪뻾????臾대즺 ?곗씠?곕쿋?댁뒪 ??븷???대떦?⑸땲??</p>'
            '<strong>?뵎 ?곕룞 轅??</strong> "Base share link"瑜??쒖꽦?뷀븯???낆옄?ㅼ씠 ?대┃ ??踰덉쑝濡?蹂몄씤???뚰겕?ㅽ럹?댁뒪濡??곗씠?곕? 蹂듭젣??媛????덇쾶 ?좊룄?섏꽭??'
            '</div>',
            unsafe_allow_html=True
        )

    # ?ㅽ듃由쇰┸
    with st.container():
        st.markdown(
            '<div class="platform-card">'
            '<span class="badge badge-streamlit">Streamlit / Glide</span>'
            '<h4>???명꽣?숉떚釉??꾨줈?좏?????/h4>'
            '<p>?뚯씠???먮뒗 ?몄퐫???대줈 鍮좊Ⅴ寃?留뚮뱶???낆옄 ?ㅼ뒿??紐⑤땲?곕쭅 ??쒕낫?쒖엯?덈떎. ?덉쑝濡??뺤씤?섎뒗 ?щ?瑜?二쇱뼱 ?낆옄 ?댄깉??留됱뒿?덈떎.</p>'
            '<strong>?뵎 ?곕룞 轅??</strong> Streamlit Cloud瑜??쒖슜?섎㈃ 源껎뿀釉??덊룷吏?좊━? ?곕룞?섏뿬 紐?珥?留뚯뿉 臾대즺 ???꾨찓?몄쑝濡?諛고룷?????덉뒿?덈떎.'
            '</div>',
            unsafe_allow_html=True
        )

with col_right:
    st.markdown("### ?렞 ?ㅼ뒿 ?뚮옯??援ъ텞 泥댄겕由ъ뒪??)
    st.write("?섎쭔???먮룞???숈뒿 ?뚮옯?쇱쓣 ?꾩꽦???섍???吏꾪뻾 ?곹깭瑜??먭???蹂댁꽭??")
    
    # ?명꽣?숉떚釉?泥댄겕諛뺤뒪
    wp_install = st.checkbox("WordPress 釉붾줈洹?媛쒖꽕 諛??몄뒪???곌껐 ?꾨즺", value=st.session_state['checklist']['wp_install'])
    wp_adsense = st.checkbox("援ш? ?좊뱶?쇱뒪 ?뱀씤 ?좎껌 ?먮뒗 愿묎퀬 肄붾뱶 ?쎌엯", value=st.session_state['checklist']['wp_adsense'])
    naver_blog = st.checkbox("?ㅼ씠踰?釉뚮옖??釉붾줈洹?媛쒖꽕 諛?泥?湲 ?깅줉", value=st.session_state['checklist']['naver_blog'])
    airtable_schema = st.checkbox("Airtable ?ㅼ뒿??媛??DB ?뚯씠釉??ㅺ퀎", value=st.session_state['checklist']['airtable_schema'])
    streamlit_deploy = st.checkbox("Streamlit ??쒕낫????濡쒖뺄 ?쒕쾭 媛??諛??뺤씤", value=st.session_state['checklist']['streamlit_deploy'])
    email_signup = st.checkbox("由щ뱶 ?띾뱷???대찓??援щ룆 ??諛?留덇렇???ㅺ퀎", value=st.session_state['checklist']['email_signup'])
    
    # ?곹깭 ?낅뜲?댄듃
    st.session_state['checklist'] = {
        "wp_install": wp_install,
        "wp_adsense": wp_adsense,
        "naver_blog": naver_blog,
        "airtable_schema": airtable_schema,
        "streamlit_deploy": streamlit_deploy,
        "email_signup": email_signup
    }
    
    # 吏꾩쿃瑜?怨꾩궛 諛??쒓컖??
    completed_tasks = sum(st.session_state['checklist'].values())
    total_tasks = len(st.session_state['checklist'])
    progress_percent = int((completed_tasks / total_tasks) * 100)
    
    st.markdown("---")
    st.markdown(f"**?룛截??뚮옯???꾩꽦?? `{progress_percent}%`**")
    st.progress(progress_percent / 100.0)
    
    if progress_percent == 100:
        st.balloons()
        st.success("?럦 異뺥븯?⑸땲?? 1??湲곗뾽 ?먮룞???숈뒿 諛??섏씡???뚮옯??援ъ텞 以鍮꾧? 紐⑤몢 ?앸궗?듬땲?? ?댁젣 蹂멸꺽?곸쑝濡??몃옒?쎌쓣 紐⑥븘蹂댁꽭??")
    elif progress_percent >= 50:
        st.info("?몟 ?꾩＜ ?섑븯怨?怨꾩떗?덈떎! ?듭떖 湲곕뒫?ㅼ씠 ?덈컲 ?댁긽 ?곌껐?섏뿀?댁슂.")
    else:
        st.warning("?쭢 ?댁젣 ?쒖옉?낅땲?? 李④렐李④렐 泥댄겕由ъ뒪?몃? ?ъ꽦?섎ŉ ?뚮옯?쇱쓣 援ъ텞??蹂댁븘??")
        
    st.write("---")
    st.markdown("### ?뱟 3?④퀎 援ъ텞 ?ㅽ뻾 媛?대뱶")
    
    with st.expander("1?④퀎: 肄섑뀗痢?鍮뚮뱶??(肄섑뀗痢??덈툕 援ъ텞)"):
        st.write("""
        - **紐⑺몴:** 寃??諛⑸Ц?먭? ?ㅼ뼱? ?숈뒿??媛移섍? ?덈뒗 8遺???쒕━利??ъ뒪??諛쒗뻾.
        - **?≪뀡:** 吏湲?援щ룞 以묒씤 ??쒕낫??`dashboard.py`)瑜??듯빐 ?쒕━利덈? ?앹꽦?섍퀬 ?뚮뱶?꾨젅?ㅼ뿉 draft(?꾩떆湲)濡??≪텧?섏뿬 ?덉빟 ?명똿?섏꽭??
        """)
        
    with st.expander("2?④퀎: 由щ뱶 留덇렇???쒓났 (?좎옱 怨좉컼 ?쎌씤)"):
        st.write("""
        - **紐⑺몴:** 諛⑸Ц?먭? ?쇳쉶?깆쑝濡??섍?踰꾨━吏 ?딅룄濡??대찓??援щ룆???뺣낫 ?섏쭛.
        - **?≪뀡:** ?먯뼱?뚯씠釉??ㅼ뒿 ?쒗뵆由?二쇱냼瑜?怨듦컻?섍퀬, '異붽? 怨좉툒 ?먮룞???뚯뒪肄붾뱶'瑜?臾대즺濡?諛쏄린 ?꾪빐 ?대찓?쇱쓣 ?낅젰?섎룄濡??쇱쓣 ?곕룞?섏꽭??
        """)
        
    with st.expander("3?④퀎: ?ㅼ뒿 ??諛고룷 (泥댄뿕??釉뚮옖??"):
        st.write("""
        - **紐⑺몴:** ?낆옄媛 吏곸젒 ?ㅼ뒿?섍퀬 ?좊ː瑜??볦쓣 ???덈뒗 怨듦컙 諛고룷.
        - **?≪뀡:** Streamlit?대굹 Glide ?뱀빋 留곹겕瑜?湲 ?대? 諛곕꼫濡??몄텧?섏뿬 ?λ?瑜??좊컻?섏꽭??
        """)

    st.write("---")
    st.markdown("### ?븩 ?ㅼ뒿 李멸퀬: ?낅Т 紐⑸줉??諛?????몃옒??媛?대뱶 ?명룷洹몃옒??)
    st.image(
        r"C:\Users\diamt\.gemini\antigravity\brain\934e1b88-24dc-4d4d-ba25-e7670d7f1d11\time_tracking_infographic_1780739970065.png",
        caption="1??湲곗뾽 ?앹궛??洹밸??붾? ?꾪븳 ????몃옒??留덉뒪?고겢?섏뒪 ?명룷洹몃옒??,
        use_container_width=True
    )
    
    st.write("---")
    st.caption("1??湲곗뾽 IT ?먮룞??媛?대뱶 v1.1")
