import streamlit as st
import pandas as pd
import time
from supabase import create_client
from components.attack_map import render_map
from components.explain_card import render_explanation

# ==================== REPLACE WITH YOUR REAL SUPABASE CREDENTIALS ====================
SUPABASE_URL = "https://beorvnttfbczhjfkorcp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # your anon key
# =====================================================================================

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_logs():
    try:
        data = supabase.table("attack_logs").select("*").order("timestamp", desc=True).limit(50).execute()
        if data.data:
            return pd.DataFrame(data.data)
    except Exception as e:
        st.error(f"Supabase error: {e}")
    return pd.DataFrame()

def show():
    st.title("🛡️ Live Attack Monitor")
    st.markdown("Real‑time visualisation of attacks and SwarmForge responses.")

    # Manual refresh button
    if st.button("🔄 Refresh Now"):
        st.session_state.refresh = True

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

    # Auto‑refresh every 3 seconds
    time.sleep(3)
    st.rerun()