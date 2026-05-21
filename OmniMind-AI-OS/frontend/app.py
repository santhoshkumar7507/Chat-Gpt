import streamlit as st
import requests
from backend.memory import get_history
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import time
import os

# Set page config with custom title, favicon and ultra-wide layout
st.set_page_config(page_title="OmniMind Quantum AI OS", page_icon="🌌", layout="wide")

# Inject premium CSS styles with custom glowing HUD components, animations, and typography
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Space+Grotesk:wght@300;400;500;600;700&family=Syncopate:wght@400;700&family=JetBrains+Mono:wght@400;700&display=swap');

    /* Global styling with Cyber Grid */
    .stApp {
        background-color: #050409;
        background-image: 
            linear-gradient(rgba(0, 229, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 229, 255, 0.03) 1px, transparent 1px),
            radial-gradient(circle at 50% 0%, rgba(181, 55, 242, 0.12) 0%, transparent 60%),
            radial-gradient(circle at 10% 100%, rgba(0, 229, 255, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 90% 100%, rgba(244, 63, 94, 0.08) 0%, transparent 50%);
        background-size: 50px 50px, 50px 50px, 100% 100%, 100% 100%, 100% 100%;
        color: #e2e8f0;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Hide standard Streamlit header, footer, and default page navigation to make it look like a standalone SaaS app */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stSidebarNav"] {
        display: none !important;
    }

    .stAppHeader { background-color: transparent !important; }

    /* Animated Scanline Overlay */
    .stApp::after {
        content: ""; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(to bottom, transparent 50%, rgba(0, 229, 255, 0.015) 51%);
        background-size: 100% 4px; pointer-events: none; z-index: 9999;
    }

    /* Sidebar HUD styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #030206 0%, #0c081d 100%) !important;
        border-right: 1px solid rgba(0, 229, 255, 0.2) !important;
        box-shadow: 10px 0 35px rgba(0, 0, 0, 0.95);
    }
    
    /* Headings */
    h1, h2, h3, h4 {
        font-family: 'Syncopate', sans-serif; text-transform: uppercase; letter-spacing: 2px;
    }

    /* Main Title Holographic Shimmer */
    .main-title {
        background: linear-gradient(90deg, #00e5ff, #ffffff, #b537f2, #00e5ff);
        background-size: 300% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.2rem !important;
        font-weight: 900;
        text-align: center; margin-bottom: 0rem;
        animation: gradientShimmer 4s linear infinite;
        text-shadow: 0 0 30px rgba(0, 229, 255, 0.4);
    }

    .sub-title {
        text-align: center; color: #8b9bb4; font-family: 'Space Grotesk', sans-serif;
        font-weight: 500; font-size: 0.9rem; margin-bottom: 2.5rem;
        letter-spacing: 12px; text-transform: uppercase;
        text-shadow: 0 0 8px rgba(139, 155, 180, 0.2);
    }

    @keyframes gradientShimmer {
        0% { background-position: 0% 50%; }
        100% { background-position: 300% 50%; }
    }

    /* Quantum Glass Cards */
    .glass-card {
        background: rgba(10, 10, 24, 0.55);
        backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 229, 255, 0.12);
        border-radius: 14px; padding: 25px; margin: 15px 0;
        box-shadow: inset 0 0 30px rgba(0, 229, 255, 0.01), 0 15px 35px rgba(0,0,0,0.8);
        position: relative; overflow: hidden;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .glass-card::before {
        content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(181, 55, 242, 0.08), transparent);
        transition: all 0.7s ease; transform: skewX(-20deg);
    }

    .glass-card:hover {
        transform: translateY(-4px);
        border-color: rgba(181, 55, 242, 0.4);
        box-shadow: 0 15px 35px rgba(181, 55, 242, 0.1), inset 0 0 20px rgba(181, 55, 242, 0.02);
    }
    
    .glass-card:hover::before { left: 200%; }

    .glass-card h3 { color: #ffffff; font-size: 1.25rem; display: flex; align-items: center; gap: 12px; text-shadow: 0 0 10px rgba(255,255,255,0.15); margin-top: 0; }
    .glass-card p { color: #94a3b8; font-size: 0.95rem; margin-top: 8px; font-family: 'Space Grotesk', sans-serif; text-transform: none; letter-spacing: 0.3px; line-height: 1.6; }

    /* Neo border utilities */
    .border-cyan { border-left: 4px solid #00e5ff !important; }
    .border-purple { border-left: 4px solid #b537f2 !important; }
    .border-green { border-left: 4px solid #10b981 !important; }
    .border-rose { border-left: 4px solid #f43f5e !important; }

    /* Cyber Buttons */
    .stButton>button {
        background: rgba(0, 229, 255, 0.03) !important;
        color: #00e5ff !important;
        border: 1px solid rgba(0, 229, 255, 0.4) !important; border-radius: 8px !important;
        padding: 0.7rem 1.8rem !important; font-family: 'Syncopate', sans-serif !important;
        font-weight: 700 !important; font-size: 0.8rem !important;
        letter-spacing: 1.5px !important; transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
        text-transform: uppercase;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.05) !important;
    }
    
    .stButton>button:hover {
        background: rgba(181, 55, 242, 0.12) !important;
        color: #fff !important; border-color: rgba(181, 55, 242, 0.8) !important;
        box-shadow: 0 0 25px rgba(181, 55, 242, 0.25), inset 0 0 10px rgba(181, 55, 242, 0.1) !important;
        transform: translateY(-2px) !important; text-shadow: 0 0 8px rgba(255,255,255,0.3) !important;
    }
    
    .stButton>button:active { transform: translateY(1px) !important; }

    /* Purge button customization */
    .purge-btn>div>button {
        background: rgba(244, 63, 94, 0.03) !important;
        color: #f43f5e !important;
        border: 1px solid rgba(244, 63, 94, 0.3) !important;
    }
    .purge-btn>div>button:hover {
        background: rgba(244, 63, 94, 0.12) !important;
        border-color: rgba(244, 63, 94, 0.8) !important;
        box-shadow: 0 0 25px rgba(244, 63, 94, 0.25) !important;
    }

    /* Streamlit radio menu container styling */
    div[data-testid="stRadio"] > div {
        gap: 10px !important;
    }
    
    div[data-testid="stRadio"] > div > label {
        background: linear-gradient(90deg, rgba(8, 7, 16, 0.8), rgba(16, 12, 28, 0.85)) !important;
        border: 1px solid rgba(0, 229, 255, 0.06) !important;
        border-left: 4px solid rgba(0, 229, 255, 0.15) !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        cursor: pointer !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
        position: relative;
        overflow: hidden;
        width: 100%;
        display: flex;
        align-items: center;
    }

    div[data-testid="stRadio"] > div > label::before {
        content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(181, 55, 242, 0.1), transparent);
        transition: all 0.6s ease; z-index: 1;
    }

    div[data-testid="stRadio"] > div > label:hover {
        transform: translateX(8px) !important;
        background: linear-gradient(90deg, rgba(16, 8, 32, 0.9), rgba(28, 14, 48, 0.95)) !important;
        border-color: rgba(181, 55, 242, 0.4) !important;
        border-left: 4px solid #b537f2 !important;
        box-shadow: 0 8px 20px rgba(181, 55, 242, 0.15) !important;
    }
    
    div[data-testid="stRadio"] > div > label:hover::before { left: 100%; }

    /* Hide standard radio circle icon */
    div[data-testid="stRadio"] > div > label > div:first-child { display: none !important; }

    /* Navigation text styling */
    div[data-testid="stRadio"] > div > label > div:nth-child(2) {
        font-family: 'Syncopate', sans-serif !important;
        font-weight: 700 !important; font-size: 0.8rem !important;
        color: #94a3b8 !important; text-transform: uppercase;
        letter-spacing: 1.5px !important; margin-left: 4px !important;
        z-index: 2; transition: all 0.3s ease !important;
    }

    div[data-testid="stRadio"] > div > label:hover > div:nth-child(2) {
        color: #ffffff !important; text-shadow: 0 0 10px rgba(255, 255, 255, 0.4) !important;
    }

    /* Active State Radio Nav Button */
    div[data-testid="stRadio"] > div > label:has(input:checked) {
        background: linear-gradient(90deg, rgba(0, 229, 255, 0.1), rgba(0, 229, 255, 0.02)) !important;
        border-color: rgba(0, 229, 255, 0.4) !important;
        border-left: 5px solid #00e5ff !important;
        transform: translateX(10px) !important;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.15) !important;
    }
    
    div[data-testid="stRadio"] > div > label:has(input:checked) > div:nth-child(2) {
        color: #00e5ff !important;
        text-shadow: 0 0 15px rgba(0, 229, 255, 0.6) !important;
        letter-spacing: 2px !important;
    }

    /* Custom progress bar styles */
    .hud-bar-bg {
        background: rgba(255,255,255,0.05);
        border-radius: 4px;
        height: 6px;
        width: 100%;
        margin-top: 6px;
        overflow: hidden;
    }
    .hud-bar-fill {
        height: 100%;
        border-radius: 4px;
        background: linear-gradient(90deg, #00e5ff, #b537f2);
        box-shadow: 0 0 8px #00e5ff;
    }

    /* Pulse Connection Indicator */
    .pulse-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
        margin-right: 8px;
        box-shadow: 0 0 10px #10b981;
        animation: pulseAnimation 2s infinite alternate;
    }
    
    @keyframes pulseAnimation {
        0% { transform: scale(0.9); opacity: 0.6; box-shadow: 0 0 4px #10b981; }
        100% { transform: scale(1.3); opacity: 1; box-shadow: 0 0 12px #10b981; }
    }

    /* Premium stChatMessage styling to match the neon design system */
    [data-testid="stChatMessage"] {
        background: rgba(12, 11, 28, 0.45) !important;
        border: 1px solid rgba(0, 229, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 18px !important;
        margin-bottom: 15px !important;
        color: #e2e8f0 !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35) !important;
        transition: all 0.3s ease;
    }
    [data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatar"] > div[role="img"]) {
        border-left: 4px solid #00e5ff !important;
    }
    [data-testid="stChatMessage"]:nth-child(even) {
        background: rgba(22, 12, 42, 0.45) !important;
        border: 1px solid rgba(181, 55, 242, 0.12) !important;
        border-left: 4px solid #b537f2 !important;
    }
    [data-testid="stChatMessage"] p {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.02rem !important;
        line-height: 1.6 !important;
    }

    /* Quick-start prompts container layout */
    .quickstart-container {
        margin: 25px 0;
    }
    .quickstart-container div.stButton > button {
        background: linear-gradient(135deg, rgba(14, 11, 30, 0.75), rgba(24, 15, 45, 0.8)) !important;
        border: 1px solid rgba(0, 229, 255, 0.15) !important;
        border-left: 4px solid #00e5ff !important;
        border-radius: 10px !important;
        padding: 16px 20px !important;
        text-align: left !important;
        font-family: 'Space Grotesk', sans-serif !important;
        color: #ffffff !important;
        font-size: 0.92rem !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        white-space: normal !important;
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
        align-items: flex-start !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.4) !important;
    }
    .quickstart-container div.stButton > button:hover {
        background: linear-gradient(135deg, rgba(22, 11, 45, 0.85), rgba(40, 15, 70, 0.9)) !important;
        border-color: rgba(181, 55, 242, 0.5) !important;
        border-left: 4px solid #b537f2 !important;
        box-shadow: 0 10px 25px rgba(181, 55, 242, 0.25) !important;
        transform: translateY(-3px) !important;
    }
    .quickstart-container div.stButton > button strong {
        color: #00e5ff !important;
        font-family: 'Syncopate', sans-serif !important;
        font-size: 0.75rem !important;
        letter-spacing: 1px !important;
        margin-bottom: 6px !important;
        text-transform: uppercase !important;
        display: block !important;
    }
    .quickstart-container div.stButton > button:hover strong {
        color: #b537f2 !important;
        text-shadow: 0 0 8px rgba(181,55,242,0.4) !important;
    }

    /* Soundwave bars container */
    .voice-wave-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 60px;
        gap: 6px;
        margin: 20px 0;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 12px;
        border: 1px solid rgba(244, 63, 94, 0.15);
        padding: 10px 30px;
    }
    .voice-wave-container .stroke {
        display: block;
        position: relative;
        background: #00e5ff;
        height: 100%;
        width: 5px;
        border-radius: 50px;
        animation: animateWave 1.2s infinite ease-in-out;
    }
    .voice-wave-container .stroke:nth-child(1) { animation-delay: 0.1s; background: #00e5ff; }
    .voice-wave-container .stroke:nth-child(2) { animation-delay: 0.3s; background: #5d3df2; }
    .voice-wave-container .stroke:nth-child(3) { animation-delay: 0.5s; background: #b537f2; }
    .voice-wave-container .stroke:nth-child(4) { animation-delay: 0.7s; background: #f43f5e; }
    .voice-wave-container .stroke:nth-child(5) { animation-delay: 0.5s; background: #b537f2; }
    .voice-wave-container .stroke:nth-child(6) { animation-delay: 0.3s; background: #5d3df2; }
    .voice-wave-container .stroke:nth-child(7) { animation-delay: 0.1s; background: #00e5ff; }

    @keyframes animateWave {
        0% { height: 8px; }
        50% { height: 45px; }
        100% { height: 8px; }
    }

    /* Custom Scrollbars */
    ::-webkit-scrollbar {
        width: 6px; height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.2);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(0, 229, 255, 0.15);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(181, 55, 242, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Main Title and Subtitle Header
st.markdown("<h1 class='main-title'>OMNIMIND AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>QUANTUM NEURAL OS_V2.0.4</p>", unsafe_allow_html=True)

# Initialize global session states for high-end UI interactivity
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "voice_history" not in st.session_state:
    st.session_state.voice_history = []
if "clicked_prompt" not in st.session_state:
    st.session_state.clicked_prompt = None
if "simulated_sys_logs" not in st.session_state:
    st.session_state.simulated_sys_logs = [
        "[OK] CORE NEURAL ARCH BOOTED IN 0.082s",
        "[OK] SQLITE IMMUTABLE DATABASE SECURED & INDEXED",
        "[OK] SPEECH COGNITION ENGINE CALIBRATED",
        "[OK] QUANTUM TELEMETRY BUFFER FLUSHED",
        "[OK] ALL COGNITIVE CHANNELS STEADY"
    ]

# Custom Sidebar Layout with Diagnostics Panel & Navigation
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; margin-bottom: 1.5rem;'>
            <h2 style='font-family: "Syncopate", sans-serif; font-size: 1.2rem; letter-spacing: 3px; color: #00e5ff; text-shadow: 0 0 20px rgba(0, 229, 255, 0.4); border-bottom: 1px solid rgba(0,229,255,0.12); padding-bottom: 10px; margin-bottom: 0;'>SYSTEM CORE</h2>
            <div style='margin-top: 8px; display: flex; align-items: center; justify-content: center; font-size: 0.72rem; color: #10b981; font-family: "Space Grotesk", sans-serif; font-weight: 600; letter-spacing: 1px;'>
                <span class='pulse-indicator'></span> COGNITIVE BRIDGE ACTIVE
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Custom Sidebar Navigation Menu (styled using the stRadio hacks above)
    menu = st.radio("", ["🧠 Core Engine", "📄 Document Intel", "🎙️ Voice Synthesis", "💾 Neural Memory", "📈 System Analytics"], label_visibility="collapsed")
    
    # Interactive Sidebar Tuning Panel
    st.markdown("""
        <div style='margin-top: 2rem; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 15px;'>
            <h4 style='font-family: "Syncopate", sans-serif; font-size: 0.75rem; color: #b537f2; letter-spacing: 1.5px; margin-bottom: 15px;'>COG PARAMETERS</h4>
        </div>
    """, unsafe_allow_html=True)
    
    st.slider("Neural Temperature", min_value=0.1, max_value=1.2, value=0.7, step=0.05, key="sidebar_temp")
    st.select_slider("Synaptic Priority", options=["Low Latency", "High Density", "Deep Reasoning"], value="Deep Reasoning", key="sidebar_priority")
    
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    
    # Action Panel
    st.markdown("""
        <div style='border-top: 1px solid rgba(255,255,255,0.08); padding-top: 15px; margin-bottom: 12px;'>
            <h4 style='font-family: "Syncopate", sans-serif; font-size: 0.75rem; color: #f43f5e; letter-spacing: 1.5px;'>SYSTEM OPERATIONS</h4>
        </div>
    """, unsafe_allow_html=True)
    
    purge_col, reset_col = st.columns(2)
    with purge_col:
        st.markdown("<div class='purge-btn'>", unsafe_allow_html=True)
        purge_db = st.button("🗑️ Purge DB", use_container_width=True, help="Wipe memory database permanently")
        st.markdown("</div>", unsafe_allow_html=True)
    with reset_col:
        reset_session = st.button("🔄 Reset UI", use_container_width=True, help="Clean frontend memory buffer")
        
    if purge_db:
        try:
            res = requests.post("http://127.0.0.1:8000/clear_history")
            st.session_state.chat_history = []
            st.session_state.voice_history = []
            log_time = time.strftime("%H:%M:%S")
            st.session_state.simulated_sys_logs.append(f"[{log_time}] [SYS] COGNITIVE MEMORY PURGED")
            st.success("Memory banks cleared.")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to clear memory: {e}")
            
    if reset_session:
        st.session_state.chat_history = []
        st.session_state.voice_history = []
        log_time = time.strftime("%H:%M:%S")
        st.session_state.simulated_sys_logs.append(f"[{log_time}] [SYS] CORE INTERFACE RESET")
        st.rerun()
        
    # Sidebar HUD Diagnostics Panel
    st.markdown("""
        <div class='glass-card border-cyan' style='padding: 18px; margin-top: 2rem; background: rgba(5,4,9,0.7);'>
            <h4 style='font-family: "Syncopate", sans-serif; font-size: 0.7rem; color: #00e5ff; margin-bottom: 12px; letter-spacing: 1px;'>CORE TELEMETRY</h4>
            
            <div style='margin-bottom: 10px;'>
                <div style='display:flex; justify-content:space-between; font-size: 0.75rem; font-family: "Space Grotesk", sans-serif;'>
                    <span>Synaptic Load</span>
                    <span style='color: #00e5ff; font-family: Orbitron; font-weight:700;'>42.7%</span>
                </div>
                <div class='hud-bar-bg'><div class='hud-bar-fill' style='width: 42.7%;'></div></div>
            </div>
            
            <div style='margin-bottom: 10px;'>
                <div style='display:flex; justify-content:space-between; font-size: 0.75rem; font-family: "Space Grotesk", sans-serif;'>
                    <span>Buffer Memory</span>
                    <span style='color: #b537f2; font-family: Orbitron; font-weight:700;'>18.9%</span>
                </div>
                <div class='hud-bar-bg'><div class='hud-bar-fill' style='width: 18.9%; background: #b537f2; box-shadow: 0 0 10px #b537f2;'></div></div>
            </div>

            <div style='display:flex; justify-content:space-between; font-size: 0.75rem; font-family: "Space Grotesk", sans-serif;'>
                <span>Sub-quantum Sync</span>
                <span style='color: #10b981; font-family: Orbitron; font-weight:700;'>99.9%</span>
            </div>
            <div class='hud-bar-bg'><div class='hud-bar-fill' style='width: 99.9%; background: #10b981; box-shadow: 0 0 10px #10b981;'></div></div>
        </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# ACTION ROUTER FOR QUICK-START CARDS
# ----------------------------------------------------
if st.session_state.clicked_prompt:
    prompt_text = st.session_state.clicked_prompt
    st.session_state.clicked_prompt = None  # Clear
    st.session_state.chat_history.append({"role": "user", "content": prompt_text})
    
    # Build logs & execute query
    log_time = time.strftime("%H:%M:%S")
    st.session_state.simulated_sys_logs.append(f"[{log_time}] [CORE] INITIATED QUICK PROMPT PATHWAY")
    
    with st.spinner("Synthesizing response through neural pathways..."):
        try:
            response = requests.post("http://127.0.0.1:8000/chat", json={"question": prompt_text})
            data = response.json()
            st.session_state.chat_history.append({"role": "assistant", "content": data.get("response", "No response")})
            st.session_state.simulated_sys_logs.append(f"[{time.strftime('%H:%M:%S')}] [CORE] TELEMETRY LOAD BALANCED")
            st.rerun()
        except Exception as e:
            st.error(f"Neural Link Severed: {e}")

# ----------------------------------------------------
# 1. CORE ENGINE PAGE (AI Chat)
# ----------------------------------------------------
if menu == "🧠 Core Engine":
    st.markdown("""
    <div class='glass-card border-purple'>
        <h3><span style='font-size:1.6rem; color:#b537f2;'>✨</span> Global AI Intelligence</h3>
        <p>Interact with the primary OmniMind cognitive module. Ask questions, code matrices, or design layouts below. Responsive models auto-load.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom Chat Bubble Area
    if st.session_state.chat_history:
        st.markdown("<h4 style='color: #94a3b8; font-family: Syncopate; font-size: 0.8rem; letter-spacing: 2px; margin-top: 1.5rem;'>ACTIVE CONVERSATION FEED</h4>", unsafe_allow_html=True)
        for msg in st.session_state.chat_history:
            avatar_char = "👤" if msg["role"] == "user" else "🤖"
            with st.chat_message(msg["role"], avatar=avatar_char):
                st.write(msg["content"])
    else:
        # Show premium Quick-Start Prompts when chat is empty
        st.markdown("<h4 style='color: #94a3b8; font-family: Syncopate; font-size: 0.8rem; letter-spacing: 2px; text-align: center; margin-top: 3rem; margin-bottom: 1.5rem;'>SELECT COGNITIVE TEMPLATE PROTOCOL</h4>", unsafe_allow_html=True)
        
        st.markdown("<div class='quickstart-container'>", unsafe_allow_html=True)
        q_col1, q_col2 = st.columns(2)
        with q_col1:
            p1 = st.button("🖥️ **Run System Diagnostics**\n\nSimulate sub-system metrics & verify quantum telemetry.", key="p_diag", use_container_width=True)
            p2 = st.button("🧬 **Analyze Vector RAG**\n\nExplain how embedding stores work in modern architectures.", key="p_vector", use_container_width=True)
        with q_col2:
            p3 = st.button("💻 **Generate Coder Matrix**\n\nWrite a high-performance Python function to optimize math.", key="p_code", use_container_width=True)
            p4 = st.button("📊 **Check Memory Health**\n\nVerify SQLite database and active session traces.", key="p_health", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        if p1:
            st.session_state.clicked_prompt = "Simulate a quantum network diagnostic and print the sub-system latency logs."
            st.rerun()
        if p2:
            st.session_state.clicked_prompt = "Explain how a vector embedding store works in a modern RAG pipeline."
            st.rerun()
        if p3:
            st.session_state.clicked_prompt = "Write a high-performance Python function to optimize matrix multiplications."
            st.rerun()
        if p4:
            st.session_state.clicked_prompt = "Analyze the current memory health status of the OmniMind database."
            st.rerun()

    # Float Input using st.chat_input at the bottom of the viewport
    if user_query := st.chat_input("Prompt the AI operating system..."):
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        log_time = time.strftime("%H:%M:%S")
        st.session_state.simulated_sys_logs.append(f"[{log_time}] [CORE] INFERENCE EXECUTION")
        
        with st.spinner("Synthesizing response through neural pathways..."):
            try:
                response = requests.post("http://127.0.0.1:8000/chat", json={"question": user_query})
                data = response.json()
                st.session_state.chat_history.append({"role": "assistant", "content": data.get("response", "No response")})
                st.session_state.simulated_sys_logs.append(f"[{time.strftime('%H:%M:%S')}] [CORE] RESPONSE COMPILED NOMINAL")
                st.rerun()
            except Exception as e:
                st.error(f"Neural Link Severed: {e}")

# ----------------------------------------------------
# 2. DOCUMENT INTEL PAGE
# ----------------------------------------------------
elif menu == "📄 Document Intel":
    st.markdown("""
    <div class='glass-card border-cyan'>
        <h3><span style='font-size:1.6rem; color:#00e5ff;'>📑</span> Document Intelligence Core</h3>
        <p>Drop PDF files into the RAG slot for automatic deep extraction, index building, and semantic summaries.</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Select PDF Dataset", type="pdf")
    
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        file_size_kb = len(file_bytes) / 1024
        
        # Display Premium File Details Grid
        st.markdown(f"""
        <div class='glass-card border-cyan' style='background: rgba(0, 229, 255, 0.03);'>
            <h4 style='font-family: "Syncopate", sans-serif; font-size: 0.8rem; color: #00e5ff; margin-bottom: 15px;'>DATA SET IDENTIFIED</h4>
            <div style='display: flex; gap: 40px; flex-wrap: wrap;'>
                <div>
                    <div style='font-size:0.75rem; color:#64748b; font-family: Syncopate;'>FILE NAME</div>
                    <div style='font-size:1.1rem; font-weight:600; color:#fff; margin-top:5px;'>{uploaded_file.name}</div>
                </div>
                <div>
                    <div style='font-size:0.75rem; color:#64748b; font-family: Syncopate;'>FILE SIZE</div>
                    <div style='font-size:1.1rem; font-weight:600; color:#fff; margin-top:5px; font-family: Orbitron;'>{file_size_kb:.2f} KB</div>
                </div>
                <div>
                    <div style='font-size:0.75rem; color:#64748b; font-family: Syncopate;'>STREAM TUNER</div>
                    <div style='font-size:1.1rem; font-weight:600; color:#10b981; margin-top:5px;'>READY FOR PARSE</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1.8, 1])
        with col2:
            if st.button("⚡ Start Neural Parsing", use_container_width=True):
                # Fake stepping logs for high-end immersion
                log_placeholder = st.empty()
                logs = [
                    "🧬 Opening document data layer...",
                    "🧬 Extracting raw unicode characters...",
                    "🧬 Aligning semantic vector embeddings...",
                    "🧬 Computing summarized abstraction matrices..."
                ]
                
                # Progress bar for visual feedback
                progress_bar = st.progress(0)
                for index, l in enumerate(logs):
                    log_placeholder.markdown(f"<div style='font-family: monospace; color:#00e5ff; text-align:center; margin-bottom:10px;'>{l}</div>", unsafe_allow_html=True)
                    progress_bar.progress((index + 1) * 25)
                    time.sleep(0.5)
                log_placeholder.empty()
                progress_bar.empty()
                
                with st.spinner("Compiling summary layers..."):
                    try:
                        log_time = time.strftime("%H:%M:%S")
                        st.session_state.simulated_sys_logs.append(f"[{log_time}] PROCESS FILE: {uploaded_file.name}")
                        
                        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                        response = requests.post("http://127.0.0.1:8000/upload_pdf", files=files)
                        summary_txt = response.json().get("pdf_summary", "")
                        
                        st.markdown(f"""
                        <div class='glass-card border-green' style='margin-top: 1.5rem;'>
                            <h4 style='color: #10b981; font-family: Syncopate; font-size: 0.85rem; margin-top:0;'>✅ COGNITIVE SUMMARY GENERATED:</h4>
                            <div style='line-height: 1.6; font-size:1.02rem; color:#e2e8f0;'>{summary_txt}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Processing Error: {e}")

# ----------------------------------------------------
# 3. VOICE SYNTHESIS PAGE
# ----------------------------------------------------
elif menu == "🎙️ Voice Synthesis":
    st.markdown("""
    <div class='glass-card border-rose'>
        <h3><span style='font-size:1.6rem; color:#f43f5e;'>🎙️</span> Voice AI Module</h3>
        <p>Direct speech-to-text transcription and high-speed audio command recognition. Use the HUD recording buttons below.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 1.8])
    
    with col1:
        st.markdown("""
        <div class='glass-card' style='text-align: center; background: rgba(5,4,9,0.5);'>
            <h4 style='font-family: "Syncopate", sans-serif; font-size: 0.8rem; color: #f43f5e; margin-bottom: 20px;'>AUDIO WAVE HUDS</h4>
            <p style='font-size:0.9rem; color:#94a3b8; margin-bottom: 25px;'>Click below to record your voice. Micro-pathways will isolate raw speech.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # HTML/CSS pulsing dynamic soundwave
        st.markdown("""
        <div class='voice-wave-container'>
            <span class='stroke'></span>
            <span class='stroke'></span>
            <span class='stroke'></span>
            <span class='stroke'></span>
            <span class='stroke'></span>
            <span class='stroke'></span>
            <span class='stroke'></span>
        </div>
        """, unsafe_allow_html=True)
        
        # Streamlit mic recorder integration
        from streamlit_mic_recorder import mic_recorder
        
        audio = mic_recorder(
            start_prompt="🎤 Start System Recording",
            stop_prompt="🛑 Stop & Process Transmission",
            just_once=True,
            use_container_width=True
        )
        
        if audio:
            with st.spinner("Processing neural audio..."):
                try:
                    # Append active logs
                    log_time = time.strftime("%H:%M:%S")
                    st.session_state.simulated_sys_logs.append(f"[{log_time}] PROCESS AUDIO TRANSMISSION")
                    
                    files = {"file": ("audio.wav", audio['bytes'], "audio/wav")}
                    response = requests.post("http://127.0.0.1:8000/voice_file", files=files)
                    data = response.json()
                    
                    st.session_state.voice_history.append({
                        "question": data.get("question", "No voice detected"),
                        "response": data.get("response", "Audio synthesis failed")
                    })
                    st.rerun()
                except Exception as e:
                    st.error(f"Auditory Link Severed: {e}")
                    
    with col2:
        if st.session_state.voice_history:
            st.markdown("<h4 style='color: #00e5ff; font-family: Syncopate; font-size: 0.8rem; letter-spacing: 2px; margin-top:0;'>RECENT TRANSMISSION FEEDS</h4>", unsafe_allow_html=True)
            for i, log in enumerate(reversed(st.session_state.voice_history)):
                st.markdown(f"""
                <div class='glass-card border-rose' style='margin-bottom: 12px; padding: 20px;'>
                    <div style='display:flex; justify-content:space-between; margin-bottom: 12px;'>
                        <span style='color:#cbd5e1; font-family: Syncopate; font-size: 0.7rem;'>TRANSMISSION #{len(st.session_state.voice_history)-i}</span>
                        <span style='color:#f43f5e; font-family: Orbitron; font-size: 0.75rem;'>SYNTH nominal</span>
                    </div>
                    <div style='color: #94a3b8; font-size: 0.8rem; margin-bottom: 4px;'>SPEECH INPUT RECEIVED:</div>
                    <div style='background:rgba(255,255,255,0.04); padding:10px 14px; border-radius:6px; font-family:Space Grotesk; margin-bottom:12px;'>"{log['question']}"</div>
                    <div style='color: #f43f5e; font-size: 0.8rem; margin-bottom: 4px;'>OMNIMIND VOCAL ANSWER:</div>
                    <div style='line-height:1.5; font-size:0.95rem; color:#fff;'>{log['response']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='glass-card' style='border: 1px dashed rgba(255,255,255,0.08); text-align: center; padding: 60px; color: #64748b;'>
                🎙️ Audio transmission buffer is clear. Use the recording panel on the left to capture audio patterns.
            </div>
            """, unsafe_allow_html=True)

# ----------------------------------------------------
# 4. NEURAL MEMORY PAGE
# ----------------------------------------------------
elif menu == "💾 Neural Memory":
    st.markdown("""
    <div class='glass-card border-green'>
        <h3><span style='font-size:1.6rem; color:#10b981;'>🗄️</span> Immutable Memory Log</h3>
        <p>Access historical cognitive traces stored within the OmniMind secure database layer.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Retrieve memories from DB
    history = get_history()
    
    # Memory Statistics Widgets
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; padding: 20px 10px;'>
            <div class='hud-metric-label' style='font-family:"Syncopate"; font-size:0.75rem; color:#94a3b8;'>SECTORS OCCUPIED</div>
            <div class='hud-metric-value' style='font-family:"Orbitron"; font-size:2rem; font-weight:700; color:#fff; text-shadow:0 0 10px #00e5ff; margin-top:5px;'>{len(history)} Blocks</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; padding: 20px 10px; border-color: rgba(181, 55, 242, 0.4);'>
            <div class='hud-metric-label' style='font-family:"Syncopate"; font-size:0.75rem; color:#b537f2;'>CYPHER ENCRYPTION</div>
            <div class='hud-metric-value' style='font-family:"Orbitron"; color:#b537f2; font-size: 1.8rem; text-shadow:0 0 15px rgba(181,55,242,0.4); margin-top:5px;'>AES-XTS-256</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; padding: 20px 10px; border-color: rgba(16, 185, 129, 0.4);'>
            <div class='hud-metric-label' style='font-family:"Syncopate"; font-size:0.75rem; color:#10b981;'>INTEGRITY BUFFER</div>
            <div class='hud-metric-value' style='font-family:"Orbitron"; font-size:2rem; font-weight:700; color:#10b981; text-shadow:0 0 15px rgba(16,185,129,0.4); margin-top:5px;'>100%</div>
        </div>
        """, unsafe_allow_html=True)

    # Search Bar for logs
    st.markdown("<br>", unsafe_allow_html=True)
    
    search_col, count_col = st.columns([4, 1.2])
    with search_col:
        search_query = st.text_input("🔍 Search Memory Arrays...", placeholder="Type to filter past prompt patterns...")
    with count_col:
        max_results = st.selectbox("Limit View", [10, 20, 50, 100], index=1)
    
    if not history:
        st.info("Memory banks are currently empty.")
    else:
        st.markdown("<h4 style='color: #00e5ff; font-family: Syncopate; font-size: 0.80rem; letter-spacing: 2px; margin-top: 1rem;'>CHRONOLOGICAL NEURAL TRACES</h4>", unsafe_allow_html=True)
        
        filtered_history = [
            item for item in history 
            if not search_query.strip() or search_query.lower() in item[1].lower() or search_query.lower() in item[2].lower()
        ]
        
        # Apply slice limit
        filtered_history = filtered_history[:max_results]
        
        if not filtered_history:
            st.warning("No memory records matched your filters.")
        else:
            for item in filtered_history:
                with st.expander(f"📌 [{item[3].split()[1] if len(item[3].split()) > 1 else item[3]}] - Prompt: {item[1][:60]}{'...' if len(item[1]) > 60 else ''}"):
                    st.markdown(f"<div style='color:#64748b; font-size:0.8rem; margin-bottom:12px; font-family:monospace;'>INDEX: {item[0]} | SYSTEM TIME: {item[3]}</div>", unsafe_allow_html=True)
                    st.markdown(f"**Prompt Pattern:**<br> <div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); padding:12px; border-radius:6px; margin:5px 0 15px 0;'>{item[1]}</div>", unsafe_allow_html=True)
                    st.markdown(f"**Cognitive Responders:**<br> <div style='background:rgba(181, 55, 242, 0.03); padding:12px; border-left:3px solid #b537f2; border-radius:0 6px 6px 0; margin-top:5px; font-family: Space Grotesk;'>{item[2]}</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# 5. SYSTEM ANALYTICS PAGE
# ----------------------------------------------------
elif menu == "📈 System Analytics":
    st.markdown("""
    <div style='text-align: center; margin-bottom: 25px;'>
        <h1 class='main-title' style='font-size: 2.2rem !important; margin-bottom:0.5rem;'>NEURAL TELEMETRY</h1>
        <p class='sub-title' style='font-size: 0.8rem; margin-bottom: 10px; letter-spacing: 6px;'>System Diagnostics & Real-Time Performance Matrix</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid of Metrics
    history = get_history()
    questions = [item[1] for item in history]
    sizes = [len(q) for q in questions]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; padding: 20px 10px; border-color: rgba(0, 229, 255, 0.4);'>
            <div class='hud-metric-label' style='font-family:"Syncopate"; font-size:0.75rem; color:#00e5ff;'>TOTAL RUN QUERIES</div>
            <div class='hud-metric-value' style='font-family:"Orbitron"; font-size:2rem; font-weight:700; color:#ffffff; text-shadow:0 0 15px rgba(0,229,255,0.5);'>{len(history)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        max_load = max(sizes) if sizes else 0
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; padding: 20px 10px; border-color: rgba(181, 55, 242, 0.4);'>
            <div class='hud-metric-label' style='font-family:"Syncopate"; font-size:0.75rem; color:#b537f2;'>PEAK CHAR LOAD</div>
            <div class='hud-metric-value' style='font-family:"Orbitron"; font-size:2rem; font-weight:700; color:#ffffff; text-shadow:0 0 15px rgba(181,55,242,0.5);'>{max_load}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        status_val = "OPTIMAL" if len(history) > 0 else "STANDBY"
        status_col = "#10b981" if status_val == "OPTIMAL" else "#b537f2"
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; padding: 20px 10px; border-color: rgba(16, 185, 129, 0.4);'>
            <div class='hud-metric-label' style='font-family:"Syncopate"; font-size:0.75rem; color:{status_col};'>OS CORE STATE</div>
            <div class='hud-metric-value' style='font-family:"Orbitron"; font-size:2rem; font-weight:700; color:#ffffff; text-shadow: 0 0 15px {status_col};'>{status_val}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.6, 1])
    
    with col_left:
        # Plotly Area Chart
        if sizes:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(range(1, len(sizes)+1)),
                y=sizes,
                mode='lines+markers',
                name='Load',
                line=dict(color='#00e5ff', width=3, shape='spline'),
                marker=dict(
                    size=10, 
                    color='#b537f2', 
                    line=dict(width=2, color='#ffffff'),
                    symbol='hexagon-open-dot'
                ),
                fill='tozeroy',
                fillcolor='rgba(0, 229, 255, 0.08)',
                hoverinfo='x+y',
                hovertemplate='<b style="font-size:14px; font-family:Orbitron;">Sequence ID %{x}</b><br>Buffer Length: <b>%{y} Chars</b><extra></extra>'
            ))
            
            fig.update_layout(
                title=dict(
                    text='REAL-TIME COMPLEXITY STREAM',
                    font=dict(family='Syncopate', size=14, color='#ffffff'),
                    x=0.5,
                    y=0.9
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    title=dict(text='SEQUENCE ID', font=dict(family='Space Grotesk', color='#94a3b8', size=11)),
                    tickfont=dict(family='Space Grotesk', color='#00e5ff'),
                    showgrid=True,
                    gridcolor='rgba(0, 229, 255, 0.06)',
                    gridwidth=1,
                    zeroline=False
                ),
                yaxis=dict(
                    title=dict(text='CHARACTER LENGTH', font=dict(family='Space Grotesk', color='#94a3b8', size=11)),
                    tickfont=dict(family='Space Grotesk', color='#b537f2'),
                    showgrid=True,
                    gridcolor='rgba(181, 55, 242, 0.06)',
                    gridwidth=1,
                    zeroline=False
                ),
                hovermode='x unified',
                margin=dict(l=20, r=20, t=60, b=20),
                height=380
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("Insufficient load metrics. Interact with the Core Engine to populate complexity matrices.")
            
    with col_right:
        # Load simulated image or diagnostic logs with filter dropdown
        st.markdown("<h4 style='font-family: Syncopate; font-size: 0.8rem; color:#00e5ff; letter-spacing:1px; margin-top:0; margin-bottom: 12px;'>LIVE COGNITIVE LOGS</h4>", unsafe_allow_html=True)
        
        log_level = st.selectbox("Log Filter Protocol", ["All Signals", "OK Codes Only", "SYS Core Operations", "CORE Inference Channels"], label_visibility="collapsed")
        
        # Custom system events display in a terminal-like console box
        filtered_logs = st.session_state.simulated_sys_logs
        if log_level == "OK Codes Only":
            filtered_logs = [l for l in filtered_logs if "[OK]" in l]
        elif log_level == "SYS Core Operations":
            filtered_logs = [l for l in filtered_logs if "[SYS]" in l]
        elif log_level == "CORE Inference Channels":
            filtered_logs = [l for l in filtered_logs if "[CORE]" in l]
            
        log_feed = ""
        for item in reversed(filtered_logs):
            log_feed += f"{item}\n"
            
        st.markdown(f"""
        <pre style='background: #040307; border: 1px solid rgba(0, 229, 255, 0.15); border-radius: 10px; color: #00ff7f; font-family: "JetBrains Mono", monospace; font-size: 0.78rem; padding: 18px; max-height: 290px; overflow-y: auto; box-shadow: inset 0 0 15px rgba(0,0,0,0.9); line-height: 1.5;'>{log_feed}</pre>
        """, unsafe_allow_html=True)
