import streamlit as st
import time
import os

# --- 1. 페이지 설정 및 제목 ---
st.set_page_config(page_title="정연이 정우 퀴즈풀기", page_icon="⭐", layout="centered")

# --- 2. 퀴즈 데이터 정의 (기존 데이터 완벽 보존) ---
QUIZZES = [
    {'id': 1, 'type': 'image', 'title': '불을 끄는 소방관이 타고 다니는 차는 뭘까?', 'options': ['police.jpg', '119.jpg', 'kids.jpg', 'truck.jpg'], 'correct_index': 1, 'success': '딩동댕! 🎉 소방차를 어떻게 알았지?', 'failure': '땡! 소방차는 빨간색이야!'},
    {'id': 2, 'type': 'image', 'title': '이 중에 왕자핑이 누구~게?', 'options': ['princeping.jpg', 'auroraping.jpg', 'heartsping.jpg', 'fixping.jpg'], 'correct_index': 0, 'success': '맞았어! 🎉 왕자핑을 잘 찾았어', 'failure': '땡! 왕자핑은 남자아이야!'},
    {'id': 3, 'type': 'image', 'title': '아빠차를 찾아봐!', 'options': ['tucson.jpg', 'koleos.jpg', 'gwagon.jpg', 'sorrento.jpg'], 'correct_index': 3, 'success': '맞았어! 🎉 아빠차 이름은 쏘렌토야', 'failure': '땡! 다 비슷하게 생겼지?'},
    {'id': 4, 'type': 'text', 'title': '아빠의 엄마는 누구~게?', 'options': ['송도할머니', '수지할머니', '이모', '돌봄선생님'], 'correct_index': 0, 'success': '딩동댕! 🎉 송도할머니야!', 'failure': '땡! 잘 생각해 보자~'},
    {'id': 5, 'type': 'text', 'title': '엄마의 아빠는 누구~게?', 'options': ['송도할아버지', '수지할아버지', '깜깜아저씨', '고모부'], 'correct_index': 1, 'success': '딩동댕! 🎉 수지할아버지야!', 'failure': '땡! 엄마의 아빠는 누구지?'},
    {'id': 6, 'type': 'text', 'title': '딸기의 색깔은?', 'options': ['노랑', '초록', '빨강', '파랑'], 'correct_index': 2, 'success': '맞았어! 🎉 딸기는 빨간색이야!', 'failure': '땡! 딸기는 빨간색이야~'},
    {'id': 7, 'type': 'text', 'title': '밖에서 놀고 집에오면 뭐부터 해야할까?', 'options': ['과자 먹기', '유튜브 보기', '손씻기', '춤추기'], 'correct_index': 2, 'success': '딩동댕! 🎉 손을 깨끗이 씻자!', 'failure': '땡! 손 안 씻으면 아야해요!'}
]

# --- 3. 세션 상태 초기화 (앱의 기억 장치) ---
if 'quiz_idx' not in st.session_state:
    st.session_state.quiz_idx, st.session_state.score, st.session_state.complete = 0, 0, False

# --- 4. 강력한 커스텀 CSS 적용 (가장 중요 ⭐) ---
st.markdown("""
    <style>
    /* 전체 컨텐츠 중앙 정렬 고정 */
    .main .block-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }

    /* 이미지 스타일 고정 */
    .stImage > img {
        height: 250px !important;
        object-fit: cover;
        border-radius: 20px 20px 0 0 !important; /* 위쪽만 둥글게 */
        border: 4px solid #667eea !important;
        border-bottom: none !important;
    }

    /* 모든 버튼(텍스트/이미지 하단)의 크기를 동일하게 규격화 */
    div.stButton > button {
        width: 100% !important;
        height: 120px !important;  /* 버튼 높이 고정 */
        font-size: 35px !important; /* 텍스트 크게 */
        font-weight: bold !important;
        border-radius: 0 0 20px 20px !important; /* 아래쪽만 둥글게 */
        border: 4px solid #667eea !important;
        background-color: white !important;
        color: #667eea !important;
        margin-top: -5px !important; /* 이미지와 밀착 */
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #667eea !important;
        color: white !important;
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
    }

    /* 마지막 페이지 결과 영역 디자인 (테두리 제거, 배경색 평평하게) */
    .result-section {
        background-color: #f0f2f6;
        border-radius: 20px;
        padding: 40px;
        margin-bottom: 20px;
    }
    .result-text {
        font-weight: bold;
        color: #333;
    }

    /* 페이드 애니메이션 결과 메시지 박스 */
    .result-msg-box {
        padding: 20px;
        border-radius: 20px;
        font-size: 30px;
        font-weight: bold;
        margin: 20px auto;
        width: 100%;
        text-align: center;
        animation: fadeIn 0.5s ease-out;
    }
    .correct-box { background-color: #90EE90; color: #2d5016; }
    .error-box { background-color: #FFB6C1; color: #8b0000; }

    @keyframes fadeIn { from {opacity: 0;} to {opacity: 1;} }
    </style>
    """, unsafe_allow_html=True)

