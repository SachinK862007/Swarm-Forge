import html

import streamlit as st


def render_explanation(text: str):
    safe = html.escape(str(text)).replace("\n", "<br/>")
    st.markdown(
        f"""
<div class="sf-explain-box">
  <div class="sf-kicker">AI explanation</div>
  <div style="color:#E6EDF3;font-size:0.95rem;">{safe}</div>
</div>
""",
        unsafe_allow_html=True,
    )
