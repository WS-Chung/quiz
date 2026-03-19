import streamlit as st
import time
import base64
import io
from PIL import Image
from st_clickable_images import clickable_images

st.set_page_config(page_title="정연 정우 퀴즈풀기", page_icon="⭐", layout="centered")

QUIZZES = [
    {'id': 1, 'type': 'image', 'title': '불을 끄는 소방관이 타고 다니는 차는 뭘까?',
     'options': ['police.jpg','119.jpg','kids.jpg','truck.jpg'],
     'correct_index': 1,
     'success': '딩동댕! 소방차 본적 있어?', 'failure': '소방차는 빨간색이야!'},
    {'id': 2, 'type': 'image', 'title': '이 중에 왕자핑이 누구~게?',
     'options': ['princeping.jpg','auroraping.jpg','heartsping.jpg','fixping.jpg'],
     'correct_index': 0,
     'success': '날 알아봐줘서 고마워', 'failure': '땡! 왕자핑은 하얀색이야!'},
    {'id': 3, 'type': 'image', 'title': '아빠차를 찾아봐!',
     'options': ['tucson.jpg','koleos.jpg','gwagon.jpg','sorrento.jpg'],
     'correct_index': 3,
     'success': '맞았어! 차 이름도 알아?', 'failure': '다 비슷하게 생겨서 어렵지?'},
    {'id': 4, 'type': 'text', 'title': '아빠의 엄마는 누구~게?',
     'options': ['송도할머니','수지할머니','이모','돌봄선생님'],
     'correct_index': 0,
     'success': '딩동댕! 잘 생각했어', 'failure': '아빠가 누구를 부를때 엄마~ 하시지?'},
    {'id': 5, 'type': 'text', 'title': '엄마의 아빠는 누구~게?',
     'options': ['송도할아버지','수지할아버지','깜깜아저씨','고모부'],
     'correct_index': 1,
     'success': '맞았어! 똑똑해~', 'failure': '엄마가 누구를 부를때 아빠~ 하시지??'},
    {'id': 6, 'type': 'text', 'title': '딸기의 색깔은?',
     'options': ['노랑','초록','빨강','파랑'],
     'correct_index': 2,
     'success': '정우랑 정연이는 딸기 좋아해?', 'failure': '딸기는 빨간색이야~'},
     {'id': 7, 'type': 'image', 'title': '바다에 사는 동물은 누구게?',
     'options': ['dog.jpg','whale.jpg','hamster.jpg','eagle.jpg'],
     'correct_index': 1,
     'success': '바다에 가본적 있어?', 'failure': '누가 헤엄을 잘치게 생겼나 잘봐~'},
    {'id': 8, 'type': 'text', 'title': '밖에서 놀고 집에오면 뭐부터 해야할까?',
     'options': ['과자 먹기','유튜브 보기','손씻기','춤추기'],
     'correct_index': 2,
     'success': '얘들아~ 손 잘 씻고 있지?', 'failure': '손 안씻으면 아야~한다구'},
    {'id': 9, 'type': 'text', 'title': '이가 아프면 어디에 가야할까요?',
     'options': ['어린이집','치과','백화점','카페'],
     'correct_index': 1,
     'success': '딩동댕! 치과 가본적 있어?', 'failure': '이가 아프면 치과에 가야해!'},
    {'id':10, 'type': 'text', 'title': '이 중에서 누구 다리가 제일 많게~?',
     'options': ['참새','고양이','거미','돌고래'],
     'correct_index': 2,
     'success': '거미 다리가 몇개인지도 알아?', 'failure': '다시 잘 생각해 보자!'}
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

/* form 테두리/패딩 제거 */
[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}

/* form 안의 직계 자식(버튼 4개)을 CSS grid로 2x2 배치
   st.columns 없이 form_submit_button 4개를 그냥 나열하면
   Streamlit이 세로로 쌓으므로, 부모 flex/grid를 덮어씀 */
[data-testid="stForm"] > div:first-child {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 12px !important;
    padding: 2px !important;
}

/* form_submit_button 래퍼 */
[data-testid="stFormSubmitButton"] {
    width: 100% !important;
}

/* 버튼 자체: 정사각형 */
[data-testid="stFormSubmitButton"] > button {
    width: 100% !important;
    aspect-ratio: 1 / 1 !important;
    height: auto !important;
    min-height: 0 !important;
    font-size: clamp(15px, 4.5vw, 26px) !important;
    font-weight: bold !important;
    border-radius: 14px !important;
    border: 3px solid #667eea !important;
    background: white !important;
    color: #667eea !important;
    white-space: normal !important;
    word-break: keep-all !important;
    line-height: 1.3 !important;
    box-shadow: none !important;
    padding: 8px !important;
    transition: none !important;
    cursor: pointer !important;
}
[data-testid="stFormSubmitButton"] > button p {
    font-size: clamp(15px, 4.5vw, 26px) !important;
    font-weight: bold !important;
    color: #667eea !important;
    line-height: 1.3 !important;
}
[data-testid="stFormSubmitButton"] > button:hover,
[data-testid="stFormSubmitButton"] > button:active,
[data-testid="stFormSubmitButton"] > button:focus {
    background: white !important;
    border-color: #667eea !important;
    box-shadow: none !important;
    outline: none !important;
}

/* 다시하기 버튼 */
button[data-testid="stBaseButton-secondary"] {
    height: 72px !important;
    font-size: clamp(16px, 4vw, 22px) !important;
    font-weight: bold !important;
    border-radius: 50px !important;
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

st.markdown(
    "<h1 style='text-align:center;color:#667eea;"
    "font-size:clamp(20px,6vw,32px);margin:0 0 2px 0;padding:0;'>"
    "정연 정우 퀴즈풀기 ⭐</h1>",
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

    else:
        # st.columns 없이 form_submit_button 4개를 나열
        # CSS가 부모 div를 grid로 만들어서 자동 2x2 배치
        with st.form(key=f"txtform_{qidx}", border=False):
            s0 = st.form_submit_button(current_q['options'][0], use_container_width=True)
            s1 = st.form_submit_button(current_q['options'][1], use_container_width=True)
            s2 = st.form_submit_button(current_q['options'][2], use_container_width=True)
            s3 = st.form_submit_button(current_q['options'][3], use_container_width=True)

        for i, s in enumerate([s0, s1, s2, s3]):
            if s:
                process_answer(i)

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
    if st.button("처음부터 다시 할래", key="restart",
                 use_container_width=True, type="secondary"):
        st.session_state.quiz_idx   = 0
        st.session_state.score      = 0
        st.session_state.complete   = False
        st.session_state.img_chosen = None
        st.session_state.txt_chosen = None
        st.rerun()
