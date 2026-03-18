import streamlit as st
import time
import base64
import os

# --- 1. 페이지 설정 및 제목 ---
st.set_page_config(page_title="정연이 정우 퀴즈풀기", page_icon="⭐", layout="centered")

# --- 2. 퀴즈 데이터 정의 ---
QUIZZES = [
    {'id': 1, 'type': 'image', 'title': '불을 끄는 소방관이 타고 다니는 차는 뭘까?', 'options': ['police.jpg', '119.jpg', 'kids.jpg', 'truck.jpg'], 'correct_index': 1, 'success': '딩동댕! 🎉 소방차를 어떻게 알았지?', 'failure': '땡! 소방차는 빨간색이야!'},
    {'id': 2, 'type': 'image', 'title': '이 중에 왕자핑이 누구~게?', 'options': ['princeping.jpg', 'auroraping.jpg', 'heartsping.jpg', 'fixping.jpg'], 'correct_index': 0, 'success': '맞았어! 🎉 왕자핑을 잘 찾았어', 'failure': '땡! 왕자핑은 남자아이야!'},
    {'id': 3, 'type': 'image', 'title': '아빠차를 찾아봐!', 'options': ['tucson.jpg', 'koleos.jpg', 'gwagon.jpg', 'sorrento.jpg'], 'correct_index': 3, 'success': '맞았어! 🎉 아빠차 이름은 쏘렌토야', 'failure': '땡! 다 비슷하게 생겼지?'},
    {'id': 4, 'type': 'text', 'title': '아빠의 엄마는 누구~게?', 'options': ['송도할머니', '수지할머니', '이모', '돌봄선생님'], 'correct_index': 0, 'success': '딩동댕! 🎉 송도할머니야!', 'failure': '땡! 잘 생각해 보자~'},
    {'id': 5, 'type': 'text', 'title': '엄마의 아빠는 누구~게?', 'options': ['송도할아버지', '수지할아버지', '깜깜아저씨', '고모부'], 'correct_index': 1, 'success': '딩동댕! 🎉 수지할아버지야!', 'failure': '땡! 엄마의 아빠는 누구지?'},
    {'id': 6, 'type': 'text', 'title': '딸기의 색깔은?', 'options': ['노랑', '초록', '빨강', '파랑'], 'correct_index': 2, 'success': '맞았어! 🎉 딸기는 빨간색이야!', 'failure': '땡! 딸기는 빨간색이야~'},
    {'id': 7, 'type': 'text', 'title': '밖에서 놀고 집에오면 뭐부터 해야할까?', 'options': ['과자 먹기', '유튜브 보기', '손씻기', '춤추기'], 'correct_index': 2, 'success': '딩동댕! 🎉 손을 깨끗이 씻자!', 'failure': '땡! 손 안 씻으면 아야해요!'}
]

# --- 3. 세션 상태 초기화 ---
for key, val in [('quiz_idx', 0), ('score', 0), ('complete', False), ('selected', None)]:
    if key not in st.session_state:
        st.session_state[key] = val

# --- 4. CSS ---
st.markdown("""
<style>
/* ── 전체 레이아웃 ── */
.main .block-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    max-width: 720px;
    margin: 0 auto;
}

/* ── 풍선 크기 절반으로 ── */
iframe[title="st_balloons.balloons"] {
    transform: scale(0.5) !important;
    transform-origin: center center !important;
}

/* ────────────────────────────────────────────
   이미지 카드: 이미지 + 클릭 오버레이 버튼
   ──────────────────────────────────────────── */
.img-card-wrapper {
    position: relative;
    width: 100%;
    cursor: pointer;
    border-radius: 20px;
    overflow: hidden;
    border: 4px solid #667eea;
    box-shadow: 0 4px 12px rgba(102,126,234,0.15);
    transition: transform 0.2s, box-shadow 0.2s;
    background: white;
}
.img-card-wrapper:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 24px rgba(102,126,234,0.35);
}
.img-card-wrapper img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    display: block;
}
/* 투명 클릭 오버레이 — 이미지 전체 영역을 버튼으로 */
.img-card-wrapper .overlay-btn {
    position: absolute;
    inset: 0;
    background: transparent;
    border: none;
    cursor: pointer;
    z-index: 10;
}

/* ────────────────────────────────────────────
   텍스트 선택지 버튼 — 4개 완전 동일 크기
   ──────────────────────────────────────────── */
div[data-testid="stButton"] > button {
    width: 100% !important;
    min-width: 0 !important;
    height: 110px !important;
    font-size: 28px !important;
    font-weight: bold !important;
    border-radius: 20px !important;
    border: 4px solid #667eea !important;
    background-color: white !important;
    color: #667eea !important;
    transition: all 0.25s ease;
    white-space: normal !important;
    word-break: keep-all !important;
    line-height: 1.3 !important;
}
div[data-testid="stButton"] > button:hover {
    background-color: #667eea !important;
    color: white !important;
    transform: translateY(-4px);
    box-shadow: 0 10px 20px rgba(102,126,234,0.4);
}

/* ── 결과 메시지 박스 ── */
.result-msg-box {
    padding: 22px;
    border-radius: 20px;
    font-size: 28px;
    font-weight: bold;
    margin: 18px auto;
    width: 100%;
    text-align: center;
    animation: fadeIn 0.4s ease-out;
}
.correct-box { background-color: #90EE90; color: #2d5016; }
.error-box   { background-color: #FFB6C1; color: #8b0000; }
@keyframes fadeIn { from {opacity:0;} to {opacity:1;} }

/* ── 결과 페이지 ── */
.result-section {
    background-color: #f0f2f6;
    border-radius: 20px;
    padding: 40px 30px;
    margin-bottom: 20px;
    width: 100%;
    text-align: center;
}
.result-text { font-weight: bold; color: #333; }

/* 결과 페이지 '다시하기' 버튼 — 가운데 고정 */
.restart-wrap {
    display: flex;
    justify-content: center;
    width: 100%;
    margin-top: 10px;
}
.restart-wrap div[data-testid="stButton"] > button {
    height: 70px !important;
    font-size: 22px !important;
    width: 280px !important;
    border-radius: 35px !important;
}
</style>
""", unsafe_allow_html=True)

