import hashlib

import pandas as pd
import plotly.express as px
import streamlit as st


def _ip_lat_lon(ip: str) -> tuple[float, float]:
    """Map IP to approximate lat/lon using a stable hash, jittered around India (demo)."""
    h = hashlib.sha256(str(ip).encode("utf-8")).hexdigest()
    hi = int(h[:12], 16)
    lo = int(h[12:24], 16)
    lat = 20.5 + (hi % 1000) / 200.0
    lon = 77.5 + (lo % 1000) / 200.0
    return lat, lon


def render_map(df: pd.DataFrame):
    if df.empty or "attacker_ip" not in df.columns or "attack_type" not in df.columns:
        st.info("Map needs columns **attacker_ip** and **attack_type** in your Supabase table.")
        return

    work = df.copy()
    coords = work["attacker_ip"].map(_ip_lat_lon)
    work["lat"] = [c[0] for c in coords]
    work["lon"] = [c[1] for c in coords]

    fig = px.scatter_geo(
        work,
        lat="lat",
        lon="lon",
        color="attack_type",
        title="Where attacks appear to originate (demo positions from IP hash)",
        projection="natural earth",
        height=420,
    )
    fig.update_traces(marker=dict(size=11, opacity=0.85))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title_font_color="#E6EDF3",
        title_font_size=15,
        font_color="#E6EDF3",
        legend_title_text="Attack type",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=56, b=0),
    )
    fig.update_geos(
        bgcolor="rgba(0,0,0,0)",
        showland=True,
        landcolor="#1a2332",
        showocean=True,
        oceancolor="#0D1117",
        showlakes=False,
        showrivers=False,
        showframe=False,
        projection_type="natural earth",
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
