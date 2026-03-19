import streamlit as st
import time
import base64
from PIL import Image

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
# 4. 이미지 → base64
# ─────────────────────────────────────────
@st.cache_resource
def load_b64(filename: str) -> str:
    path = f"{IMAGE_DIR}/{filename}"
    img = Image.open(path).convert("RGB").resize((300, 220), Image.LANCZOS)
    import io
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

# ─────────────────────────────────────────
# 5. CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
.main .block-container {
    max-width: 760px;
    margin: 0 auto;
    padding-top: 1rem;
}
iframe[title="st_balloons.balloons"] {
    transform: scale(0.5) !important;
    transform-origin: center center !important;
}

/* ── 이미지 카드 (직접 HTML 렌더링) ── */
.img-card {
    border: 4px solid #e0e0e0;
    border-radius: 14px;
    overflow: hidden;
    cursor: pointer;
    transition: border-color 0.15s, box-shadow 0.15s;
    background: white;
    margin-bottom: 10px;
}
.img-card img {
    width: 100%;
    height: 180px;
    object-fit: cover;
    display: block;
    pointer-events: none;
}
.img-card.selected {
    border: 6px solid #667eea;
    box-shadow: 0 0 0 2px #667eea44;
}

/* ── 텍스트 선택지 버튼 ── */

/* 미선택: secondary — 보라 테두리 */
button[data-testid="stBaseButton-secondary"] {
    height: 110px !important;
    font-size: 28px !important;
    font-weight: bold !important;
    border-radius: 16px !important;
    border: 4px solid #667eea !important;
    background-color: white !important;
    color: #667eea !important;
    white-space: normal !important;
    word-break: keep-all !important;
    line-height: 1.3 !important;
}
button[data-testid="stBaseButton-secondary"] p {
    font-size: 28px !important;
    font-weight: bold !important;
    color: #667eea !important;
}

/* 선택됨: primary — 분홍 테두리 + 분홍 텍스트 + 연분홍 배경 */
button[data-testid="stBaseButton-primary"].txt-option {
    height: 110px !important;
    font-size: 28px !important;
    font-weight: bold !important;
    border-radius: 16px !important;
    border: 6px solid #e91e8c !important;
    background-color: #fff0f8 !important;
    color: #e91e8c !important;
    box-shadow: none !important;
    white-space: normal !important;
    word-break: keep-all !important;
    line-height: 1.3 !important;
}
button[data-testid="stBaseButton-primary"].txt-option p {
    font-size: 28px !important;
    font-weight: bold !important;
    color: #e91e8c !important;
}