# ── 이미지를 base64로 변환하는 헬퍼 ──────────────────────────────────────────
def img_to_b64(path: str) -> str:
    """파일을 base64 data-URI 문자열로 변환"""
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ext = path.rsplit(".", 1)[-1].lower()
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "gif": "image/gif"}.get(ext, "image/jpeg")
    return f"data:{mime};base64,{data}"

# ── 이미지 카드 (클릭 → st.query_params 로 선택 전달) ─────────────────────
def image_card(img_path: str, idx: int, quiz_key: int):
    """
    이미지 전체가 클릭 가능한 카드를 렌더링한다.
    클릭 시 URL 쿼리 파라미터 ?sel=<idx>&q=<quiz_key> 를 설정하여
    Streamlit rerun 을 유도한다.
    """
    b64 = img_to_b64(img_path)
    if not b64:
        # 이미지 없으면 placeholder
        b64_src = "https://placehold.co/300x200?text=No+Image"
    else:
        b64_src = b64

    # JS: 쿼리스트링 변경 → 페이지 reload → Streamlit 이 파라미터를 읽음
    js_click = (
        f"window.location.search = '?sel={idx}&q={quiz_key}';"
    )
    st.markdown(f"""
        <div class="img-card-wrapper" onclick="{js_click}">
            <img src="{b64_src}" alt="option {idx}"/>
        </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# 5. 메인 화면
# ════════════════════════════════════════════════════════════════
st.markdown("<h1 style='text-align:center; color:#667eea;'>정연이 정우 퀴즈풀기 ⭐</h1>", unsafe_allow_html=True)

# ── 이미지 퀴즈: 쿼리 파라미터에서 선택 읽기 ──────────────────────────────
params = st.query_params
if "sel" in params and "q" in params:
    try:
        sel_idx  = int(params["sel"])
        sel_q    = int(params["q"])
        # 현재 문제와 일치할 때만 처리 (중복 방지)
        if sel_q == st.session_state.quiz_idx and st.session_state.selected is None:
            st.session_state.selected = sel_idx
        st.query_params.clear()   # 파라미터 소비 후 제거
    except ValueError:
        st.query_params.clear()

if not st.session_state.complete:
    current_q = QUIZZES[st.session_state.quiz_idx]

    # 진행바
    st.progress(st.session_state.quiz_idx / len(QUIZZES))
    st.markdown(
        f"<h3 style='text-align:center;'>Q{st.session_state.quiz_idx + 1}. {current_q['title']}</h3>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    cols = [col1, col2, col1, col2]

    # ── 이미지 퀴즈 ──────────────────────────────────────────────────────────
    if current_q['type'] == 'image':
        for i, option in enumerate(current_q['options']):
            with cols[i]:
                image_card(
                    f"static/images/{option}",
                    idx=i,
                    quiz_key=st.session_state.quiz_idx
                )

    # ── 텍스트 퀴즈 ──────────────────────────────────────────────────────────
    else:
        for i, option in enumerate(current_q['options']):
            with cols[i]:
                st.write("")  # 수직 간격
                if st.button(option, key=f"txt_{st.session_state.quiz_idx}_{i}"):
                    st.session_state.selected = i

    # ── 선택 처리 ─────────────────────────────────────────────────────────────
    if st.session_state.selected is not None:
        selected_idx = st.session_state.selected
        st.session_state.selected = None   # 소비

        if selected_idx == current_q['correct_index']:
            st.markdown(
                f'<div class="result-msg-box correct-box">{current_q["success"]}</div>',
                unsafe_allow_html=True
            )
            st.balloons()
            st.session_state.score += 1
            time.sleep(2)
        else:
            st.markdown(
                f'<div class="result-msg-box error-box">{current_q["failure"]}</div>',
                unsafe_allow_html=True
            )
            time.sleep(2)

        if st.session_state.quiz_idx < len(QUIZZES) - 1:
            st.session_state.quiz_idx += 1
        else:
            st.session_state.complete = True
        st.rerun()

# ════════════════════════════════════════════════════════════════
# 6. 결과 페이지
# ════════════════════════════════════════════════════════════════
else:
    st.balloons()
    st.markdown(f"""
        <div class="result-section">
            <h1 class="result-text" style="font-size:50px;">🎉 퀴즈 끝! 🎉</h1>
            <h2 class="result-text" style="font-size:30px;">정말 잘했어! 얘들아!</h2>
            <h1 class="result-text" style="font-size:45px; color:#667eea; margin-top:20px;">
                🌟 {len(QUIZZES)}문제 중 {st.session_state.score}개 정답! 🌟
            </h1>
        </div>
    """, unsafe_allow_html=True)

    # 다시하기 버튼 — .restart-wrap 으로 감싸서 CSS 가운데 정렬
    st.markdown('<div class="restart-wrap">', unsafe_allow_html=True)
    if st.button("처음부터 다시 하기 🔄"):
        st.session_state.quiz_idx  = 0
        st.session_state.score     = 0
        st.session_state.complete  = False
        st.session_state.selected  = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
