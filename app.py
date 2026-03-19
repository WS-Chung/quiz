import streamlit as st
import time
from PIL import Image
from streamlit_image_select import image_select

# ─────────────────────────────────────────
# 1. 페이지 설정
# ─────────────────────────────────────────
st.set_page_config(page_title="정연이 정우 퀴즈풀기", page_icon="⭐", layout="centered")

# ─────────────────────────────────────────
# 2. 퀴즈 데이터
# ─────────────────────────────────────────
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

# ─────────────────────────────────────────
# 3. 세션 상태
# ─────────────────────────────────────────
for key, val in [('quiz_idx', 0), ('score', 0), ('complete', False),
                 ('img_chosen', None), ('txt_chosen', None), ('img_clicked', False)]:
    if key not in st.session_state:
        st.session_state[key] = val

# ─────────────────────────────────────────
# 4. 이미지 로드
# ─────────────────────────────────────────
@st.cache_resource
def load_image(filename: str) -> Image.Image:
    img = Image.open(f"{IMAGE_DIR}/{filename}").convert("RGB")
    return img.resize((300, 220), Image.LANCZOS)

# ─────────────────────────────────────────
# 5. CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
/* ── 기본 레이아웃 ── */
.main .block-container {
    max-width: 760px;
    margin: 0 auto;
    padding-top: 1rem;
}

/* ── 풍선 절반 ── */
iframe[title="st_balloons.balloons"] {
    transform: scale(0.5) !important;
    transform-origin: center center !important;
}

/* ══════════════════════════════════════
   [A] 텍스트 선택지 버튼 — secondary (미선택 상태)
   ══════════════════════════════════════ */
button[data-testid="stBaseButton-secondary"] {
    height: 110px !important;
    font-size: 28px !important;
    font-weight: bold !important;
    border-radius: 16px !important;
    border: 4px solid #667eea !important;
    background-color: white !important;
    color: #667eea !important;
    white-space: normal !important;
    word-break: keep-all !important;
    line-height: 1.3 !important;
    transition: border-color 0.15s, color 0.15s !important;
}
button[data-testid="stBaseButton-secondary"] p {
    font-size: 28px !important;
    font-weight: bold !important;
    line-height: 1.3 !important;
    color: inherit !important;
}
button[data-testid="stBaseButton-secondary"]:hover {
    background-color: #f5f5ff !important;
}

/* ── 선택된 텍스트 버튼 — .selected-btn 클래스로 강조 ──
   실제로는 Python에서 label에 마커를 넣어 구분하고,
   아래 CSS는 진한 분홍색 테두리+텍스트로 강조          */
button[data-testid="stBaseButton-secondary"].selected-option {
    border: 6px solid #e91e8c !important;
    color: #e91e8c !important;
    background-color: #fff0f8 !important;
}
button[data-testid="stBaseButton-secondary"].selected-option p {
    color: #e91e8c !important;
}

/* ══════════════════════════════════════
   [B] 확인 버튼 & 다시하기 버튼 — primary
   ★ 글자 크기: font-size 두 곳을 같이 수정 ★
   ══════════════════════════════════════ */
