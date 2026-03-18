import streamlit as st
import time
from PIL import Image
from streamlit_image_select import image_select

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="정연이 정우 퀴즈풀기", page_icon="⭐", layout="centered")

# --- 2. 퀴즈 데이터 ---
QUIZZES = [
    {'id': 1, 'type': 'image', 'title': '불을 끄는 소방관이 타고 다니는 차는 뭘까?',
     'options': ['police.jpg', '119.jpg', 'kids.jpg', 'truck.jpg'],
     'correct_index': 1,
     'success': '딩동댕! 🎉 소방차를 어떻게 알았지?', 'failure': '땡! 소방차는 빨간색이야!'},
    {'id': 2, 'type': 'image', 'title': '이 중에 왕자핑이 누구~게?',
     'options': ['princeping.jpg', 'auroraping.jpg', 'heartsping.jpg', 'fixping.jpg'],
     'correct_index': 0,
     'success': '맞았어! 🎉 왕자핑을 잘 찾았어', 'failure': '땡! 왕자핑은 남자아이야!'},
    {'id': 3, 'type': 'image', 'title': '아빠차를 찾아봐!',
     'options': ['tucson.jpg', 'koleos.jpg', 'gwagon.jpg', 'sorrento.jpg'],
     'correct_index': 3,
     'success': '맞았어! 🎉 아빠차 이름은 쏘렌토야', 'failure': '땡! 다 비슷하게 생겼지?'},
    {'id': 4, 'type': 'text', 'title': '아빠의 엄마는 누구~게?',
     'options': ['송도할머니', '수지할머니', '이모', '돌봄선생님'],
     'correct_index': 0,
     'success': '딩동댕! 🎉 송도할머니야!', 'failure': '땡! 잘 생각해 보자~'},
    {'id': 5, 'type': 'text', 'title': '엄마의 아빠는 누구~게?',
     'options': ['송도할아버지', '수지할아버지', '깜깜아저씨', '고모부'],
     'correct_index': 1,
     'success': '딩동댕! 🎉 수지할아버지야!', 'failure': '땡! 엄마의 아빠는 누구지?'},
    {'id': 6, 'type': 'text', 'title': '딸기의 색깔은?',
     'options': ['노랑', '초록', '빨강', '파랑'],
     'correct_index': 2,
     'success': '맞았어! 🎉 딸기는 빨간색이야!', 'failure': '땡! 딸기는 빨간색이야~'},
    {'id': 7, 'type': 'text', 'title': '밖에서 놀고 집에오면 뭐부터 해야할까?',
     'options': ['과자 먹기', '유튜브 보기', '손씻기', '춤추기'],
     'correct_index': 2,
     'success': '딩동댕! 🎉 손을 깨끗이 씻자!', 'failure': '땡! 손 안 씻으면 아야해요!'}
]

IMAGE_DIR = "static/images"

# --- 3. 세션 상태 초기화 ---
for key, val in [('quiz_idx', 0), ('score', 0), ('complete', False),
                 ('img_chosen_idx', None), ('txt_chosen_idx', None)]:
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

/* ── 풍선 크기 절반 ── */
iframe[title="st_balloons.balloons"] {
    transform: scale(0.5) !important;
    transform-origin: center center !important;
}

/* ══════════════════════════════════════════
   텍스트 선택지 버튼
   이미지 카드(300×220)와 동일한 비율로 맞춤
   ══════════════════════════════════════════ */
div[data-testid="stButton"] > button {
    width: 100% !important;
    height: 220px !important;          /* 이미지 카드 높이와 동일 */
    font-size: 34px !important;        /* 박스가 커진 만큼 텍스트도 확대 */
    font-weight: bold !important;
    border-radius: 16px !important;
    border: 4px solid #667eea !important;
    background-color: white !important;
    color: #667eea !important;
    transition: all 0.25s ease;
    white-space: normal !important;
    word-break: keep-all !important;
    line-height: 1.3 !important;
}
div[data-testid="stButton"] > button:hover {
    background-color: #eff1ff !important;
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(102,126,234,0.3);
}
/* 선택된 텍스트 항목 강조 (선택 후 rerun 전까지) */
div[data-testid="stButton"] > button.selected-txt {
    background-color: #667eea !important;
    color: white !important;
}

/* ══════════════════════════════════════════
   "이걸로 할래요!" 확인 버튼
   — 가운데 정렬, 좌우 2배 폭, 텍스트 1.5배
   ══════════════════════════════════════════ */
.confirm-wrap {
    display: flex;
    justify-content: center;
    width: 100%;
    margin-top: 16px;
}
.confirm-wrap div[data-testid="stButton"] > button {
    width: 480px !important;           /* 좌우로 충분히 넓게 */
    height: 80px !important;
    font-size: 33px !important;        /* 기존 대비 약 1.5배 */
    font-weight: bold !important;
    border-radius: 40px !important;
    background-color: #667eea !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 6px 18px rgba(102,126,234,0.45);
    transition: all 0.25s ease;
}
.confirm-wrap div[data-testid="stButton"] > button:hover {
    background-color: #5a6fd6 !important;
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(102,126,234,0.55);
}

/* ══════════════════════════════════════════
   결과 메시지 박스
   ══════════════════════════════════════════ */
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

/* ══════════════════════════════════════════
   결과 페이지
   ══════════════════════════════════════════ */
