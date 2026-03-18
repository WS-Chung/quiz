import streamlit as st
import time
import os

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="정연이 정우 퀴즈풀기", page_icon="⭐", layout="centered")

# --- 2. 경로 설정 및 퀴즈 데이터 (메시지 완벽 보존) ---
img_dir = os.path.join(os.path.dirname(__file__), 'static', 'images')

QUIZZES = [
    {
        'id': 1, 'type': 'image', 'title': '불을 끄는 소방관이 타고 다니는 차는 뭘까?',
        'options': ['police.jpg', '119.jpg', 'kids.jpg', 'truck.jpg'],
        'correct': 1, 's': '딩동댕! 🎉 소방차를 어떻게 알았지?', 'f': '땡! 소방차 빨간색이야!'
    },
    {
        'id': 2, 'type': 'image', 'title': '이 중에 왕자핑이 누구~게?',
        'options': ['princeping.jpg', 'auroraping.jpg', 'heartsping.jpg', 'fixping.jpg'],
        'correct': 0, 's': '맞았어! 🎉 왕자핑을 잘 찾았어', 'f': '땡! 왕자핑은 하얀색 머리의 남자아이야! 다시 찾아볼까?'
    },
    {
        'id': 3, 'type': 'image', 'title': '아빠차를 찾아봐!',
        'options': ['tucson.jpg', 'koleos.jpg', 'gwagon.jpg', 'sorrento.jpg'],
        'correct': 3, 's': '맞았어! 🎉 어떻게 알았어? 차 이름도 알고있니?', 'f': '땡! 다 비슷하게 생겨서 잘 모르겠지? 아빠차 이름은 쏘렌토 야'
    },
    {
        'id': 4, 'type': 'text', 'title': '아빠의 엄마는 누구~게?',
        'options': ['송도할머니', '수지할머니', '이모', '돌봄선생님'],
        'correct': 0, 's': '딩동댕! 🎉 아빠가 엄마라고 부르는 사람은 송도할머니야!', 'f': '땡! 아빠가 엄마라고 부르는 사람이 누구지? 잘 생각해 보자'
    },
    {
        'id': 5, 'type': 'text', 'title': '엄마의 아빠는 누구~게?',
        'options': ['송도할아버지', '수지할아버지', '깜깜아저씨', '고모부'],
        'correct': 1, 's': '딩동댕! 🎉 엄마의 아빠는 수지할아버지야!', 'f': '땡! 엄마가 누구한테 아빠라고 부르는지 잘 생각해보자!'
    },
    {
        'id': 6, 'type': 'text', 'title': '딸기의 색깔은?',
        'options': ['노랑', '초록', '빨강', '파랑'],
        'correct': 2, 's': '맞았어! 🎉 딸기는 빨간색이야! 딸기 좋아해?', 'f': '땡! 딸기는 빨간색인데, 혹시 다른색깔 딸기를 본거야?'
    },
    {
        'id': 7, 'type': 'text', 'title': '밖에서 놀고 집에오면 뭐부터 해야할까?',
        'options': ['과자 먹기', '유튜브 보기', '손씻기', '춤추기'],
        'correct': 2, 's': '딩동댕! 🎉 정우랑 정연이는 손 잘 씻고 있지?', 'f': '자꾸 손을 안씻으면 아파서 병원에 가야 할지도 몰라'
    }
]

# 세션 상태 초기화
if 'idx' not in st.session_state:
    st.session_state.idx, st.session_state.score, st.session_state.comp = 0, 0, False

