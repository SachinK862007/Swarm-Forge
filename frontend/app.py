import streamlit as st
from streamlit_option_menu import option_menu
import os

st.set_page_config(
    page_title="SwarmForge",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        body, .stApp { background-color: #0D1117; color: #E6EDF3; }
        .css-1d391kg { background-color: #161B22; }
        </style>
        """, unsafe_allow_html=True)

load_css()

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=80)
    st.title("SwarmForge")
    st.markdown("AI‑Powered Adaptive Honeypot Swarm")
    st.markdown("---")
    page = option_menu(
        menu_title=None,
        options=["Live Monitor", "Simulation", "Community", "TEE Attestation"],
        icons=["broadcast", "play-circle", "people", "lock"],
        default_index=0,
    )
    st.markdown("---")
    st.caption("© 2026 SwarmForge | Open‑Source Defense")

if page == "Live Monitor":
    from pages import _1_Live_Monitor
    _1_Live_Monitor.show()
elif page == "Simulation":
    from pages import _2_Simulation
    _2_Simulation.show()
elif page == "Community":
    from pages import _3_Community
    _3_Community.show()
elif page == "TEE Attestation":
    from pages import _4_TEE_Attestation
    _4_TEE_Attestation.show()