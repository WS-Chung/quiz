import streamlit as st
import time
import os
import base64

# --- 1. 페이지 설정 및 제목 ---
st.set_page_config(page_title="정연이 정우 퀴즈풀기", page_icon="⭐", layout="centered")

# --- 2. 이미지 Base64 변환 함수 (버튼 배경용) ---
def get_image_base64(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    except:
        return ""

# 현재 경로 설정
img_dir = os.path.join(os.path.dirname(__file__), 'static', 'images')

# --- 3. 커스텀 CSS (강력한 디자인 제어) ---
st.markdown("""
    <style>
    /* 전체 컨텐츠 중앙 정렬 */
    .main .block-container {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    }

    /* 모든 버튼 규격 통일 (이미지/텍스트 공통) */
    div.stButton > button {
        width: 320px !important;
        height: 240px !important;
        border-radius: 30px !important;
        border: 6px solid #667eea !important;
        background-color: white;
        color: #667eea;
        font-size: 35px !important;
        font-weight: bold !important;
        transition: all 0.3s ease;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    /* 이미지 버튼 전용 (배경으로 이미지 삽입) */
    [data-testid="stBaseButton-secondary"] {
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        color: transparent !important; /* 텍스트 숨김 */
    }

    /* 버튼 호버 효과 */
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
        border-color: #764ba2 !important;
    }

    /* 페이드 애니메이션 메시지 박스 */
    .result-msg {
        position: fixed;
        top: 50%; left: 50%; transform: translate(-50%, -50%);
        padding: 40px; border-radius: 30px;
        font-size: 40px; font-weight: bold; text-align: center;
        z-index: 9999; width: 80%;
        animation: fadeInOut 2.5s forwards;
    }
    .correct { background-color: #90EE90; color: #2d5016; border: 8px solid #2d5016; }
    .error { background-color: #FFB6C1; color: #8b0000; border: 8px solid #8b0000; }

    @keyframes fadeInOut {
        0% { opacity: 0; transform: translate(-50%, -40%); }
        20% { opacity: 1; transform: translate(-50%, -50%); }
        80% { opacity: 1; }
        100% { opacity: 0; }
    }

    /* 문제 타이틀 크게 */
    h3 { font-size: 45px !important; color: #333; margin-bottom: 30px !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. 퀴즈 데이터 ---
QUIZZES = [
    {'id': 1, 'type': 'image', 'title': '불을 끄는 소방차는?', 'options': ['police.jpg', '119.jpg', 'kids.jpg', 'truck.jpg'], 'correct': 1, 's': '딩동댕! 🎉 소방차 최고!', 'f': '땡! 소방차는 빨간색!'},
    {'id': 2, 'type': 'image', 'title': '왕자핑을 찾아봐!', 'options': ['princeping.jpg', 'auroraping.jpg', 'heartsping.jpg', 'fixping.jpg'], 'correct': 0, 's': '맞았어! 🎉 왕자핑이야!', 'f': '땡! 왕자핑은 남자아이!'},
    {'id': 3, 'type': 'image', 'title': '아빠차 쏘렌토는?', 'options': ['tucson.jpg', 'koleos.jpg', 'gwagon.jpg', 'sorrento.jpg'], 'correct': 3, 's': '맞았어! 🎉 쏘렌토 최고!', 'f': '땡! 아빠차는 쏘렌토!'},
    {'id': 4, 'type': 'text', 'title': '아빠의 엄마는?', 'options': ['송도할머니', '수지할머니', '이모', '선생님'], 'correct': 0, 's': '딩동댕! 🎉 송도할머니!', 'f': '땡! 잘 생각해보자~'},
    {'id': 5, 'type': 'text', 'title': '엄마의 아빠는?', 'options': ['송도할아버지', '수지할아버지', '아저씨', '고모부'], 'correct': 1, 's': '딩동댕! 🎉 수지할아버지!', 'f': '땡! 수지할아버지야!'},
    {'id': 6, 'type': 'text', 'title': '딸기의 색깔은?', 'options': ['노랑', '초록', '빨강', '파랑'], 'correct': 2, 's': '맞았어! 🎉 빨간 딸기!', 'f': '땡! 딸기는 빨강색!'},
    {'id': 7, 'type': 'text', 'title': '집에 오면 뭐 할까?', 'options': ['과자먹기', '유튜브', '손씻기', '춤추기'], 'correct': 2, 's': '딩동댕! 🎉 손씻기 최고!', 'f': '땡! 손부터 씻어야해!'}
]

if 'idx' not in st.session_state:
    st.session_state.idx, st.session_state.score, st.session_state.comp = 0, 0, False

# 제목
st.markdown("<h1 style='text-align: center; color: #667eea; font-size: 50px;'>정연이 정우 퀴즈</h1>", unsafe_allow_html=True)

if not st.session_state.comp:
    q = QUIZZES[st.session_state.idx]
    st.progress((st.session_state.idx) / len(QUIZZES))
    st.markdown(f"### {q['title']}")

    # 버튼 레이아웃
    col1, col2 = st.columns(2)
    cols = [col1, col2, col1, col2]
    sel = None

    for i, opt in enumerate(q['options']):
        with cols[i]:
            if q['type'] == 'image':
                b64 = get_image_base64(os.path.join(img_dir, opt))
                # 이미지 버튼 스타일 주입 (해당 버튼의 배경을 이미지로 설정)
                st.markdown(f"<style>div[data-testid='stVerticalBlockBorderGui'] div.stButton:nth-child({(i%2)+1}) button {{ background-image: url(data:image/jpeg;base64,{b64}); }}</style>", unsafe_allow_html=True)
                if st.button(f" ", key=f"img_{st.session_state.idx}_{i}"):
                    sel = i
            else:
                if st.button(opt, key=f"txt_{st.session_state.idx}_{i}"):
                    sel = i

    if sel is not None:
        if sel == q['correct']:
            st.markdown(f'<div class="result-msg correct">{q["s"]}</div>', unsafe_allow_html=True)
            st.balloons(); st.session_state.score += 1
        else:
            st.markdown(f'<div class="result-msg error">{q["f"]}</div>', unsafe_allow_html=True)
        
        time.sleep(2.2)
        if st.session_state.idx < len(QUIZZES) - 1: st.session_state.idx += 1
        else: st.session_state.comp = True
        st.rerun()

else:
    st.balloons()
    st.markdown(f'<div class="result-msg correct" style="position:static; animation:none; margin-bottom:20px;">모든 퀴즈 끝!<br>{len(QUIZZES)}문제 중 {st.session_state.score}개 정답!</div>', unsafe_allow_html=True)
    
    # 다시하기 버튼을 중앙에 배치하기 위해 컬럼 사용
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        if st.button("처음부터 다시 하기"):
            st.session_state.idx, st.session_state.score, st.session_state.comp = 0, 0, False
            st.rerun()
