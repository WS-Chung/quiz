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
                 ('img_chosen', 0), ('txt_chosen', None)]:
    if key not in st.session_state:
        st.session_state[key] = val

# ─────────────────────────────────────────
# 4. 이미지 로드
# ─────────────────────────────────────────
@st.cache_resource
def load_image(filename: str) -> Image.Image:
    img = Image.open(f"{IMAGE_DIR}/{filename}").convert("RGB")
    return img.resize((300, 220), Image.LANCZOS)

# ─────────────────────────────────────────
# 5. CSS  — 버튼을 data-testid + nth-child 로 격리
# ─────────────────────────────────────────
st.markdown("""
<style>
/* ── 기본 레이아웃 ── */
.main .block-container {
    max-width: 760px;
    margin: 0 auto;
    padding-top: 1rem;
}

/* ── 풍선 절반 ── */
iframe[title="st_balloons.balloons"] {
    transform: scale(0.5) !important;
    transform-origin: center center !important;
}

/* ══════════════════════════════════════
   [A] 텍스트 선택지 버튼
       .txt-option-area 안의 버튼만 적용
   ══════════════════════════════════════ */
.txt-option-area div[data-testid="stButton"] > button {
    width: 100% !important;
    height: 220px !important;
    font-size: 36px !important;
    font-weight: bold !important;
    border-radius: 16px !important;
    border: 4px solid #667eea !important;
    background-color: white !important;
    color: #667eea !important;
    white-space: normal !important;
    word-break: keep-all !important;
    line-height: 1.3 !important;
    transition: background 0.2s, color 0.2s, transform 0.2s !important;
}
.txt-option-area div[data-testid="stButton"] > button:hover {
    background-color: #eff1ff !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 20px rgba(102,126,234,0.25) !important;
}

/* 선택된 텍스트 항목 강조 */
.txt-selected div[data-testid="stButton"] > button {
    background-color: #667eea !important;
    color: white !important;
    box-shadow: 0 6px 16px rgba(102,126,234,0.45) !important;
}

/* ══════════════════════════════════════
   [B] 확인 버튼 / 다시하기 버튼
       .confirm-area 안의 버튼만 적용
   ══════════════════════════════════════ */
.confirm-area {
    margin-top: 24px;
}
.confirm-area div[data-testid="stButton"] > button {
    width: 100% !important;
    height: 144px !important;
    font-size: 51px !important;
    font-weight: bold !important;
    border-radius: 40px !important;
    border: none !important;
    background-color: #667eea !important;
    color: white !important;
    box-shadow: 0 6px 18px rgba(102,126,234,0.45) !important;
    transition: background 0.2s, transform 0.2s, box-shadow 0.2s !important;
}
.confirm-area div[data-testid="stButton"] > button:hover {
    background-color: #5a6fd6 !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 24px rgba(102,126,234,0.55) !important;
}

/* 비활성 확인 버튼 */
.confirm-area div[data-testid="stButton"] > button:disabled {
    background-color: #b0b8f0 !important;
    cursor: not-allowed !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ── 결과 메시지 ── */
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
@keyframes fadeIn { from{opacity:0} to{opacity:1} }

/* ── 결과 페이지 ── */
.result-section {
    background: #f0f2f6;
    border-radius: 20px;
    padding: 40px 30px;
    width: 100%;
    text-align: center;
}
.result-text { font-weight: bold; color: #333; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 6. 정답 처리 함수
# ─────────────────────────────────────────
def process_answer(selected_idx: int):
    current_q = QUIZZES[st.session_state.quiz_idx]
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

    st.session_state.img_chosen = 0
    st.session_state.txt_chosen = None
    if st.session_state.quiz_idx < len(QUIZZES) - 1:
        st.session_state.quiz_idx += 1
    else:
        st.session_state.complete = True
    st.rerun()

# ─────────────────────────────────────────
# 7. 메인 화면
# ─────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center;color:#667eea;'>정연이 정우 퀴즈풀기 ⭐</h1>",
    unsafe_allow_html=True
)

if not st.session_state.complete:
    current_q = QUIZZES[st.session_state.quiz_idx]
    st.progress(st.session_state.quiz_idx / len(QUIZZES))
    st.markdown(
        f"<h3 style='text-align:center;'>Q{st.session_state.quiz_idx+1}. {current_q['title']}</h3>",
        unsafe_allow_html=True
    )

    # ══════════════════════════════════════
    # 이미지 퀴즈
    # ══════════════════════════════════════
    if current_q['type'] == 'image':
        pil_images = [load_image(fn) for fn in current_q['options']]

        chosen_img = image_select(
            label="",
            images=pil_images,
            use_container_width=True,
            return_value="original",
            key=f"imgsel_{st.session_state.quiz_idx}"
        )
        # 현재 선택 인덱스 파악 및 저장
        st.session_state.img_chosen = next(
            (i for i, img in enumerate(pil_images) if chosen_img is img), 0
        )

        # ── 확인 버튼: 가운데 열에 배치 ──
        _, center, _ = st.columns([1, 4, 1])
        with center:
            st.markdown('<div class="confirm-area">', unsafe_allow_html=True)
            if st.button("✅ 이걸로 할래요!", key=f"confirm_img_{st.session_state.quiz_idx}"):
                process_answer(st.session_state.img_chosen)
            st.markdown('</div>', unsafe_allow_html=True)

    # ══════════════════════════════════════
    # 텍스트 퀴즈
    # ══════════════════════════════════════
    else:
        cur = st.session_state.txt_chosen
        col1, col2 = st.columns(2)
        cols = [col1, col2, col1, col2]

        for i, option in enumerate(current_q['options']):
            # 선택된 항목은 .txt-selected 클래스로 감싸 강조
            wrapper_class = "txt-option-area txt-selected" if cur == i else "txt-option-area"
            st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
            with cols[i]:
                if st.button(option, key=f"txt_{st.session_state.quiz_idx}_{i}"):
                    st.session_state.txt_chosen = i
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # ── 확인 버튼 (항상 표시, 미선택시 비활성) ──
        _, center, _ = st.columns([1, 4, 1])
        with center:
            st.markdown('<div class="confirm-area">', unsafe_allow_html=True)
            if st.button(
                "✅ 이걸로 할래요!",
                key=f"confirm_txt_{st.session_state.quiz_idx}",
                disabled=(cur is None)
            ):
                process_answer(cur)
            st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════
# 결과 페이지
# ══════════════════════════════════════════
else:
    st.balloons()
    st.markdown(f"""
        <div class="result-section">
            <h1 class="result-text" style="font-size:50px;">🎉 퀴즈 끝! 🎉</h1>
            <h2 class="result-text" style="font-size:30px;">정말 잘했어! 얘들아!</h2>
            <h1 class="result-text" style="font-size:45px;color:#667eea;margin-top:20px;">
                🌟 {len(QUIZZES)}문제 중 {st.session_state.score}개 정답! 🌟
            </h1>
        </div>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 4, 1])
    with center:
        st.markdown('<div class="confirm-area">', unsafe_allow_html=True)
        if st.button("처음부터 다시 하기 🔄", key="restart"):
            st.session_state.quiz_idx   = 0
            st.session_state.score      = 0
            st.session_state.complete   = False
            st.session_state.img_chosen = 0
            st.session_state.txt_chosen = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
