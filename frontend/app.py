import importlib
import os

import streamlit as st

st.set_page_config(
    page_title="SwarmForge",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _assert_pandas_usable():
    """Catch a broken install or a local file named pandas.py shadowing the real library."""
    try:
        import pandas as pd
    except ImportError:
        st.error(
            "The **pandas** package is not installed. From the `frontend` folder run:  "
            "`pip install -r requirements.txt`"
        )
        st.stop()
    if not hasattr(pd, "DataFrame"):
        loc = getattr(pd, "__file__", "unknown")
        st.error(
            "Your environment is loading a broken or wrong module named **pandas** "
            f"(no `DataFrame`, loaded from `{loc}`).\n\n"
            "- Delete or rename any **`pandas.py`** in the folder you run Streamlit from.\n"
            "- Then reinstall: `pip uninstall pandas -y` and `pip install pandas`."
        )
        st.stop()


def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <style>
            body, .stApp { background-color: #0D1117; color: #E6EDF3; }
            [data-testid="stSidebar"] { background-color: #161B22; }
            h1, h2, h3 { color: #3fb950; }
            </style>
            """,
            unsafe_allow_html=True,
        )


_assert_pandas_usable()
load_css()

PAGE_MODULES = {
    "Live Monitor": "pages._1_Live_Monitor",
    "Simulation": "pages._2_Simulation",
    "Community": "pages._3_Community",
    "TEE Attestation": "pages._4_TEE_Attestation",
}

PAGE_HELP = {
    "Live Monitor": "Map + table + one AI explanation at a time.",
    "Simulation": "Call your local API and see timing charts.",
    "Community": "Submit / browse JSON templates in Supabase.",
    "TEE Attestation": "Storyboard for trusted execution demo.",
}

NAV_LABEL = {
    "Live Monitor": "📡  Live Monitor",
    "Simulation": "▶️  Simulation",
    "Community": "👥  Community",
    "TEE Attestation": "🔒  TEE Attestation",
}

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=72)
    st.markdown("### SwarmForge")
    st.caption("Adaptive honeypot swarm — hackathon dashboard.")
    st.divider()
    st.markdown("**Go to**")
    page = st.radio(
        "Navigation",
        list(PAGE_MODULES.keys()),
        format_func=lambda k: NAV_LABEL.get(k, k),
        label_visibility="collapsed",
    )
    st.caption(PAGE_HELP.get(page, ""))
    st.divider()
    st.caption("© 2026 SwarmForge · open‑source defense")

mod = importlib.import_module(PAGE_MODULES[page])
mod.show()
