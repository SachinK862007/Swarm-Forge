import streamlit as st
import pandas as pd
import time
from supabase import create_client
from components.attack_map import render_map
from components.explain_card import render_explanation

# ==================== REPLACE THESE ====================
SUPABASE_URL = "https://beorvnttfbczhjfkorcp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # your anon key
# =======================================================

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_logs():
    data = supabase.table("attack_logs").select("*").order("timestamp", desc=True).limit(50).execute()
    return pd.DataFrame(data.data) if data.data else pd.DataFrame()

def show():
    st.title("🛡️ Live Attack Monitor")
    st.markdown("Real‑time visualisation of attacks and SwarmForge responses.")

    logs_df = fetch_logs()

    if not logs_df.empty:
        render_map(logs_df)

        st.subheader("Attack Timeline")
        for _, row in logs_df.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(
                    f"**{row['timestamp']}** — {row['attacker_ip']} → "
                    f"{row['attack_type']} ({row['mitre_id']})"
                )
            with col2:
                if st.button("Why?", key=f"why_{row['id']}"):
                    render_explanation(row['explanation'])
            st.markdown("---")
    else:
        st.info("No attacks recorded yet. Launch a simulation or trigger honeytokens.")

    # Auto‑refresh every 2 seconds
    time.sleep(2)
    st.rerun()