# --- 5. 화면 구성 및 로직 ---
# 제목 중앙 배치
st.markdown(f"<h1 style='text-align: center; color: #667eea;'>정연이 정우 퀴즈풀기</h1>", unsafe_allow_html=True)

if not st.session_state.complete:
    current_q = QUIZZES[st.session_state.quiz_idx]
    
    # 진행바
    progress = (st.session_state.quiz_idx) / len(QUIZZES)
    st.progress(progress)
    
    # 문제 제목 중앙 정렬
    st.markdown(f"<h3 style='text-align: center;'>Q{st.session_state.quiz_idx + 1}. {current_q['title']}</h3>", unsafe_allow_html=True)

    # 4지 선다형 레이아웃 (2x2 그리드)
    col1, col2 = st.columns(2)
    cols = [col1, col2, col1, col2]
    
    selected_idx = None

    for i, option in enumerate(current_q['options']):
        with cols[i]:
            if current_q['type'] == 'image':
                # 이미지 출력
                st.image(f"static/images/{option}", use_container_width=True)
                # 이미지 바로 밑에 공백 버튼 배치 (텍스트 제거 "", 대소문자 맞춤)
                if st.button("", key=f"img_btn_{i}"):
                    selected_idx = i
            else:
                # 텍스트 퀴즈 버튼 (CSS로 크기 규격화 완료)
                st.write("") # 간격 맞춤용
                if st.button(option, key=f"txt_btn_{i}"):
                    selected_idx = i

    # 정답 체크 및 결과 표시 (중앙 정렬 커스텀 메시지)
    if selected_idx is not None:
        if selected_idx == current_q['correct_index']:
            st.markdown(f'<div class="result-msg-box correct-box">{current_q["success"]}</div>', unsafe_allow_html=True)
            st.balloons()
            st.session_state.score += 1
            time.sleep(2)
        else:
            st.markdown(f'<div class="result-msg-box error-box">{current_q["failure"]}</div>', unsafe_allow_html=True)
            time.sleep(2)
        
        # 다음 문제로 이동
        if st.session_state.quiz_idx < len(QUIZZES) - 1:
            st.session_state.quiz_idx += 1
        else:
            st.session_state.complete = True
        st.rerun()

else:
    # --- 6. 마지막 결과 페이지 (복원 및 중앙 정렬) ---
    st.balloons()
    
    # 결과 영역 디자인 (테두리 제거, 평평한 배경색)
    st.markdown(f"""
        <div class="result-section">
            <h1 class="result-text" style="font-size: 50px;">🎉 퀴즈 끝! 🎉</h1>
            <h2 class="result-text" style="font-size: 30px;">정말 잘했어! 얘들아!</h2>
            <h1 class="result-text" style="font-size: 45px; color: #667eea; margin-top: 20px;">🌟 {len(QUIZZES)}문제 중 {st.session_state.score}개 정답! 🌟</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # '다시 하기' 버튼 중앙 정렬을 위해 컬럼 사용
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        st.write("") # 간격 맞춤용
        if st.button("처음부터 다시 하기"):
            st.session_state.quiz_idx, st.session_state.score, st.session_state.complete = 0, 0, False
            st.rerun()
