import streamlit as st
import time

# 1. 페이지 기본 설정 및 제목
st.set_page_config(page_title="정연이 정우 퀴즈풀기", page_icon="⭐", layout="centered")

# CSS로 디자인 살짝 입히기 (폰트 크기 및 버튼 스타일)
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 150px;
        font-size: 24px !important;
        font-weight: bold;
        border-radius: 20px;
    }
    .main-title {
        font-size: 40px;
        color: #667eea;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 퀴즈 데이터 정의 (기존 데이터 유지)
QUIZZES = [
    {
        'id': 1, 'type': 'image', 'title': '불을 끄는 소방관이 타고 다니는 차는 뭘까?',
        'options': ['police.jpg', '119.jpg', 'kids.jpg', 'truck.jpg'],
        'correct_index': 1, 'success': '딩동댕! 🎉 소방차를 어떻게 알았지?', 'failure': '땡! 소방차 빨간색이야!'
    },
    {
        'id': 2, 'type': 'image', 'title': '이 중에 왕자핑이 누구~게?',
        'options': ['princeping.jpg', 'auroraping.jpg', 'heartsping.jpg', 'fixping.jpg'],
        'correct_index': 0, 'success': '맞았어! 🎉 왕자핑을 잘 찾았어', 'failure': '땡! 왕자핑은 하얀색 머리 남자아이!'
    },
    {
        'id': 3, 'type': 'image', 'title': '아빠차를 찾아봐!',
        'options': ['tucson.jpg', 'koleos.jpg', 'gwagon.jpg', 'sorrento.jpg'],
        'correct_index': 3, 'success': '맞았어! 🎉 아빠차 이름은 쏘렌토야', 'failure': '땡! 다 비슷하게 생겼지?'
    },
    {
        'id': 4, 'type': 'text', 'title': '아빠의 엄마는 누구~게?',
        'options': ['송도할머니', '수지할머니', '이모', '돌봄선생님'],
        'correct_index': 0, 'success': '딩동댕! 🎉 송도할머니야!', 'failure': '땡! 잘 생각해 보자~'
    },
    {
        'id': 5, 'type': 'text', 'title': '엄마의 아빠는 누구~게?',
        'options': ['송도할아버지', '수지할아버지', '깜깜아저씨', '고모부'],
        'correct_index': 1, 'success': '딩동댕! 🎉 수지할아버지야!', 'failure': '땡! 엄마의 아빠는 누구지?'
    },
    {
        'id': 6, 'type': 'text', 'title': '딸기의 색깔은?',
        'options': ['노랑', '초록', '빨강', '파랑'],
        'correct_index': 2, 'success': '맞았어! 🎉 딸기는 빨간색이야!', 'failure': '땡! 딸기는 빨간색이야~'
    },
    {
        'id': 7, 'type': 'text', 'title': '밖에서 놀고 집에오면 뭐부터 해야할까?',
        'options': ['과자 먹기', '유튜브 보기', '손씻기', '춤추기'],
        'correct_index': 2, 'success': '딩동댕! 🎉 손을 깨끗이 씻자!', 'failure': '땡! 손 안 씻으면 아야해요!'
    }
]

# 3. 세션 상태(Session State) 초기화 (앱의 기억 장치)
if 'quiz_idx' not in st.session_state:
    st.session_state.quiz_idx = 0
    st.session_state.score = 0
    st.session_state.complete = False

# 4. 화면 구성
st.markdown(f"<div class='main-title'>정연이 정우 퀴즈풀기</div>", unsafe_allow_html=True)

if not st.session_state.complete:
    current_q = QUIZZES[st.session_state.quiz_idx]
    
    # 진행바
    progress = (st.session_state.quiz_idx) / len(QUIZZES)
    st.progress(progress)
    
    st.subheader(f"Q{st.session_state.quiz_idx + 1}. {current_q['title']}")
    
    # 4지 선다형 레이아웃 (2x2 그리드)
    col1, col2 = st.columns(2)
    cols = [col1, col2, col1, col2]
    
    for i, option in enumerate(current_q['options']):
        with cols[i]:
            if current_q['type'] == 'image':
                # 이미지 출력
                st.image(f"static/images/{option}", use_container_width=True)
                if st.button(f"선택 {i+1}", key=f"btn_{i}"):
                    if i == current_q['correct_index']:
                        st.success(current_q['success'])
                        st.balloons() # 정답 축하 풍선!
                        st.session_state.score += 1
                        time.sleep(2)
                    else:
                        st.error(current_q['failure'])
                        time.sleep(2)
                    
                    # 다음 문제로 이동 로직
                    if st.session_state.quiz_idx < len(QUIZZES) - 1:
                        st.session_state.quiz_idx += 1
                    else:
                        st.session_state.complete = True
                    st.rerun()
            else:
                # 텍스트 버튼 출력
                if st.button(option, key=f"btn_txt_{i}"):
                    if i == current_q['correct_index']:
                        st.success(current_q['success'])
                        st.balloons()
                        st.session_state.score += 1
                        time.sleep(2)
                    else:
                        st.error(current_q['failure'])
                        time.sleep(2)
                        
                    if st.session_state.quiz_idx < len(QUIZZES) - 1:
                        st.session_state.quiz_idx += 1
                    else:
                        st.session_state.complete = True
                    st.rerun()

else:
    # 5. 결과 화면
    st.balloons()
    st.success("모든 퀴즈를 다 풀었어! 얘들아 정말 잘했어! 🌟")
    st.markdown(f"### 🌟 {len(QUIZZES)}문제 중 {st.session_state.score}개를 맞혔어! 🌟")
    
    if st.button("처음부터 다시 하기"):
        st.session_state.quiz_idx = 0
        st.session_state.score = 0
        st.session_state.complete = False
        st.rerun()