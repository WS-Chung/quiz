import streamlit as st
import time
import base64
import io
import random  # 랜덤 추출을 위해 추가
from PIL import Image
from st_clickable_images import clickable_images

st.set_page_config(page_title="정연 정우 퀴즈풀기", page_icon="⭐", layout="centered")

# 전체 퀴즈 목록 (앞으로 계속 추가하시면 됩니다!)
QUIZZES = [
    {'id': 1, 'type': 'image', 'title': '불을 끄는 소방관이 타는 차는 뭘까?',
     'options': ['police.jpg','119.jpg','kids.jpg','truck.jpg'],
     'correct_index': 1,
     'success': '딩동댕! 소방차 본적 있어?', 'failure': '소방차는 빨간색이야!'},
    
    {'id': 2, 'type': 'image', 'title': '왕자핑이 누구~게?',
     'options': ['princeping.jpg','auroraping.jpg','heartsping.jpg','fixping.jpg'],
     'correct_index': 0,
     'success': '날 알아봐줘서 고마워', 'failure': '땡! 왕자핑은 하얀색이야!'},
    
    {'id': 3, 'type': 'image', 'title': '아빠차를 찾아봐!',
     'options': ['tucson.jpg','koleos.jpg','gwagon.jpg','sorrento.jpg'],
     'correct_index': 3,
     'success': '맞았어! 차 이름도 알아?', 'failure': '다 비슷하게 생겨서 어렵지?'},
    
    {'id': 4, 'type': 'text', 'title': '아빠의 엄마는 누구~?',
     'options': ['송도할머니','수지할머니','이모','돌봄선생님'],
     'correct_index': 0,
     'success': '딩동댕! 잘 생각했어', 'failure': '아빠가 누구를 부를때 엄마~ 하시지?'},
    
    {'id': 5, 'type': 'text', 'title': '엄마의 아빠는 누구~?',
     'options': ['송도할아버지','수지할아버지','깜깜아저씨','고모부'],
     'correct_index': 1,
     'success': '맞았어! 똑똑해~', 'failure': '엄마가 누구를 부를때 아빠~ 하시지??'},
    
    {'id': 6, 'type': 'image', 'title': 'Which One is Yellow?',
     'options': ['apple.jpg','grape.jpg','banana.jpg','strawberry.jpg'],
     'correct_index': 2,
     'success': '정우랑 정연이는 바나나 좋아해?', 'failure': 'Yellow는 노란색이란 뜻이야~'},
    
    {'id': 7, 'type': 'image', 'title': '바다에 사는 동물은 누구게?',
     'options': ['dog.jpg','whale.jpg','hamster.jpg','eagle.jpg'],
     'correct_index': 1,
     'success': '바다에 가본적 있어?', 'failure': '누가 헤엄을 잘치게 생겼나 잘봐~'},
    
    {'id': 8, 'type': 'text', 'title': '밖에서 놀고 집에오면 뭐부터 해야할까?',
     'options': ['과자 먹기','유튜브 보기','손씻기','춤추기'],
     'correct_index': 2,
     'success': '얘들아~ 손 잘 씻고 있지?', 'failure': '손 안씻으면 아야~한다구'},
    
    {'id': 9, 'type': 'text', 'title': '이가 아플 때는 어디로 가면 돼?',
     'options': ['어린이집','치과','백화점','카페'],
     'correct_index': 1,
     'success': '딩동댕! 치과 가본적 있어?', 'failure': '이가 아프면 치과에 가야해!'},
    
    {'id':10, 'type': 'text', 'title': '이 중에서 누구 다리가 제일 많게~?',
     'options': ['참새','고양이','거미','돌고래'],
     'correct_index': 2,
     'success': '거미 다리가 몇개인지도 알아?', 'failure': '다시 잘 생각해 보자!'},
    
    {'id':11, 'type': 'text', 'title': '눈사람하고 산타할아버지는 언제 볼 수 있을까?',
     'options': ['봄','여름','가을','겨울'],
     'correct_index': 3,
     'success': '겨울에 눈사람 만들어 봤어?', 'failure': '눈사람은 추울 때만 만들 수 있어!'},
    
    {'id':12, 'type': 'text', 'title': '가장 위에 있는 층은 몇층이게?',
     'options': ['1층','3층','4층','6층'],
     'correct_index': 3,
     'success': '집이 몇층인지 알아?', 'failure': '숫자가 크면 더 위에있는 층이야!'},
    
    {'id':13, 'type': 'text', 'title': '왼손 오른손 손가락을 다합치면 몇 개일까?',
     'options': ['3개','5개','10개','20개'],
     'correct_index': 2,
     'success': '발가락은 몇개게~?', 'failure': '양쪽손을 펴고 잘 봐봐'},
    
    {'id':14, 'type': 'image', 'title': '어떤 신호등일 때 길을 건널 거야?',
     'options': ['blue.jpg','green.jpg','red.jpg','orange.jpg'],
     'correct_index': 1,
     'success': '손도 들고 건널거지?', 'failure': '정답은 초록색이야! 까먹으면 안돼!'},
    
    {'id':15, 'type': 'image', 'title': '하늘을 날 수 있는건?',
     'options': ['airplane.jpg','forkcrane.jpg','car.jpg','train.jpg'],
     'correct_index': 0,
     'success': '비행기 타본거 기억나?', 'failure': '얘는 하늘을 날면 큰일나!'},
    
    {'id':16, 'type': 'text', 'title': '맛있는 과자가 생기면?',
     'options': ['정우가 다 먹기','정연이가 다 먹기','가족들이랑 나눠먹기','엄마아빠 몰래 숨기기'],
     'correct_index': 2,
     'success': '사이좋게 먹을거지?', 'failure': '그럼 안된다구~'},
    
    {'id':17, 'type': 'image', 'title': '뭘 많이 먹어야 튼튼해질까?',
     'options': ['mychu.jpg','broccoli.jpg','malangcow.jpg','homerunball.jpg'],
     'correct_index': 1,
     'success': '브로콜리 잘 먹을 수 있어?', 'failure': '과자는 아주 조금씩만 먹어야돼!'},

    {'id':18, 'type': 'image', 'title': '여기서 제일 큰 공은 뭐게?',
     'options': ['golf.jpg','baseball.jpg','football.jpg','basketball.jpg'],
     'correct_index': 3,
     'success': '농구공 손으로 들 수 있어?', 'failure': '본 적 없어? 잘 기억해봐봐!'},

    {'id':19, 'type': 'text', 'title': '헤어질 때 하는 영어 인사는?',
     'options': ['Hello','Thank you','Sorry','Bye Bye'],
     'correct_index': 3,
     'success': '영어로 내일 또봐~ 가 뭔지도 알아?', 'failure': '땡! 빠이빠이~'},

    {'id':20, 'type': 'text', 'title': '초등학교는 몇살에 가는거야? ',
     'options': ['6살','7살','8살','9살'],
     'correct_index': 2,
     'success': '학교에 빨리 가고 싶어?', 'failure': '두 살더 먹으면 돼!'},

    {'id':21, 'type': 'image', 'title': '밥 먹을 때 꼭 필요한건?',
     'options': ['spoon.jpg','phone.jpg','scissor.jpg','brush.jpg'],
     'correct_index': 0,
     'success': '손으로 먹는건 아니지?', 'failure': '이건 없어도 괜찮아~'},

    {'id':22, 'type': 'image', 'title': '틀린 그림을 찾아봐',
     'options': ['sanrio.jpg','sanrio.jpg','sanrio_fault.jpg','sanrio.jpg'],
     'correct_index': 2,
     'success': '어디어디가 달랐어?', 'failure': '한 장만 그림이 달라, 잘봐봐!'},

    {'id': 23, 'type': 'text', 'title': '횡단보도를 건널 때는 어떻게?',
     'options': ['빨리 뛰어가기','손을 들고 건너기','거꾸로 걸어가기','춤추면서 건너기'],
     'correct_index': 1,
     'success': '차를 잘 보고 손을 들면 돼', 'failure': '횡단보도에선 장난치면 안돼~'},

    {'id':24, 'type': 'image', 'title': '틀린 그림을 찾아봐',
     'options': ['mini.jpg','mini_fault.jpg','mini.jpg','mini.jpg'],
     'correct_index': 1,
     'success': '어디어디가 달랐어?', 'failure': '한 장만 그림이 달라, 잘봐봐!'},
]
IMAGE_DIR = "static/images"

