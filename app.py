import streamlit as st
import streamlit.components.v1 as components
import time
import base64
import io
@@ -57,6 +56,34 @@ def load_b64(filename: str) -> str:
iframe[title="st_balloons.balloons"] {
    transform: scale(0.5) !important; transform-origin: center center !important;
}

/* ── 이미지 카드: 클릭 가능한 label로 감쌈 ── */
.img-card-label {
    display: block;
    cursor: pointer;
    border-radius: 14px;
    overflow: hidden;
    border: 3px solid #d0d0d0;
    background: #f8f8f8;
    transition: border-color 0.15s, box-shadow 0.15s;
    margin-bottom: 4px;
}
.img-card-label:hover { border-color: #667eea; }
.img-card-label.selected {
    border: 5px solid #667eea;
    box-shadow: 0 0 0 3px rgba(102,126,234,0.2);
}
.img-card-label img {
    width: 100%;
    aspect-ratio: 1 / 1;
    object-fit: contain;
    display: block;
}

/* radio 완전히 숨김 */
div[data-testid="stRadio"] { display: none !important; }

/* ── 텍스트 선택지 버튼 ── */
button[data-testid="stBaseButton-secondary"],
button[data-testid="stBaseButton-primary"] {
    height: 110px !important; font-size: 28px !important; font-weight: bold !important;
@@ -98,74 +125,6 @@ def load_b64(filename: str) -> str:
</style>
""", unsafe_allow_html=True)

def make_image_grid_html(b64_list: list, selected: int) -> str:
    """
    4개 이미지를 2x2 그리드로 렌더링하는 HTML 컴포넌트.
    이미지 클릭 → postMessage로 인덱스를 부모(Streamlit)에 전달.
    선택된 이미지는 보라색 테두리 표시.
    """
    imgs_js = "[" + ",".join(f'"{b}"' for b in b64_list) + "]"
    sel_js  = str(selected) if selected is not None else "-1"

    return f"""
    <style>
      body {{ margin:0; padding:0; background:transparent; }}
      .grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        padding: 4px;
      }}
      .card {{
        border: 3px solid #d0d0d0;
        border-radius: 14px;
        overflow: hidden;
        cursor: pointer;
        background: #f8f8f8;
        transition: border-color 0.15s, box-shadow 0.15s;
        aspect-ratio: 1 / 1;
        display: flex;
        align-items: center;
        justify-content: center;
      }}
      .card:hover {{ border-color: #667eea; }}
      .card.selected {{
        border: 5px solid #667eea;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.2);
      }}
      .card img {{
        width: 100%;
        height: 100%;
        object-fit: contain;
        display: block;
        pointer-events: none;
      }}
    </style>
    <div class="grid" id="grid"></div>
    <script>
      const images  = {imgs_js};
      const initSel = {sel_js};
      let selected  = initSel;

      const grid = document.getElementById('grid');
      images.forEach((src, idx) => {{
        const card = document.createElement('div');
        card.className = 'card' + (idx === initSel ? ' selected' : '');
        const img = document.createElement('img');
        img.src = src;
        card.appendChild(img);
        card.addEventListener('click', () => {{
          document.querySelectorAll('.card').forEach(c => c.classList.remove('selected'));
          card.classList.add('selected');
          selected = idx;
          // Streamlit 부모에게 선택 인덱스 전달
          window.parent.postMessage({{type: 'img_select', idx: idx}}, '*');
        }});
        grid.appendChild(card);
      }});
    </script>
    """

def process_answer(selected_idx: int):
    current_q = QUIZZES[st.session_state.quiz_idx]
    if selected_idx == current_q['correct_index']:
@@ -200,53 +159,81 @@ def process_answer(selected_idx: int):
        img_sel = st.session_state.img_chosen
        b64_list = [load_b64(fn) for fn in current_q['options']]

        # components.html: 완전한 HTML/JS 환경 — 이미지 클릭 100% 동작
        # postMessage 로 선택 인덱스를 전달하지만,
        # Streamlit은 postMessage 수신이 불가 → 대신 숨겨진 버튼 4개로 수신
        # 가장 안정적: 이미지 그리드 + 아래 숨겨진 버튼을 JS로 클릭
        html_code = make_image_grid_html(b64_list, img_sel)
        # ── 핵심 구조 ──
        # 1. st.radio를 CSS로 완전히 숨김 (값 저장 역할만)
        # 2. 이미지를 <label for="radio_id"> 로 감쌈
        #    → 이미지 클릭 = label 클릭 = radio 선택 = Streamlit rerun
        # 3. 선택된 이미지는 보라 테두리

        # 숨겨진 선택 버튼 (JS가 클릭, 사용자 눈에는 안 보임)
        st.markdown("""
        <style>
        .hbtn-row { height: 0 !important; overflow: hidden; }
        .hbtn-row button { height: 0 !important; min-height: 0 !important;
            padding: 0 !important; border: none !important; visibility: hidden !important; }
        </style>
        """, unsafe_allow_html=True)
        qidx = st.session_state.quiz_idx

        # 숨겨진 radio (0~3 선택)
        radio_val = st.radio(
            "img_radio",
            options=[0, 1, 2, 3],
            index=img_sel if img_sel is not None else 0,
            key=f"radio_{qidx}",
            horizontal=True
        )

        hcols = st.columns(4)
        hbtns = []
        st.markdown('<div class="hbtn-row">', unsafe_allow_html=True)
        for i in range(4):
            with hcols[i]:
                hbtns.append(st.button(f"h{i}", key=f"hb_{st.session_state.quiz_idx}_{i}"))
        st.markdown('</div>', unsafe_allow_html=True)
        # radio가 처음 로딩될 때 img_chosen=None이면 선택 안 된 상태 유지
        # radio의 초기값(0)이 자동 선택되는 문제 → sentinel로 구분
        if img_sel is None:
            # 아직 아무것도 선택 안 한 상태 → radio 값 무시
            pass
        elif radio_val != img_sel:
            st.session_state.img_chosen = radio_val
            st.rerun()

        # radio input 의 실제 DOM id 를 알아내기 위해
        # label for 속성에 radio input id 를 연결해야 함
        # → Streamlit radio 의 input id 패턴: "radio_{key}-{value}"
        col1, col2 = st.columns(2)
        cols = [col1, col2, col1, col2]
        for i, b64 in enumerate(b64_list):
            sel_class = "selected" if img_sel == i else ""
            # radio input id: Streamlit 내부 패턴
            radio_id = f"radio_{qidx}-{i}"
            with cols[i]:
                # label 클릭 → 연결된 radio input 클릭 → Streamlit 값 변경 → rerun
                st.markdown(f"""
                <label for="{radio_id}" class="img-card-label {sel_class}">
                    <img src="{b64}" />
                </label>
                """, unsafe_allow_html=True)

        for i, clicked in enumerate(hbtns):
            if clicked:
                st.session_state.img_chosen = i
                st.rerun()
        # radio 클릭 감지: radio_val 변화 → img_chosen 업데이트
        if radio_val != img_sel and img_sel is not None:
            st.session_state.img_chosen = radio_val
            st.rerun()

        # JS: postMessage 수신 → 해당 숨겨진 버튼 클릭
        recv_js = """
        # 이미지 클릭 후 img_chosen=None 상태에서 label 클릭하면
        # radio_val이 0이 되는데, 이걸 최초 선택으로 인식해야 함
        # → JS로 radio 변경 이벤트 감지해서 img_chosen 초기화
        st.markdown(f"""
        <script>
        window.addEventListener('message', function(e) {
            if (e.data && e.data.type === 'img_select') {
                var idx = e.data.idx;
                var btns = window.parent.document.querySelectorAll('.hbtn-row button');
                if (btns[idx]) btns[idx].click();
            }
        });
        (function() {{
            // radio 변경 시 img_chosen 을 None에서 업데이트하기 위해
            // Streamlit이 자동으로 rerun하므로 별도 처리 불필요
            // label 클릭 → radio change → Streamlit rerun → img_chosen 갱신
            var radios = window.parent.document.querySelectorAll(
                'input[type="radio"][name]'
            );
        }})();
        </script>
        """
        st.markdown(recv_js, unsafe_allow_html=True)
        """, unsafe_allow_html=True)

        # 이미지 그리드 렌더링
        components.html(html_code, height=500, scrolling=False)
        # img_chosen이 None일 때 label 클릭 → radio_val=0 이 되는 경우 처리
        if img_sel is None and radio_val == 0:
            # 처음 로딩인지 클릭인지 구분 불가 → 확인 버튼 비활성으로 안전 처리
            pass
        elif img_sel is None and radio_val != 0:
            st.session_state.img_chosen = radio_val
            st.rerun()

        st.write("")
        if st.button("✅ 이걸로 할래요!",
                     key=f"confirm_img_{st.session_state.quiz_idx}",
                     key=f"confirm_img_{qidx}",
                     use_container_width=True, type="primary",
                     disabled=(img_sel is None)):
            process_answer(img_sel)
