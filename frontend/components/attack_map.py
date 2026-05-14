import streamlit as st
import plotly.express as px
import pandas as pd

def render_map(df: pd.DataFrame):
    # Map attacker IP to approximate coordinates (demo)
    df["lat"] = 20.0 + (pd.util.hash_array(df["attacker_ip"].to_numpy()) % 100) / 10
    df["lon"] = 77.0 + (pd.util.hash_array(df["attacker_ip"].to_numpy()) % 100) / 10
    fig = px.scatter_geo(df, lat="lat", lon="lon", color="attack_type",
                         title="Live Attack Origins", projection="natural earth")
    fig.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)