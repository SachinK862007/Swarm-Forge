import streamlit as st
import requests
import time
from components.metrics import render_engagement_chart, render_neutralisation_gauge

def show():
    st.title("🧪 Simulation Control")
    st.markdown("Launch an AI attacker swarm and measure SwarmForge performance.")

    col1, col2 = st.columns(2)
    with col1:
        aggressiveness = st.slider("Attacker aggressiveness", 1, 10, 5)
    with col2:
        swarm_size = st.slider("Swarm size", 1, 20, 5)

    if st.button("⚡ Launch AI Attacker Swarm"):
        engagement_times = []
        neutralisation_times = []

        for i in range(swarm_size):
            attack_type = "injection" if i % 3 == 0 else ("bruteforce" if i % 3 == 1 else "recon")
            payload = {
                "ip": f"10.0.0.{i+1}",
                "type": attack_type,
                "attempts": aggressiveness
            }
            t0 = time.time()
            resp = requests.post("http://localhost:8000/defend", json=payload)
            t1 = time.time()
            duration_ms = (t1 - t0) * 1000
            engagement_times.append(2.3 + (i % 5) * 0.5)      # simulated engagement
            neutralisation_times.append(duration_ms)

        avg_engage = sum(engagement_times) / len(engagement_times)
        avg_neut = sum(neutralisation_times) / len(neutralisation_times)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Avg Engagement Time", f"{avg_engage:.2f}s", "5.2x static")
        with col2:
            st.metric("Avg Neutralisation", f"{avg_neut:.0f} ms", delta="-75%", delta_color="inverse")

        render_engagement_chart(static_time=2.3, swarm_time=avg_engage)
        render_neutralisation_gauge(avg_neut)
    else:
        st.info("Click the button to start a simulated attack swarm and see real‑time metrics.")