from datetime import timedelta

import pandas as pd
import streamlit as st
from supabase import create_client

from components.attack_map import render_map
from components.explain_card import render_explanation

# --- REPLACE WITH YOUR REAL CREDENTIALS (Supabase project URL + anon key) ---
SUPABASE_URL = "REPLACE_WITH_YOUR_SUPABASE_URL"
SUPABASE_KEY = "REPLACE_WITH_YOUR_SUPABASE_ANON_KEY"
# -----------------------------------------------------------------------------


def _client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_logs():
    try:
        supabase = _client()
        data = (
            supabase.table("attack_logs")
            .select("*")
            .order("timestamp", desc=True)
            .limit(50)
            .execute()
        )
        if data.data:
            return pd.DataFrame(data.data)
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=8, show_spinner=False)
def load_logs():
    return fetch_logs()


def _render_live_body(logs_df: pd.DataFrame):
    if logs_df.empty:
        st.info(
            "**No attacks in the database yet.**\n\n"
            "1. Add your Supabase URL and anon key at the top of this file.\n"
            "2. Run the **Simulation** page while the API is up, or insert rows into `attack_logs`.\n"
            "3. Press **Refresh data** here."
        )
        return

    want = ["timestamp", "attacker_ip", "attack_type", "mitre_id"]
    have = [c for c in want if c in logs_df.columns]
    n = len(logs_df)
    uniq_ip = (
        logs_df["attacker_ip"].nunique() if "attacker_ip" in logs_df.columns else "—"
    )
    types = (
        logs_df["attack_type"].nunique() if "attack_type" in logs_df.columns else "—"
    )

    m1, m2, m3 = st.columns(3)
    m1.metric("Events shown", str(n))
    m2.metric("Unique IPs", str(uniq_ip))
    m3.metric("Attack types", str(types))

    st.markdown("#### Map")
    render_map(logs_df)

    st.markdown("#### Event log")
    st.caption("Scroll the table, then use the dropdown below to read the AI explanation for one event.")
    display = logs_df[have].copy() if have else logs_df.copy()
    st.dataframe(
        display.head(50),
        use_container_width=True,
        hide_index=True,
        height=min(360, 48 + 36 * min(len(display), 10)),
    )

    pick = logs_df.head(30).reset_index(drop=True)
    labels = []
    for _, row in pick.iterrows():
        ts = str(row.get("timestamp", "—"))[:22]
        ip = row.get("attacker_ip", "—")
        atk = row.get("attack_type", "—")
        labels.append(f"{atk}  ·  {ip}  ·  {ts}")

    st.markdown("#### Pick one event")
    idx = st.selectbox(
        "Event",
        range(len(pick)),
        format_func=lambda i: labels[i],
        label_visibility="collapsed",
    )
    expl = pick.iloc[idx].get("explanation", "No explanation stored for this row.")
    render_explanation(str(expl))


_frag = getattr(st, "fragment", None) or getattr(st, "experimental_fragment", None)

if _frag:

    @_frag(run_every=timedelta(seconds=12))
    def _live_fragment_panel():
        _render_live_body(load_logs())

else:
    _live_fragment_panel = None


def show():
    st.markdown("## Live attack monitor")
    st.caption(
        "See recent honeypot hits on a map, scan the log, and read one plain‑English explanation at a time."
    )

    row1 = st.columns([1.2, 1.2, 2.2])
    with row1[0]:
        if st.button("Refresh data", type="primary", use_container_width=True):
            load_logs.clear()
            st.rerun()
    with row1[1]:
        live = st.toggle(
            "Live updates (12s)",
            value=False,
            help="Only refreshes the monitor panel, not the whole browser.",
        )
    with row1[2]:
        st.caption("Turn **Live updates** off when you switch to other pages for the snappiest UI.")

    st.divider()

    if live and _live_fragment_panel is not None:
        _live_fragment_panel()
    else:
        if live and _live_fragment_panel is None:
            st.warning(
                "Live auto‑updates are not available in this Streamlit version. "
                "Upgrade to **Streamlit 1.28+** or use **Refresh data**."
            )
        _render_live_body(load_logs())
