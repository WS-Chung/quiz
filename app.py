import streamlit as st
import time
import base64
import os

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="정연이 정우 퀴즈풀기", page_icon="⭐", layout="centered")

# --- 2. 퀴즈 데이터 ---
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
.main .block-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    max-width: 720px;
    margin: 0 auto;
}

/* 풍선 크기 절반 */
iframe[title="st_balloons.balloons"] {
    transform: scale(0.5) !important;
    transform-origin: center center !important;
}

/* ── 텍스트 버튼 동일 크기 ── */
div[data-testid="stButton"] > button {
    width: 100% !important;
    height: 120px !important;
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

/* ── 숨겨진 버튼 행: 화면 공간 0, 시각적으로 완전히 숨김 ── */
.hidden-btn-row {
    overflow: hidden;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}
.hidden-btn-row div[data-testid="stButton"] > button {
    visibility: hidden !important;
    height: 0 !important;
    min-height: 0 !important;
    padding: 0 !important;
    border: none !important;
    margin: 0 !important;
    pointer-events: none !important;  /* JS click()은 동작, 사용자 클릭은 차단 */
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

# --- 5. 이미지 → base64 ---
def img_to_b64(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ext = path.rsplit(".", 1)[-1].lower()
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "gif": "image/gif"}.get(ext, "image/jpeg")
    return f"data:{mime};base64,{data}"

# --- 6. 이미지 퀴즈 그리드 ---
def image_option_grid(options: list, quiz_idx: int):
    """
    동작 원리:
      ① Streamlit 버튼 4개를 .hidden-btn-row 안에 렌더링 (CSS로 높이 0, 비가시화)
      ② 이미지 카드의 onclick JS 가 hidden-btn-row 내 해당 버튼을 .click() 으로 호출
      ③ Streamlit 이 버튼 클릭 이벤트를 감지 → rerun → selected_idx 반환
    """
    # ── ① 숨겨진 버튼 4개 ──────────────────────────────────────────
    # data-quiz 속성으로 이번 문제를 특정해 JS가 정확히 찾을 수 있게 함
    area_id = f"hba_{quiz_idx}"

    st.markdown(f'<div class="hidden-btn-row" id="{area_id}">', unsafe_allow_html=True)
    hcols = st.columns(4)
    btn_results = []
    for i in range(4):
        with hcols[i]:
            btn_results.append(st.button(f"_{i}", key=f"hbtn_{quiz_idx}_{i}"))
    st.markdown("</div>", unsafe_allow_html=True)

    # ── ② 이미지 카드 2x2 ─────────────────────────────────────────
    col1, col2 = st.columns(2)
    cols = [col1, col2, col1, col2]

    for i, option in enumerate(options):
        b64 = img_to_b64(f"static/images/{option}")
        img_src = b64 if b64 else "https://placehold.co/300x200?text=No+Image"

        # hidden-btn-row 안의 버튼 목록에서 i번째를 클릭
        js_onclick = f"""
            var area = document.getElementById('{area_id}');
            var btns = area ? area.querySelectorAll('button') : [];
            if (btns.length > {i}) {{ btns[{i}].click(); }}
        """.replace('\n', ' ')

        with cols[i]:
            st.markdown(f"""
                <div
                    onclick="{js_onclick}"
                    style="
                        cursor:pointer;
                        border-radius:20px;
                        overflow:hidden;
                        border:4px solid #667eea;
                        box-shadow:0 4px 12px rgba(102,126,234,0.15);
                        transition:transform 0.2s,box-shadow 0.2s;
                        margin-bottom:12px;
                        -webkit-tap-highlight-color: rgba(102,126,234,0.2);
                    "
                    onmouseover="this.style.transform='translateY(-5px)';this.style.boxShadow='0 10px 24px rgba(102,126,234,0.35)'"
                    onmouseout="this.style.transform='';this.style.boxShadow='0 4px 12px rgba(102,126,234,0.15)'"
                >
                    <img src="{img_src}"
                         style="width:100%;height:200px;object-fit:cover;display:block;pointer-events:none;"
                    />
                </div>
            """, unsafe_allow_html=True)

    # ── ③ 클릭된 인덱스 반환 ──────────────────────────────────────
    for i, clicked in enumerate(btn_results):
        if clicked:
            return i
    return None


# ════════════════════════════════════════════════════════════════
# 7. 메인 화면
# ════════════════════════════════════════════════════════════════
st.markdown("<h1 style='text-align:center; color:#667eea;'>정연이 정우 퀴즈풀기 ⭐</h1>", unsafe_allow_html=True)

if not st.session_state.complete:
    current_q = QUIZZES[st.session_state.quiz_idx]

    st.progress(st.session_state.quiz_idx / len(QUIZZES))
    st.markdown(
        f"<h3 style='text-align:center;'>Q{st.session_state.quiz_idx + 1}. {current_q['title']}</h3>",
        unsafe_allow_html=True
    )

    selected_idx = None

    # ── 이미지 퀴즈 ──
    if current_q['type'] == 'image':
        selected_idx = image_option_grid(current_q['options'], st.session_state.quiz_idx)

    # ── 텍스트 퀴즈 ──
    else:
        col1, col2 = st.columns(2)
        cols = [col1, col2, col1, col2]
        for i, option in enumerate(current_q['options']):
            with cols[i]:
                st.write("")
                if st.button(option, key=f"txt_{st.session_state.quiz_idx}_{i}"):
                    selected_idx = i

    # ── 선택 처리 ──
    if selected_idx is not None:
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

# ── 결과 페이지 ──
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

    st.markdown('<div class="restart-wrap">', unsafe_allow_html=True)
    if st.button("처음부터 다시 하기 🔄"):
        st.session_state.quiz_idx = 0
        st.session_state.score    = 0
        st.session_state.complete = False
        st.session_state.selected = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