# --- 3. 커스텀 CSS (이미지 가시성 확보 및 하단 토스트) ---
st.markdown("""
    <style>
    /* 전체 중앙 정렬 */
    .main .block-container {
        display: flex; flex-direction: column; align-items: center;
    }

    /* 모든 버튼 규격 통일 (320px x 100px) */
    div.stButton > button {
        width: 100% !important;
        height: 100px !important;
        font-size: 32px !important;
        font-weight: bold !important;
        border-radius: 0 0 25px 25px !important; /* 아래만 둥글게 */
        border: 5px solid #667eea !important;
        border-top: none !important;
        background-color: white !important;
        color: #667eea !important;
    }

    /* 이미지 스타일 (버튼과 합쳐져 보이게) */
    .stImage > img {
        border: 5px solid #667eea !important;
        border-bottom: none !important;
        border-radius: 25px 25px 0 0 !important;
        height: 250px !important;
        object-fit: cover;
    }

    /* 하단 페이드 토스트 메시지 */
    .bottom-toast {
        position: fixed;
        bottom: 30px; left: 50%; transform: translateX(-50%);
        width: 80%; max-width: 600px;
        padding: 20px; border-radius: 20px;
        font-size: 24px; font-weight: bold; text-align: center;
        z-index: 9999;
        animation: fadeInOut 2.2s forwards;
    }
    .toast-correct { background-color: #90EE90; color: #2d5016; border: 4px solid #2d5016; }
    .toast-error { background-color: #FFB6C1; color: #8b0000; border: 4px solid #8b0000; }

    @keyframes fadeInOut {
        0% { opacity: 0; bottom: 10px; }
        15% { opacity: 1; bottom: 30px; }
        85% { opacity: 1; }
        100% { opacity: 0; bottom: 30px; }
    }

    /* 타이틀 및 텍스트 퀴즈 간격 조정 */
    .stMarkdown h1 { font-size: 50px !important; color: #667eea; text-align: center; }
    .stMarkdown h3 { font-size: 35px !important; text-align: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. 메인 화면 구성 ---
st.markdown("# 정연이 정우 퀴즈풀기")

if not st.session_state.comp:
    q = QUIZZES[st.session_state.idx]
    st.progress((st.session_state.idx) / len(QUIZZES))
    st.markdown(f"### Q{st.session_state.idx+1}. {q['title']}")

    # 2x2 그리드
    col1, col2 = st.columns(2)
    cols = [col1, col2, col1, col2]
    sel = None

    for i, opt in enumerate(q['options']):
        with cols[i]:
            if q['type'] == 'image':
                # 안전한 이미지 출력
                img_path = os.path.join(img_dir, opt)
                st.image(img_path, use_container_width=True)
                # 이미지 바로 밑에 '여기에요!' 버튼 배치 (글자 없이 공백도 가능하지만 아이들을 위해 번호 표시)
                if st.button(f"{i+1}번!", key=f"img_{i}"):
                    sel = i
            else:
                # 텍스트 퀴즈 (위쪽 테두리 다시 살림)
                st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
                if st.button(opt, key=f"txt_{i}"):
                    sel = i

    if sel is not None:
        if sel == q['correct']:
            st.markdown(f'<div class="bottom-toast toast-correct">{q["s"]}</div>', unsafe_allow_html=True)
            st.balloons()
            st.session_state.score += 1
        else:
            st.markdown(f'<div class="bottom-toast toast-error">{q["f"]}</div>', unsafe_allow_html=True)
        
        time.sleep(2.2)
        if st.session_state.idx < len(QUIZZES) - 1:
            st.session_state.idx += 1
        else:
            st.session_state.comp = True
        st.rerun()

else:
    # --- 5. 마지막 결과 페이지 (복원 및 중앙 정렬) ---
    st.balloons()
    st.markdown(f"""
        <div style="text-align: center; padding: 50px; background-color: #f0f2f6; border-radius: 30px; border: 5px solid #667eea; margin-top: 30px;">
            <h1 style="font-size: 60px;">🎉 퀴즈 끝! 🎉</h1>
            <h2 style="font-size: 40px; color: #333;">정말 잘했어! 얘들아!</h2>
            <h1 style="font-size: 55px; color: #667eea; margin-top: 20px;">🌟 {len(QUIZZES)}문제 중 {st.session_state.score}개 정답! 🌟</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("") # 간격
    if st.button("처음부터 다시 하기"):
        st.session_state.idx, st.session_state.score, st.session_state.comp = 0, 0, False
        st.rerun()
