import plotly.graph_objects as go
import streamlit as st


def render_engagement_chart(static_time=2.3, swarm_time=12.0):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=["Static honeypot", "SwarmForge swarm"],
            y=[static_time, swarm_time],
            marker_color=["#f85149", "#3fb950"],
            text=[f"{static_time:.1f}s", f"{swarm_time:.1f}s"],
            textposition="outside",
            textfont=dict(color="#E6EDF3", size=13),
        )
    )
    fig.update_layout(
        title="Time attackers stay engaged (higher often means better intel capture)",
        yaxis_title="Seconds",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(22,27,34,0.6)",
        font_color="#E6EDF3",
        title_font_color="#3fb950",
        title_font_size=14,
        showlegend=False,
        height=360,
        yaxis=dict(gridcolor="rgba(48,54,61,0.8)", zeroline=False),
        margin=dict(t=72, b=48),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_neutralisation_gauge(value_ms):
    display_val = float(value_ms)
    axis_max = max(500.0, display_val * 1.05)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=display_val,
            number={"suffix": " ms", "font": {"size": 28}},
            title={
                "text": "API response time (lower = faster neutralisation)",
                "font": {"size": 14, "color": "#8b949e"},
            },
            gauge={
                "axis": {"range": [0, axis_max], "tickcolor": "#8b949e"},
                "bar": {"color": "#3fb950"},
                "bgcolor": "#21262d",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, min(300, axis_max)], "color": "rgba(63,185,80,0.2)"},
                    {"range": [min(300, axis_max), axis_max], "color": "rgba(210,153,34,0.2)"},
                ],
                "threshold": {
                    "line": {"color": "#f85149", "width": 3},
                    "thickness": 0.8,
                    "value": 300,
                },
            },
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#E6EDF3",
        height=300,
        margin=dict(t=80, b=24, l=24, r=24),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
