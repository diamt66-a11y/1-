import streamlit as st
import time
import json
import run_agents

# ==========================================================================
# UI / ?붿옄???ㅼ젙
# ==========================================================================
st.set_page_config(
    page_title="?붾줈?꾨젅???쒕━利??몄쭛 ??쒕낫??,
    page_icon="??,
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
# Session State 珥덇린??
# ==========================================================================
if 'series_title' not in st.session_state:
    st.session_state['series_title'] = ""
if 'generated_posts' not in st.session_state:
    st.session_state['generated_posts'] = []
if 'is_running' not in st.session_state:
    st.session_state['is_running'] = False

# ==========================================================================
# Sidebar ?ㅼ젙 ?곸뿭
# ==========================================================================
with st.sidebar:
    st.header("?숋툘 ?쒖뒪???뺣낫 ?뺤씤")
    st.write("---")
    st.success("?쨼 ?먯씠?꾪듃 以鍮??꾨즺 (Gemini-2.5-Flash)")
    st.info(f"?뙋 ?뚮뱶?꾨젅??二쇱냼:\n{run_agents.WP_URL}")
    st.info(f"?뫀 ?ъ슜??怨꾩젙:\n{run_agents.WP_USER}")
    st.info(f"?눛 ?ㅼ씠踰?釉붾줈洹?\nblog.naver.com/agentlabs")
    
    st.write("---")
    if st.button("?봽 ??쒕낫???곗씠??珥덇린??):
        st.session_state['series_title'] = ""
        st.session_state['generated_posts'] = []
        st.session_state['is_running'] = False
        st.rerun()

    st.write("---")
    st.caption("1??湲곗뾽 ?먮룞 ?섏씡 ?먮룞???꾧뎄 v2.5")

# ==========================================================================
# Main UI ?붿옄??
# ==========================================================================
st.markdown('<h1 class="main-title">???붾줈?꾨젅???곗옱 ?ъ뒪???먯씠?꾪듃</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">援ш? ?뚮뱶?꾨젅???꾩넚怨??④퍡 ?ㅼ씠踰?釉붾줈洹몄뿉 理쒖쟻?붾맂 蹂듭궗 ?띿뒪?몃? ?쒓났?섏뿬 理쒖쟻?????몃옓(Two-Track) 釉뚮옖?⑹쓣 ?뺤뒿?덈떎.</p>', unsafe_allow_html=True)

# 1. 二쇱젣 ?낅젰 ?꾨뱶
topic_input = st.text_input(
    "?랃툘 釉붾줈洹?湲?????二쇱젣瑜??먯쑀濡?쾶 ?낅젰?섏꽭??,
    value="1??湲곗뾽???앹궛?깆쓣 洹밸??뷀븯??IT ?먮룞??鍮꾧껐",
    placeholder="?? 1??湲곗뾽?쇰줈 ?깃났?섎뒗 釉붾줈洹?釉뚮옖???꾨왂"
)

# 2. ?곗옱 ?몄닔 議곗젅 ?щ씪?대뜑
series_count = st.slider(
    "?뱴 紐?遺???쒕━利덈줈 履쇨컻???곗옱 ?ъ뒪?낆쓣 諛쒗뻾?좉퉴??",
    min_value=2,
    max_value=8,
    value=8,
    step=1
)

# ?먯씠?꾪듃 媛??踰꾪듉
if st.button("?? ?먯씠?꾪듃 ?곗옱 吏묓븘 ?쒖옉", type="primary"):
    st.session_state['generated_posts'] = []
    st.session_state['series_title'] = ""
    
    status_box = st.empty()
    main_progress = st.progress(0)
    
    try:
        run_agents.init_gemini()
        
        # 1?④퀎: 湲고쉷 (Planner)
        status_box.info(f"?쨼 Planner媛 {series_count}遺???쒕━利?紐⑹감? ?뚯젣紐⑸뱾???ㅺ퀎 以묒엯?덈떎...")
        main_progress.progress(15)
        
        series_plan = run_agents.run_planner(topic_input, series_count)
        st.session_state['series_title'] = series_plan['series_title']
        
        # 2~3?④퀎: ?쒖감??吏묓븘 諛??몄쭛
        for idx, post in enumerate(series_plan['posts']):
            part_num = post['part_number']
            percent_complete = 15 + int((idx / series_count) * 80)
            main_progress.progress(percent_complete)
            
            status_box.info(f"?쨼 ??{part_num}??湲 吏묓븘 諛?SEO ?몄쭛 媛怨?以?..")
            
            # Writer濡?蹂몃Ц ?묒꽦
            raw_content = run_agents.run_writer(post, part_num, series_count)
            
            # Editor濡?寃??諛?媛怨?
            final_post = run_agents.run_editor(post['title'], raw_content)
            
            # HTML 肄붾뱶瑜??ㅼ씠踰??먮뵒?곗슜 ?쇰컲 媛?낆꽦 ?띿뒪?몃줈 移섑솚?섍린 ?꾪븳 媛怨?
            import re
            naver_text = final_post['final_content']
            # ?쒓렇???쒓굅
            naver_text = re.sub(r'<hr\s*/?>', '\n----------------------------------------\n', naver_text)
            naver_text = re.sub(r'<h2>(.*?)</h2>', r'\n\n[?뚯젣紐? \1\n', naver_text)
            naver_text = re.sub(r'<h3>(.*?)</h3>', r'\n\n[?뚯＜?? \1\n', naver_text)
            naver_text = re.sub(r'<li><a href="(.*?)" target="_blank">(.*?)</a></li>', r'??\2 (\1)', naver_text)
            naver_text = re.sub(r'<p>(.*?)</p>', r'\1\n', naver_text)
            naver_text = re.sub(r'<.*?>', '', naver_text)  # ?⑥? HTML ?쒓렇 ?뚭굅
            naver_text = naver_text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
            
            # ?ㅼ씠踰꾩슜 湲 ?뚭컻 ?ㅽ봽??蹂댁젙 異붽?
            naver_intro = f"?덈뀞?섏꽭?? 1??湲곗뾽 IT ?먮룞???숈뒿 釉붾줈洹몄엯?덈떎.\n?ㅻ뒛 ?낅줈?쒗븯??湲? {st.session_state['series_title']} ?쒕━利덉쓽 ??{part_num}???ъ뒪?낆엯?덈떎. 1??李쎌뾽媛濡??앹〈?섍린 ?꾪븳 湲곗닠 濡쒕뱶留듭쓣 ?④퍡 怨듬??섎ŉ 留덉뒪?고빐 遊낆떆??\n\n"
            naver_text = naver_intro + naver_text
            
            # ?몄뀡 ?ㅽ뀒?댄듃???몄쭛 媛?ν븯?꾨줉 ?꾩떆 蹂닿?
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
        status_box.success("?럦 紐⑤뱺 ?먯씠?꾪듃 吏묓븘???꾨즺?섏뿀?듬땲?? ?꾨옒 ?먮뵒?곗뿉??湲???뺤씤?섍퀬 ?ㅻ벉??蹂댁꽭??")
        st.rerun()
        
    except Exception as e:
        main_progress.progress(0)
        status_box.error(f"???묒뾽 ?섑뻾 以??쒖뒪???ㅻ쪟 諛쒖깮: {str(e)}")

# ==========================================================================
# ?랃툘 ?ㅼ떆媛???쒕낫???몄쭛 & ?≪텧 ?쒖뼱 ?뚮뜑留??곸뿭
# ==========================================================================
if st.session_state['generated_posts']:
    st.write("---")
    st.markdown(f"### ?뱷 '{st.session_state['series_title']}' ?쒕━利??몄쭛 ?湲곗떎")
    st.info("?뮕 ?? ?꾨옒 ?띿뒪???곸옄 ?덉뿉??媛?낆꽦???믪씠湲??꾪빐 留덉쓬猿?以꾨컮轅?Enter) 諛??ㅽ? 援먯젙??吏꾪뻾???? 媛??몄쓽 [?≪텧] 踰꾪듉???꾨Ⅴ?몄슂.")
    
    for idx, post in enumerate(st.session_state['generated_posts']):
        part_num = post['part_number']
        
        with st.container():
            st.markdown(f"#### ?뱴 ??{part_num}?? {post['title']}")
            
            # 1. ?쒕ぉ ?몄쭛 ?꾨뱶
            edited_title = st.text_input(
                f"??{part_num}??理쒖쥌 ?쒕ぉ",
                value=post['title'],
                key=f"title_part_{part_num}"
            )
            st.session_state['generated_posts'][idx]['title'] = edited_title
            
            # 2. 蹂몃Ц(HTML) ?몄쭛 ?꾨뱶
            edited_content = st.text_area(
                f"??{part_num}??蹂몃Ц HTML 肄붾뱶 ?몄쭛李?(援ш? ?뚮뱶?꾨젅?ㅼ슜)",
                value=post['content'],
                height=300,
                key=f"content_part_{part_num}"
            )
            st.session_state['generated_posts'][idx]['content'] = edited_content
            
            # 3. 寃???붿빟臾??몄쭛 ?꾨뱶
            edited_desc = st.text_area(
                f"??{part_num}??援ш? 寃???붿빟(Meta Description) ?몄쭛",
                value=post['description'],
                height=80,
                key=f"desc_part_{part_num}"
            )
            st.session_state['generated_posts'][idx]['description'] = edited_desc
            
            # 4. ?ㅼ씠踰?釉붾줈洹?諛쒗뻾???띿뒪???곸옄 (?ㅻ줈吏 ?띿뒪??蹂듭궗?⑹쑝濡?源붾걫?섍쾶 援ъ꽦)
            with st.expander(f"?윟 ??{part_num}???ㅼ씠踰?釉붾줈洹??ъ뒪?낆슜 蹂듭궗 ?띿뒪??):
                st.markdown('<div class="naver-box">', unsafe_allow_html=True)
                st.caption("?꾨옒 ?띿뒪???곸옄 ?대?瑜?蹂듭궗?섏뀛???ㅼ씠踰??ㅻ쭏?몄뿉?뷀꽣??諛붾줈 遺숈뿬?ｊ린?섏꽭??")
                st.text_area(
                    "?ㅼ씠踰꾩슜 蹂몃Ц (Ctrl + A ??Ctrl + C濡??꾩껜 蹂듭궗 媛??",
                    value=post['naver_content'],
                    height=250,
                    key=f"naver_part_{part_num}"
                )
                st.markdown(f'<a href="https://blog.naver.com/agentlabs" target="_blank" style="display: inline-block; padding: 0.5rem 1rem; background-color: #2db400; color: white; border-radius: 6px; font-weight: 600; text-decoration: none; font-size: 0.9rem; margin-top: 0.5rem;">?ㅼ씠踰?湲?곌린 ?붾㈃?쇰줈 ?대룞 ??/a>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # 諛고룷 ?곹깭 異쒕젰 諛??쒖뼱 ?⑥텛
            if post['published_link']:
                st.markdown(f'<p style="color: #10b981; font-weight: 600;">??援ш? ?뚮뱶?꾨젅???꾩넚 ?꾨즺! <a href="{post["published_link"]}" target="_blank">?뚮뱶?꾨젅?ㅼ뿉???덉빟/?몄쭛?섍린 ??/a></p>', unsafe_allow_html=True)
            else:
                col1, col2 = st.columns([3, 7])
                with col1:
                    if st.button(f"?뱾 ??{part_num}???뚮뱶?꾨젅?ㅻ줈 理쒖쥌 ?≪텧", key=f"publish_btn_{part_num}", type="primary"):
                        with st.spinner("?뚮뱶?꾨젅???쒕쾭???덉쟾?섍쾶 ?낅줈??以?.."):
                            wp_payload = {
                                "final_title": edited_title,
                                "final_content": edited_content,
                                "description": edited_desc,
                                "tags": [t.strip() for t in post['tags'].split(",") if t.strip()]
                            }
                            
                            post_link = run_agents.publish_to_wordpress(wp_payload)
                            
                            if post_link:
                                st.session_state['generated_posts'][idx]['published_link'] = post_link
                                st.success(f"?럦 ??{part_num}???≪텧 ?꾨즺!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("?뚮뱶?꾨젅???꾩넚 ?꾩쨷 ?ㅻ쪟媛 諛쒖깮?덉뒿?덈떎. ?ъ씠???곌껐?대굹 ?묒슜?꾨줈洹몃옩 鍮꾨?踰덊샇 ?ㅼ젙???ы솗?명빐 二쇱꽭??")
            
            st.write("---")
