"""
삼괴고 3학년 선택과목 가이드 — 리다이렉트 페이지

2025-05 이후 정적 사이트(Hugging Face Space)로 이전됨.
이 Streamlit 앱은 책자에 인쇄된 기존 주소를 새 주소로 자동 이동시키는 역할만 합니다.
"""
import streamlit as st

HF_URL = "https://hyojin22c-course3-ai.hf.space"

st.set_page_config(page_title="삼괴고 3학년 선택과목 가이드", page_icon="📚")

# 1) 메타 리프레시 + JS 리다이렉트 (브라우저가 즉시 새 주소로 이동)
st.markdown(
    f"""
<meta http-equiv="refresh" content="0; url={HF_URL}">
<script>window.location.replace("{HF_URL}");</script>
""",
    unsafe_allow_html=True,
)

# 2) 자동 이동 실패 대비 안내 (수동 클릭 가능)
st.markdown(
    f"""
<div style="text-align:center; padding: 3rem 1rem; font-family: 'Noto Sans KR', sans-serif;">
  <div style="font-size: 2.5rem; margin-bottom: 1rem;">📚</div>
  <h2 style="color: #1a365d;">페이지가 이동되었습니다</h2>
  <p style="color: #475569; font-size: 1rem; line-height: 1.6;">
    삼괴고 3학년 선택과목 가이드는 새 주소로 이전되었습니다.<br>
    자동으로 이동되지 않으면 아래 버튼을 눌러주세요.
  </p>
  <a href="{HF_URL}" style="
    display: inline-block;
    margin-top: 1.5rem;
    padding: 0.8rem 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-decoration: none;
    border-radius: 8px;
    font-weight: 700;
    font-size: 1rem;">
    👉 새 사이트로 이동
  </a>
  <p style="color: #94a3b8; font-size: 0.85rem; margin-top: 2rem;">
    새 주소: <a href="{HF_URL}" style="color: #2563eb;">{HF_URL}</a>
  </p>
</div>
""",
    unsafe_allow_html=True,
)
