import streamlit as st
import time
import base64
import os
from PIL import Image

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="정연이 정우 퀴즈풀기", page_icon="⭐", layout="centered")

# --- 2. 퀴즈 데이터 (기존 데이터 유지) ---
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
     'success': '맞았어! 🎉 아빠차 이름은 쏘렌토야', 'failure': '땡! 다 비슷하게 생겼지?'}
    # ... 텍스트 퀴즈는 생략 (기존 데이터와 동일하게 작동합니다)
]
# 텍스트 퀴즈 데이터 추가 (기존 코드와 동일)
QUIZZES += [
    {'id': 4, 'type': 'text', 'title': '아빠의 엄마는 누구~게?', 'options': ['송도할머니','수지할머니','이모','돌봄선생님'], 'correct_index': 0, 'success': '딩동댕! 🎉 송도할머니야!', 'failure': '땡! 잘 생각해 보자~'},
    {'id': 5, 'type': 'text', 'title': '엄마의 아빠는 누구~게?', 'options': ['송도할아버지','수지할아버지','깜깜아저씨','고모부'], 'correct_index': 1, 'success': '딩동댕! 🎉 수지할아버지야!', 'failure': '땡! 엄마의 아빠는 누구지?'},
    {'id': 6, 'type': 'text', 'title': '딸기의 색깔은?', 'options': ['노랑','초록','빨강','파랑'], 'correct_index': 2, 'success': '맞았어! 🎉 딸기는 빨간색이야!', 'failure': '땡! 딸기는 빨간색이야~'},
    {'id': 7, 'type': 'text', 'title': '밖에서 놀고 집에오면 뭐부터 해야할까?', 'options': ['과자 먹기','유튜브 보기','손씻기','춤추기'], 'correct_index': 2, 'success': '딩동댕! 🎉 손을 깨끗이 씻자!', 'failure': '땡! 손 안 씻으면 아야해요!'}
]

# --- 3. 세션 상태 초기화 ---
for key, val in [('quiz_idx', 0), ('score', 0), ('complete', False), ('chosen_idx', None)]:
    if key not in st.session_state:
        st.session_state[key] = val

# --- 4. 경로 및 이미지 로드 함수 ---
IMAGE_DIR = "static/images"

def get_image(filename):
    """이미지 파일이 있는지 확인하고 로드합니다."""
    img_path = os.path.join(IMAGE_DIR, filename)
    if os.path.exists(img_path):
        return Image.open(img_path)
    else:
        # 이미지가 없을 경우 빈 이미지 생성 (에러 방지)
        return Image.new('RGB', (300, 300), color=(240, 240, 240))

# --- 5. 커스텀 CSS (카드형 디자인) ---
st.markdown("""
<style>
    /* 전체 컨테이너 정렬 */
    .main .block-container { max-width: 800px; padding-top: 2rem; }

    /* 이미지 스타일: 버튼과 붙어 보이게 테두리 설정 */
    .stImage > img {
        border: 4px solid #d0d0d0;
        border-bottom: none !important;
        border-radius: 20px 20px 0 0 !important;
        object-fit: cover;
        height: 250px !important;
    }

    /* 선택된 이미지의 테두리 색상 변경 */
    .selected-img > div > div > img {
        border-color: #667eea !important;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
    }

    /* 이미지 바로 아래 버튼 스타일 */
    div[data-testid="stButton"] > button {
        width: 100% !important;
        border-radius: 0 0 20px 20px !important;
        border: 4px solid #d0d0d0 !important;
        border-top: none !important;
        height: 60px !important;
        font-size: 20px !important;
        background-color: white !important;
        margin-top: -5px !important;
    }

    /* 선택된 버튼 스타일 */
    .selected-btn div[data-testid="stButton"] > button {
        background-color: #667eea !important;
        color: white !important;
        border-color: #667eea !important;
    }

    /* 확인 버튼 스타일 */
    .confirm-btn div[data-testid="stButton"] > button {
        border-radius: 50px !important;
        height: 80px !important;
        font-size: 28px !important;
        background-color: #667eea !important;
        color: white !important;
        margin-top: 30px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 6. 퀴즈 로직 ---
def next_quiz(selected_idx):
    current_q = QUIZZES[st.session_state.quiz_idx]
    if selected_idx == current_q['correct_index']:
        st.success(current_q['success'])
        st.balloons()
        st.session_state.score += 1
        time.sleep(2)
    else:
        st.error(current_q['failure'])
        time.sleep(2)
    
    st.session_state.chosen_idx = None
    if st.session_state.quiz_idx < len(QUIZZES) - 1:
        st.session_state.quiz_idx += 1
    else:
        st.session_state.complete = True
    st.rerun()

st.markdown(f"<h1 style='text-align:center; color:#667eea;'>정연이 정우 퀴즈풀기 ⭐</h1>", unsafe_allow_html=True)

if not st.session_state.complete:
    current_q = QUIZZES[st.session_state.quiz_idx]
    st.progress(st.session_state.quiz_idx / len(QUIZZES))
    st.markdown(f"<h2 style='text-align:center;'>Q{st.session_state.quiz_idx+1}. {current_q['title']}</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    cols = [col1, col2, col1, col2]

    # 선택지 렌더링
    for i, option in enumerate(current_q['options']):
        with cols[i]:
            is_selected = (st.session_state.chosen_idx == i)
            
            if current_q['type'] == 'image':
                # 1. 이미지 표시 (CSS 클래스로 선택 효과 부여)
                img_container = st.container()
                if is_selected:
                    img_container.markdown('<div class="selected-img">', unsafe_allow_html=True)
                img_container.image(get_image(option), use_container_width=True)
                if is_selected:
                    img_container.markdown('</div>', unsafe_allow_html=True)

                # 2. 이미지 바로 아래 선택 버튼
                btn_label = "이거야! ✅" if is_selected else f"{i+1}번 선택"
                btn_container = st.container()
                if is_selected:
                    btn_container.markdown('<div class="selected-btn">', unsafe_allow_html=True)
                if btn_container.button(btn_label, key=f"btn_{st.session_state.quiz_idx}_{i}", use_container_width=True):
                    st.session_state.chosen_idx = i
                    st.rerun()
                if is_selected:
                    btn_container.markdown('</div>', unsafe_allow_html=True)
            else:
                # 텍스트 퀴즈 버튼
                btn_type = "primary" if is_selected else "secondary"
                if st.button(option, key=f"txt_{st.session_state.quiz_idx}_{i}", use_container_width=True, type=btn_type):
                    st.session_state.chosen_idx = i
                    st.rerun()

    # 확인 버튼
    st.markdown('<div class="confirm-btn">', unsafe_allow_html=True)
    if st.button("✅ 이걸로 결정했어요!", use_container_width=True, disabled=(st.session_state.chosen_idx is None)):
        next_quiz(st.session_state.chosen_idx)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # 결과 화면 (기존과 동일)
    st.balloons()
    st.markdown(f"""
        <div style="text-align:center; background:#f0f2f6; padding:40px; border-radius:20px;">
            <h1 style="font-size:50px;">🎉 퀴즈 끝! 🎉</h1>
            <h2>{len(QUIZZES)}문제 중 {st.session_state.score}개 정답!</h2>
        </div>
    """, unsafe_allow_html=True)
    if st.button("다시 하기 🔄", use_container_width=True, type="primary"):
        st.session_state.quiz_idx = 0
        st.session_state.score = 0
        st.session_state.complete = False
        st.session_state.chosen_idx = None
        st.rerun()