# ----------------- 추가된 부분 시작 -----------------
# 퀴즈 목록이 10개가 안 될 경우를 대비해 min(10, len(QUIZZES))로 설정합니다.
NUM_QUESTIONS = min(10, len(QUIZZES)) 

# 처음 시작할 때 전체 QUIZZES에서 랜덤으로 NUM_QUESTIONS 개수를 뽑아 세션에 저장합니다.
if 'current_quizzes' not in st.session_state:
    st.session_state.current_quizzes = random.sample(QUIZZES, NUM_QUESTIONS)
# ----------------- 추가된 부분 끝 -------------------

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

[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}

[data-testid="stForm"] > div:first-child {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 12px !important;
    padding: 2px !important;
}

[data-testid="stFormSubmitButton"] {
    width: 100% !important;
}

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
    # 전체 QUIZZES 대신 랜덤으로 뽑힌 current_quizzes를 사용합니다.
    current_q = st.session_state.current_quizzes[st.session_state.quiz_idx]
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
    
    # 길이가 current_quizzes 기준이 되도록 수정
    if st.session_state.quiz_idx < len(st.session_state.current_quizzes) - 1:
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
    # 현재 퀴즈를 세션의 current_quizzes에서 가져옵니다.
    current_q = st.session_state.current_quizzes[st.session_state.quiz_idx]
    total_q = len(st.session_state.current_quizzes)
    
    st.progress(st.session_state.quiz_idx / total_q)
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
                🌟 {len(st.session_state.current_quizzes)}문제 중 {st.session_state.score}개 정답! 🌟
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 다시하기 버튼을 누르면 새로운 10개의 문제를 다시 뽑도록 갱신합니다.
    if st.button("처음부터 다시 할래", key="restart",
                 use_container_width=True, type="secondary"):
        st.session_state.quiz_idx   = 0
        st.session_state.score      = 0
        st.session_state.complete   = False
        st.session_state.img_chosen = None
        st.session_state.txt_chosen = None
        # 다시하기 클릭 시 새로운 랜덤 문제 세트 구성
        st.session_state.current_quizzes = random.sample(QUIZZES, NUM_QUESTIONS)
        st.rerun()