/* ── 확인 / 다시하기 버튼: primary — 보라 둥근 버튼 ── */
button[data-testid="stBaseButton-primary"]:not(.txt-option) {
    height: 120px !important;
    font-size: 28px !important;
    font-weight: bold !important;
    border-radius: 50px !important;
    border: none !important;
    background-color: #667eea !important;
    color: white !important;
    box-shadow: 0 6px 18px rgba(102,126,234,0.45) !important;
    transition: background 0.2s, transform 0.2s !important;
    white-space: normal !important;
    line-height: 1.3 !important;
}
button[data-testid="stBaseButton-primary"]:not(.txt-option) p {
    font-size: 28px !important;
    font-weight: bold !important;
    color: white !important;
}
button[data-testid="stBaseButton-primary"]:not(.txt-option):hover {
    background-color: #5a6fd6 !important;
    transform: translateY(-3px) !important;
}
button[data-testid="stBaseButton-primary"]:not(.txt-option):disabled {
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

.result-section {
    background: #f0f2f6;
    border-radius: 20px;
    padding: 40px 30px;
    width: 100%;
    text-align: center;
    margin-bottom: 20px;
}
.result-text { font-weight: bold; color: #333; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 6. 정답 처리
# ─────────────────────────────────────────
def process_answer(selected_idx: int):
    current_q = QUIZZES[st.session_state.quiz_idx]
    if selected_idx == current_q['correct_index']:
        st.markdown(f'<div class="result-msg-box correct-box">{current_q["success"]}</div>',
                    unsafe_allow_html=True)
        st.balloons()
        st.session_state.score += 1
        time.sleep(2)
    else:
        st.markdown(f'<div class="result-msg-box error-box">{current_q["failure"]}</div>',
                    unsafe_allow_html=True)
        time.sleep(2)

    st.session_state.img_chosen = None
    st.session_state.txt_chosen = None
    if st.session_state.quiz_idx < len(QUIZZES) - 1:
        st.session_state.quiz_idx += 1
    else:
        st.session_state.complete = True
    st.rerun()

# ─────────────────────────────────────────
# 7. 메인 화면
# ─────────────────────────────────────────
st.markdown("<h1 style='text-align:center;color:#667eea;'>정연이 정우 퀴즈풀기 ⭐</h1>",
            unsafe_allow_html=True)

if not st.session_state.complete:
    current_q = QUIZZES[st.session_state.quiz_idx]
    st.progress(st.session_state.quiz_idx / len(QUIZZES))
    st.markdown(f"<h3 style='text-align:center;'>Q{st.session_state.quiz_idx+1}. {current_q['title']}</h3>",
                unsafe_allow_html=True)

    # ══════════════════════════════════════
    # 이미지 퀴즈 — streamlit-image-select 대신 직접 HTML 카드로 구현
    # 클릭 → 숨겨진 st.button 트리거 방식
    # ══════════════════════════════════════
    if current_q['type'] == 'image':
        img_sel = st.session_state.img_chosen  # None or 0~3

        col1, col2 = st.columns(2)
        cols = [col1, col2, col1, col2]

        # 숨겨진 트리거 버튼 4개 (높이 0으로 완전히 숨김)
        st.markdown("""
        <style>
        .hidden-triggers { overflow:hidden; height:0; margin:0; padding:0; }
        .hidden-triggers button { height:0 !important; min-height:0 !important;
            padding:0 !important; border:none !important; margin:0 !important;
            visibility:hidden !important; }
        </style>
        """, unsafe_allow_html=True)

        trigger_cols = st.columns(4)
        triggers = []
        with st.container():
            st.markdown('<div class="hidden-triggers">', unsafe_allow_html=True)
            for i in range(4):
                with trigger_cols[i]:
                    triggers.append(
                        st.button("x", key=f"imgtrig_{st.session_state.quiz_idx}_{i}")
                    )
            st.markdown('</div>', unsafe_allow_html=True)

        # 트리거 버튼이 눌렸으면 선택 업데이트
        for i, clicked in enumerate(triggers):
            if clicked:
                st.session_state.img_chosen = i
                st.rerun()

        # 이미지 카드 렌더링 (2x2)
        for i, fname in enumerate(current_q['options']):
            b64 = load_b64(fname)
            selected_class = "selected" if img_sel == i else ""
            # onclick → 해당 트리거 버튼 클릭
            js = f"""
                var btns = window.parent.document.querySelectorAll(
                    'button[data-testid="stBaseButton-secondary"]'
                );
                // hidden-triggers 안의 버튼들 중 i번째
                var hidden = Array.from(window.parent.document.querySelectorAll(
                    '.hidden-triggers button'
                ));
                if(hidden[{i}]) hidden[{i}].click();
            """
            card_html = f"""
            <div class="img-card {selected_class}"
                 onclick="{js.strip()}"
                 style="margin-bottom:10px;">
                <img src="{b64}" />
            </div>
            """
            with cols[i]:
                st.markdown(card_html, unsafe_allow_html=True)

        st.write("")
        if st.button("✅ 이걸로 할래요!",
                     key=f"confirm_img_{st.session_state.quiz_idx}",
                     use_container_width=True, type="primary",
                     disabled=(img_sel is None)):
            process_answer(img_sel)

    # ══════════════════════════════════════
    # 텍스트 퀴즈
    # 선택됨 → type="primary" (분홍 스타일)
    # 미선택 → type="secondary" (보라 스타일)
    # ══════════════════════════════════════
    else:
        cur = st.session_state.txt_chosen
        col1, col2 = st.columns(2)
        cols = [col1, col2, col1, col2]

        for i, option in enumerate(current_q['options']):
            with cols[i]:
                if cur == i:
                    # 선택된 항목: primary 타입 → 분홍 스타일
                    if st.button(option,
                                 key=f"txt_{st.session_state.quiz_idx}_{i}",
                                 use_container_width=True,
                                 type="primary"):
                        # 같은 버튼 다시 누르면 선택 해제
                        st.session_state.txt_chosen = None
                        st.rerun()
                else:
                    # 미선택: secondary 타입 → 보라 스타일
                    if st.button(option,
                                 key=f"txt_{st.session_state.quiz_idx}_{i}",
                                 use_container_width=True,
                                 type="secondary"):
                        st.session_state.txt_chosen = i
                        st.rerun()

        st.write("")
        if st.button("✅ 이걸로 할래요!",
                     key=f"confirm_txt_{st.session_state.quiz_idx}",
                     use_container_width=True, type="primary",
                     disabled=(cur is None)):
            process_answer(cur)

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
    st.write("")
    if st.button("처음부터 다시 하기 🔄", key="restart",
                 use_container_width=True, type="primary"):
        st.session_state.quiz_idx   = 0
        st.session_state.score      = 0
        st.session_state.complete   = False
        st.session_state.img_chosen = None
        st.session_state.txt_chosen = None
        st.rerun()
