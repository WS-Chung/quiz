import streamlit as st
import time
import base64
import io
from PIL import Image
from st_clickable_images import clickable_images

st.set_page_config(page_title="정연이 정우 퀴즈풀기", page_icon="⭐", layout="centered")

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

for key, val in [('quiz_idx', 0), ('score', 0), ('complete', False),
                 ('img_chosen', None), ('txt_chosen', None)]:
    if key not in st.session_state:
        st.session_state[key] = val

@st.cache_resource
def load_b64(filename: str) -> str:
    img = Image.open(f"{IMAGE_DIR}/{filename}").convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

st.markdown("""
<style>
/* ══ 상단 여백 제거 ══ */
[data-testid="stHeader"]     { display: none !important; }
[data-testid="stToolbar"]    { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
.stApp > header              { display: none !important; }
.main .block-container {
    max-width: 720px;
    margin: 0 auto;
    padding-top: 0.4rem !important;
    padding-bottom: 0.4rem !important;
}
iframe[title="st_balloons.balloons"] {
    transform: scale(0.5) !important;
    transform-origin: center center !important;
}

/* ══ 텍스트 선택지 버튼 (primary)
   height를 vw 단위로 → 화면 너비의 절반 크기로 정사각형 유지
   모바일(360px): 약 170px / PC(720px): 약 340px → max로 제한
   ══ */
button[data-testid="stBaseButton-primary"] {
    width: 100% !important;
    height: min(42vw, 300px) !important;
    font-size: clamp(14px, 4.5vw, 26px) !important;
    font-weight: bold !important;
    border-radius: 14px !important;
    white-space: normal !important;
    word-break: keep-all !important;
    line-height: 1.3 !important;
    box-shadow: none !important;
    border: 3px solid #667eea !important;
    background-color: white !important;
    color: #667eea !important;
    transition: none !important;
    padding: 8px !important;
}
button[data-testid="stBaseButton-primary"] p {
    font-size: clamp(14px, 4.5vw, 26px) !important;
    font-weight: bold !important;
    line-height: 1.3 !important;
    color: #667eea !important;
}
/* 피드백 없음 */
button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="stBaseButton-primary"]:active,
button[data-testid="stBaseButton-primary"]:focus {
    background-color: white !important;
    border-color: #667eea !important;
    outline: none !important;
    box-shadow: none !important;
    color: #667eea !important;
}

/* ══ 다시하기 버튼 (secondary) ══ */
button[data-testid="stBaseButton-secondary"] {
    aspect-ratio: unset !important;
    height: 72px !important;
    font-size: clamp(16px, 4vw, 22px) !important;
    font-weight: bold !important;
    border-radius: 50px !important;
    white-space: normal !important;
    line-height: 1.3 !important;
    box-shadow: 0 5px 15px rgba(102,126,234,0.4) !important;
    border: 3px solid #667eea !important;
    background-color: #667eea !important;
    color: white !important;
    margin-top: 8px !important;
}
button[data-testid="stBaseButton-secondary"] p {
    font-size: clamp(16px, 4vw, 22px) !important;
    font-weight: bold !important;
    color: white !important;
}
button[data-testid="stBaseButton-secondary"]:hover {
    background-color: #5a6fd6 !important;
}

/* ══ 정답/오답 메시지 ══ */
.result-msg-box {
    padding: clamp(8px, 2vw, 16px);
    border-radius: 14px;
    font-size: clamp(14px, 4.5vw, 22px);
    font-weight: bold;
    margin: 8px auto;
    width: 100%;
    text-align: center;
    animation: fadeIn 0.3s ease-out;
}
.correct-box { background: #90EE90; color: #2d5016; }
.error-box   { background: #FFB6C1; color: #8b0000; }
@keyframes fadeIn { from{opacity:0} to{opacity:1} }

/* ══ 결과 페이지 ══ */
.result-section {
    background: #f0f2f6;
    border-radius: 18px;
    padding: clamp(16px, 4vw, 36px);
    width: 100%;
    text-align: center;
    margin-bottom: 12px;
}
.result-text { font-weight: bold; color: #333; }
</style>
""", unsafe_allow_html=True)

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

# ── 제목 ──
st.markdown(
    "<h1 style='text-align:center;color:#667eea;"
    "font-size:clamp(20px,6vw,32px);margin:0 0 2px 0;padding:0;'>"
    "정연이 정우 퀴즈풀기 ⭐</h1>",
    unsafe_allow_html=True
)

if not st.session_state.complete:
    current_q = QUIZZES[st.session_state.quiz_idx]
    st.progress(st.session_state.quiz_idx / len(QUIZZES))
    st.markdown(
        f"<p style='text-align:center;font-weight:bold;"
        f"font-size:clamp(13px,4vw,19px);margin:4px 0 8px 0;'>"
        f"Q{st.session_state.quiz_idx+1}. {current_q['title']}</p>",
        unsafe_allow_html=True
    )

    qidx = st.session_state.quiz_idx

    # ── 이미지 퀴즈 ──
    if current_q['type'] == 'image':
        b64_list = [load_b64(fn) for fn in current_q['options']]
        clicked  = clickable_images(
            b64_list,
            titles=["", "", "", ""],
            div_style={
                "display": "grid",
                "grid-template-columns": "1fr 1fr",
                "gap": "10px",
                "padding": "2px",
            },
            img_style={
                "border": "3px solid #d0d0d0",
                "border-radius": "12px",
                "cursor": "pointer",
                "object-fit": "contain",
                "background": "#f8f8f8",
                "width": "100%",
                "aspect-ratio": "1 / 1",
                "-webkit-tap-highlight-color": "transparent",
            },
            key=f"clickimg_{qidx}"
        )
        if clicked > -1:
            process_answer(clicked)

    # ── 텍스트 퀴즈: st.button으로 한글 정상 표시 ──
    # height를 vw 단위로 지정해 모바일에서도 2x2 유지
    else:
        col1, col2 = st.columns(2, gap="small")
        cols = [col1, col2, col1, col2]
        txt_clicked = None
        for i, option in enumerate(current_q['options']):
            with cols[i]:
                if st.button(option,
                             key=f"txt_{qidx}_{i}",
                             use_container_width=True,
                             type="primary"):
                    txt_clicked = i
        if txt_clicked is not None:
            process_answer(txt_clicked)

# ── 결과 페이지 ──
else:
    st.balloons()
    st.markdown(f"""
        <div class="result-section">
            <div class="result-text" style="font-size:clamp(22px,7vw,44px);">
                🎉 퀴즈 끝! 🎉</div>
            <div class="result-text"
                 style="font-size:clamp(14px,4vw,22px);margin:8px 0;">
                정말 잘했어! 얘들아!</div>
            <div class="result-text"
                 style="font-size:clamp(18px,6vw,38px);color:#667eea;margin-top:10px;">
                🌟 {len(QUIZZES)}문제 중 {st.session_state.score}개 정답! 🌟
            </div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("처음부터 다시 하기 🔄", key="restart",
                 use_container_width=True, type="secondary"):
        st.session_state.quiz_idx   = 0
        st.session_state.score      = 0
        st.session_state.complete   = False
        st.session_state.img_chosen = None
        st.session_state.txt_chosen = None
        st.rerun()
