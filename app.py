import streamlit as st
import time
from PIL import Image
from streamlit_image_select import image_select

# ─────────────────────────────────────────
# 1. 페이지 설정
# ─────────────────────────────────────────
st.set_page_config(page_title="정연이 정우 퀴즈풀기", page_icon="⭐", layout="centered")

# ─────────────────────────────────────────
# 2. 퀴즈 데이터
# ─────────────────────────────────────────
QUIZZES = [
    {'id': 1, 'type': 'image', 'title': '불을 끄는 소방관이 타고 다니는 차는 뭘까?',
     'options': ['police.jpg','119.jpg','kids.jpg','truck.jpg'],
     'correct_index': 1,
     'success': '딩동댕! 🎉 소방차를 어떻게 알았지?', 'failure': '땡! 소방차는 빨간색이야!'},
    {'id': 2, 'type': 'image', 'title': '이 중에 왕자핑이 누구~게?',
     'options': ['princeping.jpg','auroraping.jpg','heartsping.jpg','fixping.jpg'],
     'correct_index': 0,
     'success': '맞았어! 🎉 왕자핑을 잘 찾았어', 'failure': '땡! 왕자핑은 남자아이야!'},
    {'id': 3, 'type': 'image', 'title': '아빠차를 찾아봐!',
     'options': ['tucson.jpg','koleos.jpg','gwagon.jpg','sorrento.jpg'],
     'correct_index': 3,
     'success': '맞았어! 🎉 아빠차 이름은 쏘렌토야', 'failure': '땡! 다 비슷하게 생겼지?'},
    {'id': 4, 'type': 'text', 'title': '아빠의 엄마는 누구~게?',
     'options': ['송도할머니','수지할머니','이모','돌봄선생님'],
     'correct_index': 0,
     'success': '딩동댕! 🎉 송도할머니야!', 'failure': '땡! 잘 생각해 보자~'},
    {'id': 5, 'type': 'text', 'title': '엄마의 아빠는 누구~게?',
     'options': ['송도할아버지','수지할아버지','깜깜아저씨','고모부'],
     'correct_index': 1,
     'success': '딩동댕! 🎉 수지할아버지야!', 'failure': '땡! 엄마의 아빠는 누구지?'},
    {'id': 6, 'type': 'text', 'title': '딸기의 색깔은?',
     'options': ['노랑','초록','빨강','파랑'],
     'correct_index': 2,
     'success': '맞았어! 🎉 딸기는 빨간색이야!', 'failure': '땡! 딸기는 빨간색이야~'},
    {'id': 7, 'type': 'text', 'title': '밖에서 놀고 집에오면 뭐부터 해야할까?',
     'options': ['과자 먹기','유튜브 보기','손씻기','춤추기'],
     'correct_index': 2,
     'success': '딩동댕! 🎉 손을 깨끗이 씻자!', 'failure': '땡! 손 안 씻으면 아야해요!'}
]

IMAGE_DIR = "static/images"

# ─────────────────────────────────────────
# 3. 세션 상태
# ─────────────────────────────────────────
for key, val in [('quiz_idx', 0), ('score', 0), ('complete', False),
                 ('img_chosen', None), ('txt_chosen', None)]:
    if key not in st.session_state:
        st.session_state[key] = val

