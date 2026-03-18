import streamlit as st
import time
import os
from PIL import Image

# --- 1. 페이지 설정 및 제목 ---
st.set_page_config(page_title="정연이 정우 퀴즈풀기", page_icon="⭐", layout="centered")

# --- 2. 경로 보정 (클라우드 서버용) ---
# 현재 실행 중인 파일의 절대 경로를 기준으로 이미지를 찾습니다.
current_path = os.path.dirname(__file__)
img_dir = os.path.join(current_path, 'static', 'images')

# --- 3. 퀴즈 데이터 정의 ---
QUIZZES = [
    {'id': 1, 'type': 'image', 'title': '불을 끄는 소방관이 타고 다니는 차는 뭘까?', 'options': ['police.jpg', '119.jpg', 'kids.jpg', 'truck.jpg'], 'correct_index': 1, 'success': '딩동댕! 🎉 소방차를 어떻게 알았지?', 'failure': '땡! 소방차는 빨간색이야!'},
    {'id': 2, 'type': 'image', 'title': '이 중에 왕자핑이 누구~게?', 'options': ['princeping.jpg', 'auroraping.jpg', 'heartsping.jpg', 'fixping.jpg'], 'correct_index': 0, 'success': '맞았어! 🎉 왕자핑을 잘 찾았어', 'failure': '땡! 왕자핑은 남자아이야!'},
    {'id': 3, 'type': 'image', 'title': '아빠차를 찾아봐!', 'options': ['tucson.jpg', 'koleos.jpg', 'gwagon.jpg', 'sorrento.jpg'], 'correct_index': 3, 'success': '맞았어! 🎉 아빠차 이름은 쏘렌토야', 'failure': '땡! 다 비슷하게 생겼지?'},
    {'id': 4, 'type': 'text', 'title': '아빠의 엄마는 누구~게?', 'options': ['송도할머니', '수지할머니', '이모', '돌봄선생님'], 'correct_index': 0, 'success': '딩동댕! 🎉 송도할머니야!', 'failure': '땡! 잘 생각해 보자~'},
    {'id': 5, 'type': 'text', 'title': '엄마의 아빠는 누구~게?', 'options': ['송도할아버지', '수지할아버지', '깜깜아저씨', '고모부'], 'correct_index': 1, 'success': '딩동댕! 🎉 수지할아버지야!', 'failure': '땡! 엄마의 아빠는 누구지?'},
    {'id': 6, 'type': 'text', 'title': '딸기의 색깔은?', 'options': ['노랑', '초록', '빨강', '파랑'], 'correct_index': 2, 'success': '맞았어! 🎉 딸기는 빨간색이야!', 'failure': '땡! 딸기는 빨간색이야~'},
    {'id': 7, 'type': 'text', 'title': '밖에서 놀고 집에오면 뭐부터 해야할까?', 'options': ['과자 먹기', '유튜브 보기', '손씻기', '춤추기'], 'correct_index': 2, 'success': '딩동댕! 🎉 손을 깨끗이 씻자!', 'failure': '땡! 손 안 씻으면 아야해요!'}
]

if 'quiz_idx' not in st.session_state:
    st.session_state.quiz_idx, st.session_state.score, st.session_state.complete = 0, 0, False

# --- 4. 강력한 커스텀 CSS (이미지 버튼 전용) ---
st.markdown("""
    <style>
    /* 전체 중앙 정렬 */
    .main .block-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    /* 텍스트 버튼 및 이미지 하단 버튼 공통 스타일 */
    div.stButton > button {
        width: 100% !important;
        height: 100px !important;
        font-size: 30px !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        border: 4px solid #667eea !important;
        background-color: white !important;
        color: #667eea !important;
        margin-top: 0px !important;
    }

    /* 이미지 스타일 */
    .stImage > img {
        border-radius: 15px 15px 0 0 !important;
        border: 4px solid #667eea !important;
        border-bottom: none !important;
    }

    /* 결과 박스 중앙 정렬 */
    .result-box {
        padding: 25px;
        border-radius: 20px;
        font-size: 28px;
        font-weight: bold;
        margin: 20px 0;
        width: 100%;
        text-align: center;
    }
    .correct { background-color: #90EE90; color: #2d5016; }
    .error { background-color: #FFB6C1; color: #8b0000; }
    </style>
    """, unsafe_allow_html=True)

# 제목
st.markdown("<h1 style='text-align: center; color: #667eea;'>정연이 정우 퀴즈풀기</h1>", unsafe_allow_html=True)

if not st.session_state.complete:
    current_q = QUIZZES[st.session_state.quiz_idx]
    st.progress((st.session_state.quiz_idx) / len(QUIZZES))
    st.markdown(f"### Q{st.session_state.quiz_idx + 1}. {current_q['title']}")

    # 2x2 그리드
    col1, col2 = st.columns(2)
    cols = [col1, col2, col1, col2]
    
    selected_idx = None

    for i, option in enumerate(current_q['options']):
        with cols[i]:
            if current_q['type'] == 'image':
                # [이미지 로드 방식 개선] 엑스박스 방지를 위해 파일 존재 여부 확인 후 로드
                img_path = os.path.join(img_dir, option)
                try:
                    image = Image.open(img_path)
                    st.image(image, use_container_width=True)
                except:
                    st.error(f"이미지 없음: {option}")
                
                # 이미지 바로 아래에 텍스트 없는 빈 버튼 배치 (이미지 클릭 효과)
                if st.button(" ", key=f"img_btn_{i}"):
                    selected_idx = i
            else:
                # 텍스트 퀴즈 버튼
                st.write("") # 간격 맞춤용
                if st.button(option, key=f"txt_btn_{i}"):
                    selected_idx = i

    # 정답 체크 로직
    if selected_idx is not None:
        if selected_idx == current_q['correct_index']:
            st.markdown(f'<div class="result-box correct">{current_q["success"]}</div>', unsafe_allow_html=True)
            st.balloons()
            st.session_state.score += 1
            time.sleep(2)
        else:
            st.markdown(f'<div class="result-box error">{current_q["failure"]}</div>', unsafe_allow_html=True)
            time.sleep(2)
        
        if st.session_state.quiz_idx < len(QUIZZES) - 1:
            st.session_state.quiz_idx += 1
        else:
            st.session_state.complete = True
        st.rerun()

else:
    st.balloons()
    st.markdown(f'<div class="result-box correct">모든 퀴즈 끝! 정말 잘했어! 🌟<br>{len(QUIZZES)}문제 중 {st.session_state.score}개 정답!</div>', unsafe_allow_html=True)
    if st.button("처음부터 다시 하기"):
        st.session_state.quiz_idx, st.session_state.score, st.session_state.complete = 0, 0, False
        st.rerun()