.result-section {
    background-color: #f0f2f6;
    border-radius: 20px;
    padding: 40px 30px;
    margin-bottom: 20px;
    width: 100%;
    text-align: center;
}
.result-text { font-weight: bold; color: #333; }

/* "처음부터 다시하기" — 가운데, 2배 폭, 텍스트 1.5배 */
.restart-wrap {
    display: flex;
    justify-content: center;
    width: 100%;
    margin-top: 10px;
}
.restart-wrap div[data-testid="stButton"] > button {
    width: 480px !important;           /* 좌우 2배 확대 */
    height: 80px !important;
    font-size: 33px !important;        /* 텍스트 1.5배 */
    font-weight: bold !important;
    border-radius: 40px !important;
    background-color: #667eea !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 6px 18px rgba(102,126,234,0.45);
}
.restart-wrap div[data-testid="stButton"] > button:hover {
    background-color: #5a6fd6 !important;
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(102,126,234,0.55);
}

/* ══════════════════════════════════════════
   선택된 텍스트 버튼 강조용 커스텀 박스
   ══════════════════════════════════════════ */
.txt-selected-box {
    width: 100%;
    height: 220px;
    border-radius: 16px;
    border: 4px solid #667eea;
    background-color: #667eea;
    color: white;
    font-size: 34px;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    word-break: keep-all;
    line-height: 1.3;
    box-sizing: border-box;
    padding: 8px;
}
</style>
""", unsafe_allow_html=True)

# --- 5. 이미지 로드 헬퍼 ---
@st.cache_resource
def load_image(filename: str) -> Image.Image:
    img = Image.open(f"{IMAGE_DIR}/{filename}").convert("RGB")
    img = img.resize((300, 220), Image.LANCZOS)
    return img

# ════════════════════════════════════════════════════════════════
# 6. 메인 화면
# ════════════════════════════════════════════════════════════════
st.markdown("<h1 style='text-align:center; color:#667eea;'>정연이 정우 퀴즈풀기 ⭐</h1>", unsafe_allow_html=True)

if not st.session_state.complete:
    current_q = QUIZZES[st.session_state.quiz_idx]

    st.progress(st.session_state.quiz_idx / len(QUIZZES))
    st.markdown(
        f"<h3 style='text-align:center;'>Q{st.session_state.quiz_idx + 1}. {current_q['title']}</h3>",
        unsafe_allow_html=True
    )

    selected_idx = None   # 확인 버튼 눌렸을 때 최종 확정값

    # ── 이미지 퀴즈 ──────────────────────────────────────────────
    if current_q['type'] == 'image':
        pil_images = [load_image(fn) for fn in current_q['options']]

        chosen_img = image_select(
            label="",
            images=pil_images,
            use_container_width=True,
            return_value="original",
            key=f"imgsel_{st.session_state.quiz_idx}"
        )

        # 현재 선택 인덱스를 세션에 보관
        st.session_state.img_chosen_idx = next(
            (i for i, img in enumerate(pil_images) if chosen_img is img), 0
        )

        # ── 확인 버튼 (가운데 정렬, 넓게) ──
        st.markdown('<div class="confirm-wrap">', unsafe_allow_html=True)
        if st.button("✅ 이걸로 할래요!", key=f"confirm_{st.session_state.quiz_idx}"):
            selected_idx = st.session_state.img_chosen_idx
        st.markdown('</div>', unsafe_allow_html=True)

    # ── 텍스트 퀴즈 ──────────────────────────────────────────────
    else:
        col1, col2 = st.columns(2)
        cols = [col1, col2, col1, col2]
        cur_txt = st.session_state.txt_chosen_idx  # 현재 선택(미확정)

        for i, option in enumerate(current_q['options']):
            with cols[i]:
                if cur_txt == i:
                    # 선택된 항목 → 보라색 강조 박스로 표시
                    st.markdown(
                        f'<div class="txt-selected-box">{option}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    # 미선택 항목 → 일반 버튼
                    if st.button(option, key=f"txt_{st.session_state.quiz_idx}_{i}"):
                        st.session_state.txt_chosen_idx = i
                        st.rerun()

        # ── 확인 버튼: 항목을 하나라도 골랐을 때만 표시 ──
        if cur_txt is not None:
            st.markdown('<div class="confirm-wrap">', unsafe_allow_html=True)
            if st.button("✅ 이걸로 할래요!", key=f"confirm_txt_{st.session_state.quiz_idx}"):
                selected_idx = st.session_state.txt_chosen_idx
            st.markdown('</div>', unsafe_allow_html=True)

    # ── 선택 처리 ─────────────────────────────────────────────────
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

        # 다음 문제로
        st.session_state.img_chosen_idx = None
        st.session_state.txt_chosen_idx = None
        if st.session_state.quiz_idx < len(QUIZZES) - 1:
            st.session_state.quiz_idx += 1
        else:
            st.session_state.complete = True
        st.rerun()

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
    """, unsafe_allow_html=True)

    st.markdown('<div class="restart-wrap">', unsafe_allow_html=True)
    if st.button("처음부터 다시 하기 🔄"):
        st.session_state.quiz_idx       = 0
        st.session_state.score          = 0
        st.session_state.complete       = False
        st.session_state.img_chosen_idx = None
        st.session_state.txt_chosen_idx = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
