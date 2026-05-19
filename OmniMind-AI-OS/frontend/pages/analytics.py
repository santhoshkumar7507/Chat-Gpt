import streamlit as st
import plotly.graph_objects as go
import os
import sys

# Ensure backend can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from backend.memory import get_history

st.set_page_config(page_title="Neural Telemetry", page_icon="📈", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&family=Syncopate:wght@400;700&display=swap');

    /* Global styling with Cyber Grid */
    .stApp {
        background-color: #030305;
        background-image: 
            linear-gradient(rgba(0, 229, 255, 0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 229, 255, 0.04) 1px, transparent 1px),
            radial-gradient(circle at 50% 0%, rgba(181, 55, 242, 0.15) 0%, transparent 60%),
            radial-gradient(circle at 50% 100%, rgba(0, 229, 255, 0.15) 0%, transparent 70%);
        background-size: 40px 40px, 40px 40px, 100% 100%, 100% 100%;
        color: #e2e8f0;
        font-family: 'Space Grotesk', sans-serif;
    }

    .stAppHeader { background-color: transparent !important; }

    /* Animated Scanline Overlay */
    .stApp::after {
        content: ""; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(to bottom, transparent 50%, rgba(0, 229, 255, 0.02) 51%);
        background-size: 100% 4px; pointer-events: none; z-index: 9999;
    }
    
    /* Main Title Holographic Shimmer */
    .main-title {
        font-family: 'Syncopate', sans-serif;
        background: linear-gradient(90deg, #00e5ff, #ffffff, #b537f2, #00e5ff);
        background-size: 300% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem !important;
        text-align: center; margin-bottom: 0rem;
        animation: gradientShimmer 4s linear infinite;
        text-shadow: 0 0 30px rgba(0, 229, 255, 0.4);
        letter-spacing: 2px;
    }

    .sub-title {
        text-align: center; color: #8b9bb4; font-family: 'Space Grotesk', sans-serif;
        font-weight: 400; font-size: 0.9rem; margin-bottom: 20px;
        letter-spacing: 4px; text-transform: uppercase;
    }

    @keyframes gradientShimmer {
        0% { background-position: 0% 50%; }
        100% { background-position: 300% 50%; }
    }

    /* Quantum Glass Cards */
    .glass-card {
        background: rgba(10, 10, 20, 0.6);
        backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(0, 229, 255, 0.15);
        border-radius: 8px; padding: 20px; margin: 10px 0;
        box-shadow: inset 0 0 30px rgba(0, 229, 255, 0.02), 0 15px 40px rgba(0,0,0,0.9);
        position: relative; overflow: hidden;
        transition: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
    }
    
    .glass-card::before {
        content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(181, 55, 242, 0.1), transparent);
        transition: all 0.6s ease; transform: skewX(-20deg);
    }

    .glass-card:hover {
        transform: translateY(-5px) scale(1.02);
        border-color: rgba(181, 55, 242, 0.6) !important;
        box-shadow: 0 20px 50px rgba(181, 55, 242, 0.2), inset 0 0 20px rgba(181, 55, 242, 0.1) !important;
    }
    
    .glass-card:hover::before { left: 200%; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; margin-bottom: 20px;'>
    <h1 class='main-title'>NEURAL TELEMETRY</h1>
    <p class='sub-title'>System Diagnostics & Core Performance</p>
</div>
""", unsafe_allow_html=True)

# Display the AI Generated Image as a HUD Core
try:
    # Need to specify absolute or relative path from frontend/pages
    image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../assets/quantum_core.png'))
    st.image(image_path, use_container_width=True)
except Exception as e:
    st.write("Core Image offline.", e)

history = get_history()
questions = [item[1] for item in history]
sizes = [len(q) for q in questions]

# HUD Metrics Grid
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class='glass-card' style='text-align: center;'>
        <div style='color: #00e5ff; font-family: "Syncopate", sans-serif; font-size: 0.8rem; letter-spacing: 2px;'>TOTAL QUERIES</div>
        <div style='color: #fff; font-size: 2.5rem; font-weight: 700; text-shadow: 0 0 15px rgba(0,229,255,0.5);'>{len(history)}</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    max_load = max(sizes) if sizes else 0
    st.markdown(f"""
    <div class='glass-card' style='text-align: center; border-color: rgba(181, 55, 242, 0.5);'>
        <div style='color: #b537f2; font-family: "Syncopate", sans-serif; font-size: 0.8rem; letter-spacing: 2px;'>PEAK LOAD</div>
        <div style='color: #fff; font-size: 2.5rem; font-weight: 700; text-shadow: 0 0 15px rgba(181,55,242,0.5);'>{max_load}<span style='font-size:1rem; color:#94a3b8;'> chars</span></div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    status = "OPTIMAL" if len(history) > 0 else "STANDBY"
    color = "#00e5ff" if status == "OPTIMAL" else "#b537f2"
    st.markdown(f"""
    <div class='glass-card' style='text-align: center; border-color: rgba(0, 229, 255, 0.5);'>
        <div style='color: {color}; font-family: "Syncopate", sans-serif; font-size: 0.8rem; letter-spacing: 2px;'>CORE STATUS</div>
        <div style='color: #fff; font-size: 2rem; font-weight: 700; text-shadow: 0 0 15px {color}; margin-top: 5px;'>{status}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if sizes:
    # Create an ultra-premium Plotly graph
    fig = go.Figure()
    
    # Add glowing area fill
    fig.add_trace(go.Scatter(
        x=list(range(1, len(sizes)+1)),
        y=sizes,
        mode='lines+markers',
        name='Load',
        line=dict(color='#00e5ff', width=3, shape='spline'),
        marker=dict(
            size=12, 
            color='#b537f2', 
            line=dict(width=2, color='#ffffff'),
            symbol='hexagon-open-dot'
        ),
        fill='tozeroy',
        fillcolor='rgba(0, 229, 255, 0.1)',
        hoverinfo='x+y',
        hovertemplate='<b style="font-size:16px;">Query Sequence %{x}</b><br><br>Network Load: <b>%{y} Tokens</b><extra></extra>'
    ))
    
    # Style the layout for HUD
    fig.update_layout(
        title=dict(
            text='REAL-TIME QUERY COMPLEXITY',
            font=dict(family='Syncopate', size=18, color='#ffffff'),
            x=0.5,
            y=0.85
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            title=dict(text='SEQUENCE ID', font=dict(family='Space Grotesk', color='#94a3b8', size=12)),
            tickfont=dict(family='Space Grotesk', color='#00e5ff'),
            showgrid=True,
            gridcolor='rgba(0, 229, 255, 0.1)',
            gridwidth=1,
            zeroline=False
        ),
        yaxis=dict(
            title=dict(text='TOKEN / CHARACTER LOAD', font=dict(family='Space Grotesk', color='#94a3b8', size=12)),
            tickfont=dict(family='Space Grotesk', color='#b537f2'),
            showgrid=True,
            gridcolor='rgba(181, 55, 242, 0.1)',
            gridwidth=1,
            zeroline=False
        ),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor="rgba(10, 10, 20, 0.9)",
            font_size=14,
            font_family="Space Grotesk",
            bordercolor="#00e5ff"
        ),
        margin=dict(l=20, r=20, t=70, b=20),
        height=450
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
else:
    st.info("Insufficient data to generate telemetry. Please interact with the Core Engine.")
