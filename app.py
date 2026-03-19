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
.main .block-container { max-width: 760px; margin: 0 auto; padding-top: 1rem; }
iframe[title="st_balloons.balloons"] {
    transform: scale(0.5) !important; transform-origin: center center !important;
}
/* 텍스트 선택지 버튼 */
button[data-testid="stBaseButton-secondary"],
button[data-testid="stBaseButton-primary"] {
    height: 110px !important; font-size: 28px !important; font-weight: bold !important;
    border-radius: 16px !important; white-space: normal !important;
    word-break: keep-all !important; line-height: 1.3 !important; box-shadow: none !important;
}
button[data-testid="stBaseButton-secondary"] p,
button[data-testid="stBaseButton-primary"] p {
    font-size: 28px !important; font-weight: bold !important; line-height: 1.3 !important;
}
button[data-testid="stBaseButton-secondary"] {
    border: 4px solid #667eea !important; background-color: white !important; color: #667eea !important;
}
button[data-testid="stBaseButton-secondary"] p { color: #667eea !important; }
button[data-testid="stBaseButton-secondary"]:hover { background-color: #f0f2ff !important; }
button[data-testid="stBaseButton-primary"] {
    border: 4px solid #667eea !important; background-color: #667eea !important; color: white !important;
}
button[data-testid="stBaseButton-primary"] p { color: white !important; }
button[data-testid="stBaseButton-primary"]:hover { background-color: #5a6fd6 !important; border-color: #5a6fd6 !important; }
button[data-testid="stBaseButton-primary"]:disabled { background-color: #b0b8f0 !important; border-color: #b0b8f0 !important; }
button[data-testid="stBaseButton-primary"][aria-label="✅ 이걸로 할래요!"],
button[data-testid="stBaseButton-primary"][aria-label="처음부터 다시 하기 🔄"] {
    border-radius: 50px !important; height: 120px !important;
    box-shadow: 0 6px 18px rgba(102,126,234,0.45) !important;
}
.result-msg-box {
    padding: 22px; border-radius: 20px; font-size: 28px; font-weight: bold;
    margin: 18px auto; width: 100%; text-align: center; animation: fadeIn 0.4s ease-out;
}
.correct-box { background: #90EE90; color: #2d5016; }
.error-box   { background: #FFB6C1; color: #8b0000; }
@keyframes fadeIn { from{opacity:0} to{opacity:1} }
.result-section {
    background: #f0f2f6; border-radius: 20px;
    padding: 40px 30px; width: 100%; text-align: center; margin-bottom: 20px;
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

st.markdown("<h1 style='text-align:center;color:#667eea;'>정연이 정우 퀴즈풀기 ⭐</h1>",
            unsafe_allow_html=True)

if not st.session_state.complete:
    current_q = QUIZZES[st.session_state.quiz_idx]
    st.progress(st.session_state.quiz_idx / len(QUIZZES))
    st.markdown(
        f"<h3 style='text-align:center;'>Q{st.session_state.quiz_idx+1}. {current_q['title']}</h3>",
        unsafe_allow_html=True)

    if current_q['type'] == 'image':
        img_sel  = st.session_state.img_chosen
        qidx     = st.session_state.quiz_idx
        b64_list = [load_b64(fn) for fn in current_q['options']]

        # 선택된 이미지 테두리 스타일
        img_styles = []
        for i in range(4):
            if i == img_sel:
                img_styles.append({
                    "border": "5px solid #667eea",
                    "border-radius": "14px",
                    "box-shadow": "0 0 0 3px rgba(102,126,234,0.2)",
                    "cursor": "pointer",
                    "object-fit": "contain",
                    "background": "#f0f2ff",
                    "width": "100%",
                })
            else:
                img_styles.append({
                    "border": "3px solid #d0d0d0",
                    "border-radius": "14px",
                    "cursor": "pointer",
                    "object-fit": "contain",
                    "background": "#f8f8f8",
                    "width": "100%",
                })

        # clickable_images: 이미지 클릭 → 인덱스 반환 (-1: 미클릭)
        clicked = clickable_images(
            b64_list,
            titles=["", "", "", ""],
            div_style={
                "display": "grid",
                "grid-template-columns": "1fr 1fr",
                "gap": "12px",
                "padding": "4px",
            },
            img_style={
                "border": "3px solid #d0d0d0",
                "border-radius": "14px",
                "cursor": "pointer",
                "object-fit": "contain",
                "background": "#f8f8f8",
                "width": "100%",
                "aspect-ratio": "1 / 1",
            },
            key=f"clickimg_{qidx}"
        )

        # 이미지 클릭 즉시 정답 처리
        if clicked > -1:
            process_answer(clicked)

    else:
        col1, col2 = st.columns(2)
        cols = [col1, col2, col1, col2]
        txt_clicked = None
        for i, option in enumerate(current_q['options']):
            with cols[i]:
                if st.button(option, key=f"txt_{st.session_state.quiz_idx}_{i}",
                             use_container_width=True, type="secondary"):
                    txt_clicked = i
        if txt_clicked is not None:
            process_answer(txt_clicked)

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