button[data-testid="stBaseButton-primary"] {
    height: 120px !important;
    font-size: 28px !important;
    font-weight: bold !important;
    border-radius: 50px !important;
    border: none !important;
    background-color: #667eea !important;
    color: white !important;
    box-shadow: 0 6px 18px rgba(102,126,234,0.45) !important;
    transition: background 0.2s, transform 0.2s, box-shadow 0.2s !important;
    white-space: normal !important;
    line-height: 1.3 !important;
}
button[data-testid="stBaseButton-primary"] p {
    font-size: 28px !important;
    font-weight: bold !important;
}
button[data-testid="stBaseButton-primary"]:hover {
    background-color: #5a6fd6 !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 24px rgba(102,126,234,0.55) !important;
}
button[data-testid="stBaseButton-primary"]:disabled {
    background-color: #b0b8f0 !important;
    cursor: not-allowed !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ══════════════════════════════════════
   image_select: 초기 빨간 테두리 강제 제거
   선택 시 테마 보라색 굵은 테두리
   ══════════════════════════════════════ */
/* iframe 안까지 접근 불가이므로 컴포넌트 감싸는 div에 오버레이 */
[data-testid="stIFrame"] { border: none !important; outline: none !important; }

/* image_select 컴포넌트 wrapper — 내부 iframe의 기본 선택 테두리를 숨김 */
div[data-testid="element-container"]:has(iframe) iframe {
    border: none !important;
}

/* ── 결과 메시지 ── */
.result-msg-box {
    padding: 22px;
    border-radius: 20px;
    font-size: 28px;
    font-weight: bold;
    margin: 18px auto;
    width: 100%;
    text-align: center;
    animation: fadeIn 0.4s ease-out;
}
.correct-box { background: #90EE90; color: #2d5016; }
.error-box   { background: #FFB6C1; color: #8b0000; }
@keyframes fadeIn { from{opacity:0} to{opacity:1} }

/* ── 결과 페이지 ── */
.result-section {
    background: #f0f2f6;
    border-radius: 20px;
    padding: 40px 30px;
    width: 100%;
    text-align: center;
    margin-bottom: 20px;
}
.result-text { font-weight: bold; color: #333; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 6. 정답 처리 함수
# ─────────────────────────────────────────
def process_answer(selected_idx: int):
    current_q = QUIZZES[st.session_state.quiz_idx]
    if selected_idx == current_q['correct_index']:
        st.markdown(
            f'<div class="result-msg-box correct-box">{current_q["success"]}</div>',
            unsafe_allow_html=True
        )
        st.balloons()
        st.session_state.score += 1
        time.sleep(2)
    else:
        st.markdown(
            f'<div class="result-msg-box error-box">{current_q["failure"]}</div>',
            unsafe_allow_html=True
        )
        time.sleep(2)

    st.session_state.img_chosen  = None
    st.session_state.txt_chosen  = None
    st.session_state.img_clicked = False
    if st.session_state.quiz_idx < len(QUIZZES) - 1:
        st.session_state.quiz_idx += 1
    else:
        st.session_state.complete = True
    st.rerun()

# ─────────────────────────────────────────
# 7. 메인 화면
# ─────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center;color:#667eea;'>정연이 정우 퀴즈풀기 ⭐</h1>",
    unsafe_allow_html=True
)

if not st.session_state.complete:
    current_q = QUIZZES[st.session_state.quiz_idx]
    st.progress(st.session_state.quiz_idx / len(QUIZZES))
    st.markdown(
        f"<h3 style='text-align:center;'>Q{st.session_state.quiz_idx+1}. {current_q['title']}</h3>",
        unsafe_allow_html=True
    )

    # ══════════════════════════════════════
    # 이미지 퀴즈
    # ══════════════════════════════════════
    if current_q['type'] == 'image':
        pil_images = [load_image(fn) for fn in current_q['options']]

        # image_select 는 항상 index=0 을 기본 선택으로 반환
        # → 첫 렌더링 여부를 img_clicked 로 추적
        chosen_img = image_select(
            label="",
            images=pil_images,
            use_container_width=True,
            return_value="original",
            key=f"imgsel_{st.session_state.quiz_idx}"
        )
        chosen_idx = next(
            (i for i, img in enumerate(pil_images) if chosen_img is img), 0
        )

        # 이전 렌더링의 chosen_idx 와 비교해서 달라지면 실제 클릭으로 판단
        prev_key = f"prev_img_{st.session_state.quiz_idx}"
        prev_idx = st.session_state.get(prev_key, -99)  # -99: 아직 한번도 렌더링 안됨

        if prev_idx == -99:
            # 최초 진입: 선택 없음 상태로 초기화
            st.session_state[prev_key] = chosen_idx
            st.session_state.img_clicked = False
            st.session_state.img_chosen  = None
        elif chosen_idx != prev_idx:
            # 이전과 다른 이미지 → 실제 클릭
            st.session_state[prev_key]   = chosen_idx
            st.session_state.img_clicked = True
            st.session_state.img_chosen  = chosen_idx
            st.rerun()

        img_ready = st.session_state.img_clicked
        img_sel   = st.session_state.img_chosen

        # 선택된 이미지 테두리: JS로 iframe 내부에 스타일 주입
        # (CSS로는 iframe 내부에 접근 불가)
        if img_ready and img_sel is not None:
            st.markdown(f"""
            <script>
            (function() {{
                // image_select iframe 을 찾아서 내부 선택 이미지 테두리를 테마색으로 교체
                var frames = window.parent.document.querySelectorAll('iframe');
                frames.forEach(function(f) {{
                    try {{
                        var imgs = f.contentDocument.querySelectorAll('img');
                        imgs.forEach(function(img, idx) {{
                            // 기존 빨간/초록 테두리 제거
                            img.style.outline = 'none';
                            img.style.border = idx === {img_sel}
                                ? '6px solid #667eea'
                                : '2px solid transparent';
                            img.style.borderRadius = '10px';
                        }});
                    }} catch(e) {{}}
                }});
            }})();
            </script>
            """, unsafe_allow_html=True)

        st.write("")
        if st.button(
            "✅ 이걸로 할래요!",
            key=f"confirm_img_{st.session_state.quiz_idx}",
            use_container_width=True,
            type="primary",
            disabled=not img_ready
        ):
            process_answer(img_sel)

    # ══════════════════════════════════════
    # 텍스트 퀴즈
    # ══════════════════════════════════════
    else:
        cur = st.session_state.txt_chosen
        col1, col2 = st.columns(2)
        cols = [col1, col2, col1, col2]

        # ── 선택 강조 CSS 주입 ──
        # data-key 가 DOM에 없으므로, 선택된 버튼과 미선택 버튼을 label로 구분
        # 선택된 버튼: label 앞에 고유 유니코드 마커(U+200B) 추가
        # CSS는 :nth-of-type 없이 label 텍스트로 구분 불가 → 대신 두 가지 버튼 타입 활용:
        #   미선택 → type="secondary" (보라 테두리)
        #   선택됨 → type="secondary" + 동적 CSS로 분홍 강조
        # 선택된 버튼의 순번(col 위치)으로 nth-child 를 정확히 계산해서 적용

        if cur is not None:
            # cur 이 0,2 → col1(1번째), cur 이 1,3 → col2(2번째)
            col_pos  = (cur % 2) + 1   # 1 or 2
            # col 내에서 몇 번째 버튼인지: 0,1 → 1번째 / 2,3 → 2번째
            btn_pos  = (cur // 2) + 1  # 1 or 2

            st.markdown(f"""
            <style>
            /* 선택된 버튼: col{col_pos} 의 {btn_pos}번째 secondary 버튼 */
            [data-testid="stHorizontalBlock"]
              > div:nth-child({col_pos})
              button[data-testid="stBaseButton-secondary"]:nth-of-type({btn_pos}) {{
                border: 6px solid #e91e8c !important;
                color: #e91e8c !important;
                background-color: #fff0f8 !important;
            }}
            [data-testid="stHorizontalBlock"]
              > div:nth-child({col_pos})
              button[data-testid="stBaseButton-secondary"]:nth-of-type({btn_pos}) p {{
                color: #e91e8c !important;
            }}
            </style>
            """, unsafe_allow_html=True)

        for i, option in enumerate(current_q['options']):
            with cols[i]:
                if st.button(
                    option,
                    key=f"txt_{st.session_state.quiz_idx}_{i}",
                    use_container_width=True,
                    type="secondary"
                ):
                    st.session_state.txt_chosen = i
                    st.rerun()

        st.write("")
        if st.button(
            "✅ 이걸로 할래요!",
            key=f"confirm_txt_{st.session_state.quiz_idx}",
            use_container_width=True,
            type="primary",
            disabled=(cur is None)
        ):
            process_answer(cur)

# ══════════════════════════════════════════
# 결과 페이지
# ══════════════════════════════════════════
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
    if st.button(
        "처음부터 다시 하기 🔄",
        key="restart",
        use_container_width=True,
        type="primary"
    ):
        st.session_state.quiz_idx   = 0
        st.session_state.score      = 0
        st.session_state.complete   = False
        st.session_state.img_chosen  = None
        st.session_state.txt_chosen  = None
        st.session_state.img_clicked = False
        st.rerun()