# ─────────────────────────────────────────
# 4. CSS  ── data-role 속성으로 버튼을 명확히 구분
# ─────────────────────────────────────────
st.markdown("""
<style>
/* ── 전체 컨테이너 ── */
.main .block-container {
    max-width: 760px;
    margin: 0 auto;
    padding-top: 1rem;
}

/* ── 풍선 절반 크기 ── */
iframe[title="st_balloons.balloons"] {
    transform: scale(0.5) !important;
    transform-origin: center center !important;
}

/* ════════════════════════════════════════
   텍스트 선택지 카드
   — 이미지 카드와 동일한 높이(220px), 1열에 2개
   ════════════════════════════════════════ */
.txt-card {
    width: 100%;
    height: 220px;
    border-radius: 16px;
    border: 4px solid #667eea;
    background: white;
    color: #667eea;
    font-size: 36px;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-sizing: border-box;
    word-break: keep-all;
    line-height: 1.3;
    transition: background 0.2s, color 0.2s, transform 0.2s, box-shadow 0.2s;
    margin-bottom: 12px;
    -webkit-tap-highlight-color: rgba(102,126,234,0.15);
    user-select: none;
}
.txt-card:hover {
    background: #eff1ff;
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(102,126,234,0.25);
}
.txt-card.selected {
    background: #667eea;
    color: white;
    box-shadow: 0 6px 16px rgba(102,126,234,0.45);
}

/* ════════════════════════════════════════
   확인 버튼 / 다시하기 버튼  ← 순수 HTML 버튼
   ════════════════════════════════════════ */
.big-btn {
    display: block;
    width: 480px;
    max-width: 92%;
    height: 72px;
    margin: 18px auto 0;
    border: none;
    border-radius: 40px;
    background: #667eea;
    color: white;
    font-size: 32px;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 6px 18px rgba(102,126,234,0.45);
    transition: background 0.2s, transform 0.2s, box-shadow 0.2s;
    -webkit-tap-highlight-color: rgba(102,126,234,0.2);
}
.big-btn:hover {
    background: #5a6fd6;
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(102,126,234,0.55);
}
.big-btn:active {
    transform: translateY(0);
    box-shadow: 0 4px 10px rgba(102,126,234,0.4);
}
.big-btn:disabled {
    background: #b0b8f0;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}

/* ════════════════════════════════════════
   결과 메시지 박스
   ════════════════════════════════════════ */
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
.correct-box { background: #90EE90; color: #2d5016; }
.error-box   { background: #FFB6C1; color: #8b0000; }
@keyframes fadeIn { from {opacity:0;} to {opacity:1;} }

/* ════════════════════════════════════════
   결과 페이지
   ════════════════════════════════════════ */
.result-section {
    background: #f0f2f6;
    border-radius: 20px;
    padding: 40px 30px;
    margin-bottom: 20px;
    width: 100%;
    text-align: center;
}
.result-text { font-weight: bold; color: #333; }

/* Streamlit 기본 버튼은 이 앱에서 사용 안 함 → 숨김 */
div[data-testid="stButton"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 5. JS 브릿지: HTML 버튼 클릭 → Streamlit rerun
#    st.query_params 를 사용해 선택값 전달
# ─────────────────────────────────────────
# query_params 에서 액션 읽기
params = st.query_params
action = params.get("action", "")
val    = params.get("val", "")

if action == "txt_select" and val != "":
    st.session_state.txt_chosen = int(val)
    st.query_params.clear()
    st.rerun()

if action == "confirm" and val != "":
    # val = 선택 인덱스
    chosen = int(val)
    st.session_state._pending_answer = chosen
    st.query_params.clear()
    st.rerun()

if action == "restart":
    st.session_state.quiz_idx   = 0
    st.session_state.score      = 0
    st.session_state.complete   = False
    st.session_state.img_chosen = None
    st.session_state.txt_chosen = None
    if hasattr(st.session_state, '_pending_answer'):
        del st.session_state['_pending_answer']
    st.query_params.clear()
    st.rerun()

# ─────────────────────────────────────────
# 6. 정답 처리 (pending_answer 가 있을 때)
# ─────────────────────────────────────────
if '_pending_answer' in st.session_state and not st.session_state.complete:
    selected_idx = st.session_state.pop('_pending_answer')
    current_q    = QUIZZES[st.session_state.quiz_idx]

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

    st.session_state.img_chosen = None
    st.session_state.txt_chosen = None
    if st.session_state.quiz_idx < len(QUIZZES) - 1:
        st.session_state.quiz_idx += 1
    else:
        st.session_state.complete = True
    st.rerun()

# ─────────────────────────────────────────
# 7. 이미지 로드
# ─────────────────────────────────────────
@st.cache_resource
def load_image(filename: str) -> Image.Image:
    img = Image.open(f"{IMAGE_DIR}/{filename}").convert("RGB")
    return img.resize((300, 220), Image.LANCZOS)

# ─────────────────────────────────────────
# 8. JS 클릭 헬퍼
# ─────────────────────────────────────────
def js_goto(action: str, val: str = "") -> str:
    """버튼 onclick 에 넣을 JS — query_params 변경으로 rerun 유도"""
    return f"window.location.search='?action={action}&val={val}';"

# ─────────────────────────────────────────
# 9. 메인 화면
# ─────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center; color:#667eea;'>정연이 정우 퀴즈풀기 ⭐</h1>",
    unsafe_allow_html=True
)

if not st.session_state.complete:
    current_q = QUIZZES[st.session_state.quiz_idx]
    st.progress(st.session_state.quiz_idx / len(QUIZZES))
    st.markdown(
        f"<h3 style='text-align:center;'>Q{st.session_state.quiz_idx + 1}. {current_q['title']}</h3>",
        unsafe_allow_html=True
    )

    # ── 이미지 퀴즈 ───────────────────────────────────────────────
    if current_q['type'] == 'image':
        pil_images = [load_image(fn) for fn in current_q['options']]

        chosen_img = image_select(
            label="",
            images=pil_images,
            use_container_width=True,
            return_value="original",
            key=f"imgsel_{st.session_state.quiz_idx}"
        )
        chosen_idx = next(
            (i for i, img in enumerate(pil_images) if chosen_img is img), 0
        )
        st.session_state.img_chosen = chosen_idx

        # 확인 버튼 (순수 HTML — query_params 방식)
        st.markdown(
            f'<button class="big-btn" onclick="{js_goto("confirm", chosen_idx)}">✅ 이걸로 할래요!</button>',
            unsafe_allow_html=True
        )

    # ── 텍스트 퀴즈 ──────────────────────────────────────────────
    else:
        cur = st.session_state.txt_chosen   # 현재 선택(None or int)

        # 2열 그리드 — HTML 카드로 렌더링
        col1, col2 = st.columns(2)
        for i, option in enumerate(current_q['options']):
            sel_class = "selected" if cur == i else ""
            card_html = f"""
                <div class="txt-card {sel_class}"
                     onclick="{js_goto('txt_select', i)}">
                    {option}
                </div>"""
            if i % 2 == 0:
                with col1:
                    st.markdown(card_html, unsafe_allow_html=True)
            else:
                with col2:
                    st.markdown(card_html, unsafe_allow_html=True)

        # 확인 버튼 — 항목 선택 전엔 비활성(disabled)
        confirm_val = cur if cur is not None else -1
        disabled    = "disabled" if cur is None else ""
        st.markdown(
            f'<button class="big-btn" {disabled} onclick="{js_goto("confirm", confirm_val)}">✅ 이걸로 할래요!</button>',
            unsafe_allow_html=True
        )

# ── 결과 페이지 ──────────────────────────────────────────────────
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
        <button class="big-btn" onclick="{js_goto('restart')}">처음부터 다시 하기 🔄</button>
    """, unsafe_allow_html=True)
