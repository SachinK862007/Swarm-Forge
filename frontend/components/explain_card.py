import streamlit as st

def render_explanation(text: str):
    st.markdown(f"""
    <div style="background-color:#161B22; padding:15px; border-radius:8px; border-left:5px solid #00B4D8;">
        <small style="color:#00B4D8;">💡 EXPLAINABILITY (AI‑Generated)</small><br>
        {text}
    </div>
    """, unsafe_allow_html=True)