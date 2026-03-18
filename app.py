import streamlit as st
import time
import base64
import os

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="정연이 정우 퀴즈풀기", page_icon="⭐", layout="centered")

# 로컬 이미지를 CSS 배경으로 쓰기 위한 함수
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# --- 2. 강력한 커스텀 CSS 적용 ---
st.markdown("""
    <style>
    /* 전체 컨텐츠 중앙 정렬 */
    .main .block-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }

    /* 모든 버튼(텍스트/이미지 하단)의 크기를 동일하게 고정 */
    div.stButton > button {
        width: 100% !important;
        height: 120px !important;  /* 버튼 높이 고정 */
        font-size: 35px !important; /* 텍스트 크게 */
        font-weight: bold !important;
        border-radius: 0 0 20px 20px !important; /* 아래쪽만 둥글게 */
        border: 3px solid #667eea !important;
        background-color: white !important;
        color: #667eea !important;
        margin-top: -5px !important; /* 이미지와 밀착 */
    }

    /* 이미지 스타일 고정 */
    .quiz-img {
        width: 100%;
        height: 250px; /* 이미지 높이 고정 */
        object-fit: cover;
        border-radius: 20px 20px 0 0; /* 위쪽만 둥글게 */
        border: 3px solid #667eea;
        border-bottom: none;
        cursor: pointer;
    }

    /* 결과 메시지 중앙 정렬 박스 */
    .result-box {
        padding: 20px;
        border-radius: 20px;
        font-size: 30px;
        font-weight: bold;
        margin: 20px auto;
        width: 100%;
        text-align: center;
        animation: fadeIn 0.5s;
    }
    .correct-box { background-color: #90EE90; color: #2d5016; }
    .error-box { background-color: #FFB6C1; color: #8b0000; }

    @keyframes fadeIn { from {opacity: 0;} to {opacity: 1;} }
    </style>
    """, unsafe_allow_html=True)

# 3. 퀴즈 데이터 (동일하게 유지)
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

# 제목 중앙 배치
st.markdown(f"<h1 style='text-align: center; color: #667eea;'>정연이 정우 퀴즈풀기</h1>", unsafe_allow_html=True)

if not st.session_state.complete:
    current_q = QUIZZES[st.session_state.quiz_idx]
    st.progress((st.session_state.quiz_idx) / len(QUIZZES))
    st.markdown(f"### Q{st.session_state.quiz_idx + 1}. {current_q['title']}")

    # 2x2 그리드 레이아웃
    col1, col2 = st.columns(2)
    cols = [col1, col2, col1, col2]
    
    selected_idx = None

    for i, option in enumerate(current_q['options']):
        with cols[i]:
            if current_q['type'] == 'image':
                # 이미지와 버튼을 하나의 세트로 구성
                img_path = f"static/images/{option}"
                img_base64 = get_base64_image(img_path)
                if img_base64:
                    st.markdown(f'<img src="data:image/jpeg;base64,{img_base64}" class="quiz-img">', unsafe_allow_html=True)
                
                # '선택'이라는 글자 대신 번호만 크게 표시하거나 빈 칸으로 둬서 이미지 클릭 유도
                if st.button(f"{i+1}번 보러가기", key=f"img_btn_{i}"):
                    selected_idx = i
            else:
                # 텍스트 퀴즈용 버튼 (이미지 퀴즈 버튼과 높이/너비를 CSS로 통일함)
                # 텍스트 버튼은 이미지가 없으므로 높이를 조금 더 키워서 균형을 맞춤
                st.markdown("<div style='height:150px;'></div>", unsafe_allow_html=True) # 위쪽 여백
                if st.button(option, key=f"txt_btn_{i}"):
                    selected_idx = i

    # 정답 체크 및 결과 표시 (중앙 정렬 커스텀 메시지)
    if selected_idx is not None:
        if selected_idx == current_q['correct_index']:
            st.markdown(f'<div class="result-box correct-box">{current_q["success"]}</div>', unsafe_allow_html=True)
            st.balloons()
            st.session_state.score += 1
            time.sleep(2)
        else:
            st.markdown(f'<div class="result-box error-box">{current_q["failure"]}</div>', unsafe_allow_html=True)
            time.sleep(2)
        
        if st.session_state.quiz_idx < len(QUIZZES) - 1:
            st.session_state.quiz_idx += 1
        else:
            st.session_state.complete = True
        st.rerun()

else:
    st.balloons()
    st.markdown(f'<div class="result-box correct-box">모든 퀴즈 끝! 정말 잘했어! 🌟<br> {len(QUIZZES)}문제 중 {st.session_state.score}개 정답!</div>', unsafe_allow_html=True)
    if st.button("처음부터 다시 하기"):
        st.session_state.quiz_idx, st.session_state.score, st.session_state.complete = 0, 0, False
        st.rerun()
