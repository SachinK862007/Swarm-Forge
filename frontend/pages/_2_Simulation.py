import time

import requests
import streamlit as st

from components.metrics import render_engagement_chart, render_neutralisation_gauge


def show():
    st.markdown("## Attack simulation")
    st.caption(
        "Stress‑test your local SwarmForge API. Each request is real; engagement time is simulated for the chart."
    )

    st.markdown("### 1 · Configure")
    c1, c2 = st.columns(2)
    with c1:
        aggressiveness = st.slider(
            "How intense each attacker is (1 = light, 10 = heavy)",
            1,
            10,
            5,
        )
    with c2:
        swarm_size = st.slider(
            "How many attackers in the swarm",
            1,
            20,
            5,
        )

    st.markdown("### 2 · Run")
    st.caption("Backend URL: `http://localhost:8000/defend` — start the FastAPI server first.")

    if st.button("Run swarm", type="primary", use_container_width=False):
        engagement_times = []
        neutralisation_times = []
        errors = []
        bar = st.progress(0, text="Starting…")

        for i in range(swarm_size):
            if i % 3 == 0:
                attack_type = "injection"
            elif i % 3 == 1:
                attack_type = "bruteforce"
            else:
                attack_type = "recon"

            payload = {
                "ip": f"10.0.0.{i + 1}",
                "type": attack_type,
                "attempts": aggressiveness,
            }
            bar.progress(
                i / max(swarm_size, 1),
                text=f"Request {i + 1}/{swarm_size} — {attack_type} from {payload['ip']}",
            )
            t0 = time.perf_counter()
            try:
                resp = requests.post(
                    "http://localhost:8000/defend",
                    json=payload,
                    timeout=30,
                )
                t1 = time.perf_counter()
                duration_ms = (t1 - t0) * 1000
                if resp.status_code >= 400:
                    errors.append(f"{payload['ip']}: HTTP {resp.status_code}")
                    continue
            except requests.RequestException as e:
                errors.append(f"{payload['ip']}: {e}")
                continue

            neutralisation_times.append(duration_ms)
            engagement_times.append(2.3 + (i % 5) * 0.5)

        bar.progress(1.0, text="Done")
        time.sleep(0.25)
        bar.empty()

        if errors:
            with st.expander("Some requests failed (showing up to 10)", expanded=True):
                st.code("\n".join(errors[:10]), language="text")

        if not engagement_times or not neutralisation_times:
            st.error(
                "No successful API responses. Start the backend from the `backend` folder, "
                "for example: `uvicorn main:app --reload --port 8000`, then try again."
            )
            return

        avg_engage = sum(engagement_times) / len(engagement_times)
        avg_neut = sum(neutralisation_times) / len(neutralisation_times)

        st.success(
            f"Completed **{len(neutralisation_times)}** successful calls. "
            f"Average API time **{avg_neut:.0f} ms**."
        )

        st.markdown("### 3 · Results")
        m1, m2 = st.columns(2)
        with m1:
            st.metric(
                "Avg engagement (simulated)",
                f"{avg_engage:.2f} s",
                help="Demo curve for the bar chart; not from the network.",
            )
        with m2:
            st.metric(
                "Avg API time (measured)",
                f"{avg_neut:.0f} ms",
                delta="lower is faster",
                delta_color="inverse",
            )

        ch1, ch2 = st.columns(2)
        with ch1:
            render_engagement_chart(static_time=2.3, swarm_time=avg_engage)
        with ch2:
            render_neutralisation_gauge(avg_neut)
    else:
        st.info("Set the sliders, then click **Run swarm** to generate metrics and charts.")
