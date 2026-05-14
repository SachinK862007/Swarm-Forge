import streamlit as st
import plotly.graph_objects as go

def render_engagement_chart(static_time=2.3, swarm_time=12.0):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=["Static Honeypot"], y=[static_time], name="Static", marker_color="red"))
    fig.add_trace(go.Bar(x=["SwarmForge"], y=[swarm_time], name="SwarmForge", marker_color="green"))
    fig.update_layout(title="Engagement Time (seconds)", yaxis_title="Seconds")
    st.plotly_chart(fig, use_container_width=True)

def render_neutralisation_gauge(value_ms):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value_ms,
        title={'text': "Neutralisation Speed (ms)"},
        gauge={'axis': {'range': [0, 500]}, 'bar': {'color': "green"},
               'steps': [{'range': [0, 300], 'color': "lightgreen"}, {'range': [300, 500], 'color': "orange"}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 300}}))
    st.plotly_chart(fig, use_container_width=True)