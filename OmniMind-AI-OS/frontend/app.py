import streamlit as st
import requests
from backend.memory import get_history
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import time
import os

st.set_page_config(page_title="OmniMind AI OS", page_icon="🌌", layout="wide")

# Inject premium CSS styles with custom glowing HUD components, animations, and typography
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Space+Grotesk:wght@300;400;600;700&family=Syncopate:wght@400;700&display=swap');

    /* Global styling with Cyber Grid */
    .stApp {
        background-color: #030305;
        background-image: 
            linear-gradient(rgba(0, 229, 255, 0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 229, 255, 0.04) 1px, transparent 1px),
            radial-gradient(circle at 50% 0%, rgba(181, 55, 242, 0.15) 0%, transparent 60%),
            radial-gradient(circle at 50% 100%, rgba(0, 229, 255, 0.15) 0%, transparent 70%);
        background-size: 45px 45px, 45px 45px, 100% 100%, 100% 100%;
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

    /* Sidebar HUD styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(3,3,5,0.98) 0%, rgba(10,5,25,0.99) 100%) !important;
        border-right: 1px solid rgba(0, 229, 255, 0.25);
        box-shadow: 5px 0 30px rgba(0, 229, 255, 0.08);
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
        font-size: 4rem !important;
        font-weight: 700;
        text-align: center; margin-bottom: 0rem;
        animation: gradientShimmer 4s linear infinite;
        text-shadow: 0 0 35px rgba(0, 229, 255, 0.5);
    }

    .sub-title {
        text-align: center; color: #8b9bb4; font-family: 'Space Grotesk', sans-serif;
        font-weight: 400; font-size: 1rem; margin-bottom: 3rem;
        letter-spacing: 10px; text-transform: uppercase;
        text-shadow: 0 0 8px rgba(139, 155, 180, 0.3);
    }

    @keyframes gradientShimmer {
        0% { background-position: 0% 50%; }
        100% { background-position: 300% 50%; }
    }

    /* Quantum Glass Cards */
    .glass-card {
        background: rgba(10, 10, 22, 0.65);
        backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(0, 229, 255, 0.15);
        border-radius: 12px; padding: 25px; margin: 15px 0;
        box-shadow: inset 0 0 30px rgba(0, 229, 255, 0.02), 0 15px 35px rgba(0,0,0,0.85);
        position: relative; overflow: hidden;
        transition: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
    }
    
    .glass-card::before {
        content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(181, 55, 242, 0.1), transparent);
        transition: all 0.8s ease; transform: skewX(-20deg);
    }

    .glass-card:hover {
        transform: translateY(-5px);
        border-color: rgba(181, 55, 242, 0.5);
        box-shadow: 0 15px 35px rgba(181, 55, 242, 0.15), inset 0 0 20px rgba(181, 55, 242, 0.05);
    }
    
    .glass-card:hover::before { left: 200%; }

    .glass-card h3 { color: #ffffff; font-size: 1.3rem; display: flex; align-items: center; gap: 12px; text-shadow: 0 0 10px rgba(255,255,255,0.2); margin-top: 0; }
    .glass-card p { color: #94a3b8; font-size: 1rem; margin-top: 10px; font-family: 'Space Grotesk', sans-serif; text-transform: none; letter-spacing: 0.5px; line-height: 1.6; }

    /* Neo borders */
    .border-cyan { border-left: 4px solid #00e5ff !important; }
    .border-purple { border-left: 4px solid #b537f2 !important; }
    .border-green { border-left: 4px solid #10b981 !important; }
    .border-rose { border-left: 4px solid #f43f5e !important; }

    /* Input Fields Terminal Style */
    .stTextArea textarea {
        background: rgba(0, 0, 0, 0.7) !important;
        border: 1px solid rgba(0, 229, 255, 0.25) !important;
        color: #00e5ff !important; border-radius: 8px !important;
        padding: 18px !important; font-size: 1.05rem !important;
        transition: all 0.4s ease !important; font-family: 'Space Grotesk', monospace !important;
        box-shadow: inset 0 0 15px rgba(0,0,0,0.6) !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #b537f2 !important;
        box-shadow: 0 0 20px rgba(181, 55, 242, 0.25), inset 0 0 15px rgba(181, 55, 242, 0.15) !important;
    }

    /* Cyber Buttons */
    .stButton>button {
        background: rgba(0, 229, 255, 0.04) !important;
        color: #00e5ff !important;
        border: 1px solid #00e5ff !important; border-radius: 6px !important;
        padding: 0.8rem 2rem !important; font-family: 'Syncopate', sans-serif !important;
        font-weight: 700 !important; font-size: 0.85rem !important;
        letter-spacing: 2px !important; transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
        text-transform: uppercase; position: relative; overflow: hidden;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.08) !important;
    }
    
    .stButton>button:hover {
        background: rgba(181, 55, 242, 0.15) !important;
        color: #fff !important; border-color: #b537f2 !important;
        box-shadow: 0 0 25px rgba(181, 55, 242, 0.35), inset 0 0 15px rgba(181, 55, 242, 0.15) !important;
        transform: translateY(-2px) !important; text-shadow: 0 0 8px rgba(255,255,255,0.4) !important;
    }
    
    .stButton>button:active { transform: translateY(1px) !important; }

    /* File uploader HUD */
    [data-testid="stFileUploader"] {
        background: rgba(0, 229, 255, 0.01);
        border: 1px dashed rgba(0, 229, 255, 0.35);
        border-radius: 8px; padding: 25px; transition: all 0.4s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #b537f2; background: rgba(181, 55, 242, 0.06); box-shadow: 0 0 20px rgba(181, 55, 242, 0.1);
    }
    
    /* Expanders Memory Log */
    .streamlit-expanderHeader {
        background-color: rgba(0, 229, 255, 0.02) !important;
        border-radius: 8px !important; font-family: 'Space Grotesk', sans-serif !important;
        border: 1px solid rgba(0, 229, 255, 0.12) !important; color: #00e5ff !important;
        transition: all 0.3s ease !important;
    }
    .streamlit-expanderHeader:hover { background-color: rgba(0, 229, 255, 0.07) !important; border-color: #00e5ff !important; }
    
    /* -------------------------------------
       PREMIUM SIDEBAR RADIO BUTTONS
       ------------------------------------- */
    div[data-testid="stRadio"] > div {
        gap: 12px !important;
    }
    
    div[data-testid="stRadio"] > div > label {
        background: linear-gradient(90deg, rgba(8, 8, 18, 0.9), rgba(16, 12, 28, 0.95)) !important;
        border: 1px solid rgba(0, 229, 255, 0.08) !important;
        border-left: 4px solid rgba(0, 229, 255, 0.2) !important;
        border-radius: 6px !important;
        padding: 12px 18px !important;
        cursor: pointer !important;
        transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
        position: relative;
        overflow: hidden;
        width: 100%;
        display: flex;
        align-items: center;
    }

    div[data-testid="stRadio"] > div > label::before {
        content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(181, 55, 242, 0.15), transparent);
        transition: all 0.6s ease; z-index: 1;
    }

    div[data-testid="stRadio"] > div > label:hover {
        transform: translateX(8px) !important;
        background: linear-gradient(90deg, rgba(16, 8, 32, 0.95), rgba(32, 16, 48, 1)) !important;
        border-color: rgba(181, 55, 242, 0.5) !important;
        border-left: 4px solid #b537f2 !important;
        box-shadow: 0 8px 20px rgba(181, 55, 242, 0.25), inset 0 0 10px rgba(181, 55, 242, 0.08) !important;
    }
    
    div[data-testid="stRadio"] > div > label:hover::before { left: 100%; }

    /* Hide standard radio circle */
    div[data-testid="stRadio"] > div > label > div:first-child { display: none !important; }

    /* Text styling */
    div[data-testid="stRadio"] > div > label > div:nth-child(2) {
        font-family: 'Syncopate', sans-serif !important;
        font-weight: 600 !important; font-size: 0.85rem !important;
        color: #94a3b8 !important; text-transform: uppercase;
        letter-spacing: 1.5px !important; margin-left: 5px !important;
        z-index: 2; transition: all 0.4s ease !important;
    }

    div[data-testid="stRadio"] > div > label:hover > div:nth-child(2) {
        color: #ffffff !important; text-shadow: 0 0 10px rgba(255, 255, 255, 0.5) !important;
        letter-spacing: 3px !important;
    }
    
    @keyframes activePulse {
        0% { box-shadow: 0 0 12px rgba(0, 229, 255, 0.15), inset 0 0 8px rgba(0, 229, 255, 0.08); }
        50% { box-shadow: 0 0 25px rgba(0, 229, 255, 0.4), inset 0 0 15px rgba(0, 229, 255, 0.2); }
        100% { box-shadow: 0 0 12px rgba(0, 229, 255, 0.15), inset 0 0 8px rgba(0, 229, 255, 0.08); }
    }

    /* Active State Radio */
    div[data-testid="stRadio"] > div > label:has(input:checked) {
        background: linear-gradient(90deg, rgba(0, 229, 255, 0.12), rgba(0, 229, 255, 0.04)) !important;
        border-color: #00e5ff !important;
        border-left: 5px solid #00e5ff !important;
        transform: translateX(10px) !important;
        animation: activePulse 2.5s infinite alternate !important;
    }
    
    div[data-testid="stRadio"] > div > label:has(input:checked) > div:nth-child(2) {
        color: #00e5ff !important;
        text-shadow: 0 0 15px rgba(0, 229, 255, 0.7) !important;
        font-weight: 700 !important;
        letter-spacing: 3px !important;
    }

    /* -------------------------------------
       PREMIUM HUD SPEECH BUBBLES
       ------------------------------------- */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 15px;
        margin-bottom: 25px;
    }
    .user-bubble {
        align-self: flex-end;
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.12), rgba(0, 229, 255, 0.03));
        border: 1px solid rgba(0, 229, 255, 0.25);
        border-radius: 12px 12px 0 12px;
        padding: 15px 20px;
        max-width: 80%;
        color: #e2e8f0;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    .ai-bubble {
        align-self: flex-start;
        background: linear-gradient(135deg, rgba(181, 55, 242, 0.12), rgba(181, 55, 242, 0.03));
        border: 1px solid rgba(181, 55, 242, 0.25);
        border-radius: 12px 12px 12px 0;
        padding: 15px 20px;
        max-width: 80%;
        color: #ffffff;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }

    /* Pulsing Audio Circle Animation */
    .pulse-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 120px;
        margin: 20px 0;
    }
    .pulse-circle {
        width: 50px;
        height: 50px;
        background: #00e5ff;
        border-radius: 50%;
        box-shadow: 0 0 25px #00e5ff;
        animation: ringPulse 1.8s infinite ease-in-out;
    }
    @keyframes ringPulse {
        0% { transform: scale(0.85); opacity: 0.6; box-shadow: 0 0 15px #00e5ff; }
        50% { transform: scale(1.3); opacity: 1; box-shadow: 0 0 35px #b537f2; background: #b537f2; }
        100% { transform: scale(0.85); opacity: 0.6; box-shadow: 0 0 15px #00e5ff; }
    }

    /* Terminal HUD Metrics */
    .hud-metric-label {
        font-family: 'Syncopate', sans-serif;
        font-size: 0.75rem;
        color: #8b9bb4;
        letter-spacing: 1.5px;
        margin-bottom: 5px;
    }
    .hud-metric-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
        text-shadow: 0 0 15px rgba(0, 229, 255, 0.4);
    }
    .hud-bar-bg {
        background: rgba(255,255,255,0.06);
        border-radius: 4px;
        height: 6px;
        width: 100%;
        margin-top: 8px;
        overflow: hidden;
    }
    .hud-bar-fill {
        height: 100%;
        border-radius: 4px;
        background: linear-gradient(90deg, #00e5ff, #b537f2);
        box-shadow: 0 0 10px #00e5ff;
    }

    /* Custom scrollbar for chat logs */
    .chat-scroll {
        max-height: 450px;
        overflow-y: auto;
        padding-right: 10px;
    }
    .chat-scroll::-webkit-scrollbar {
        width: 4px;
    }
    .chat-scroll::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.1);
    }
    .chat-scroll::-webkit-scrollbar-thumb {
        background: rgba(0, 229, 255, 0.2);
        border-radius: 2px;
    }
    .chat-scroll::-webkit-scrollbar-thumb:hover {
        background: rgba(181, 55, 242, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Main Title and Subtitle Header
st.markdown("<h1 class='main-title'>OMNIMIND AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>QUANTUM NEURAL OS_V2.0</p>", unsafe_allow_html=True)

# Initialize global session states for high-end UI interactivity
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "voice_history" not in st.session_state:
    st.session_state.voice_history = []
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
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h2 style='font-family: "Syncopate", sans-serif; font-size: 1.3rem; letter-spacing: 3px; color: #00e5ff; text-shadow: 0 0 20px rgba(0, 229, 255, 0.4); border-bottom: 1px solid rgba(0,229,255,0.15); padding-bottom: 12px; margin-bottom: 0;'>SYSTEM CORE</h2>
            <p style='font-family: "Space Grotesk", sans-serif; font-size: 0.7rem; color: #b537f2; letter-spacing: 2px; margin-top: 6px; text-transform: uppercase;'>Quantum HUD Controller</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Custom Sidebar Navigation Menu
    menu = st.radio("", ["🧠 Core Engine", "📄 Document Intel", "🎙️ Voice Synthesis", "💾 Neural Memory", "📈 System Analytics"], label_visibility="collapsed")
    
    # Sidebar HUD Diagnostics Panel
    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div class='glass-card border-cyan' style='padding: 15px; margin-top: 2rem;'>
            <h4 style='font-family: "Syncopate", sans-serif; font-size: 0.75rem; color: #00e5ff; margin-bottom: 12px; letter-spacing: 1px;'>CORE HEALTH</h4>
            
            <div style='margin-bottom: 10px;'>
                <div style='display:flex; justify-content:space-between; font-size: 0.8rem;'>
                    <span>Synaptic Load</span>
                    <span style='color: #00e5ff; font-family: Orbitron;'>42.7%</span>
                </div>
                <div class='hud-bar-bg'><div class='hud-bar-fill' style='width: 42.7%;'></div></div>
            </div>
            
            <div style='margin-bottom: 10px;'>
                <div style='display:flex; justify-content:space-between; font-size: 0.8rem;'>
                    <span>Buffer Memory</span>
                    <span style='color: #b537f2; font-family: Orbitron;'>18.9%</span>
                </div>
                <div class='hud-bar-bg'><div class='hud-bar-fill' style='width: 18.9%; background: #b537f2; box-shadow: 0 0 10px #b537f2;'></div></div>
            </div>

            <div style='display:flex; justify-content:space-between; font-size: 0.8rem;'>
                <span>Sub-quantum Sync</span>
                <span style='color: #10b981; font-family: Orbitron;'>99.9%</span>
            </div>
            <div class='hud-bar-bg'><div class='hud-bar-fill' style='width: 99.9%; background: #10b981; box-shadow: 0 0 10px #10b981;'></div></div>
        </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# 1. CORE ENGINE PAGE
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
        chat_html = "<div class='chat-container chat-scroll'>"
        for msg in st.session_state.chat_history:
            bubble_class = "user-bubble" if msg["role"] == "user" else "ai-bubble"
            sender_label = "👤 YOU" if msg["role"] == "user" else "🤖 OMNIMIND AI"
            sender_color = "#00e5ff" if msg["role"] == "user" else "#b537f2"
            chat_html += f"""
            <div class='{bubble_class}'>
                <div style='font-family: Syncopate; font-size: 0.75rem; color: {sender_color}; letter-spacing: 1px; margin-bottom: 6px;'>{sender_label}</div>
                <div style='font-family: Space Grotesk; line-height: 1.5;'>{msg["content"]}</div>
            </div>
            """
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='glass-card' style='border: 1px dashed rgba(255,255,255,0.08); text-align: center; padding: 40px; color: #64748b;'>
            💬 Conversation feed is empty. Initialize the sequence below to establish a neural connection.
        </div>
        """, unsafe_allow_html=True)
        
    question = st.text_area("Initialize prompt sequence...", height=120, placeholder="Ask the system anything...")
    
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        btn_cols = st.columns([2, 1])
        with btn_cols[0]:
            execute_query = st.button("🚀 Execute Neural Query", use_container_width=True)
        with btn_cols[1]:
            clear_chat = st.button("🗑️ Reset", use_container_width=True)
            
        if execute_query:
            if question.strip():
                st.session_state.chat_history.append({"role": "user", "content": question})
                with st.spinner("Synthesizing response through neural pathways..."):
                    try:
                        # Append a fresh timestamp to active logs
                        log_time = time.strftime("%H:%M:%S")
                        st.session_state.simulated_sys_logs.append(f"[{log_time}] EXECUTE PROMPT PATHWAY")
                        
                        response = requests.post("http://127.0.0.1:8000/chat", json={"question": question})
                        data = response.json()
                        st.session_state.chat_history.append({"role": "assistant", "content": data.get("response", "No response")})
                        st.rerun()
                    except Exception as e:
                        st.error(f"Neural Link Severed: {e}")
            else:
                st.warning("Please provide a prompt to execute.")
                
        if clear_chat:
            st.session_state.chat_history = []
            st.rerun()

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
        # Calculate file metrics dynamically
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
                for l in logs:
                    log_placeholder.markdown(f"<div style='font-family: monospace; color:#00e5ff; text-align:center;'>{l}</div>", unsafe_allow_html=True)
                    time.sleep(0.6)
                log_placeholder.empty()
                
                with st.spinner("Compiling summary layers..."):
                    try:
                        # Append a fresh timestamp to active logs
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
        <div class='glass-card' style='text-align: center;'>
            <h4 style='font-family: "Syncopate", sans-serif; font-size: 0.8rem; color: #f43f5e; margin-bottom: 20px;'>AUDIO WAVE HUDS</h4>
            <p style='font-size:0.9rem; color:#94a3b8;'>Click below to record your voice. Micro-pathways will isolate raw speech.</p>
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
            st.markdown("""
            <div class='pulse-container'>
                <div class='pulse-circle'></div>
            </div>
            <div style='text-align: center; color: #00e5ff; font-family: monospace; font-size: 0.8rem; margin-bottom: 20px;'>Analyzing Auditory Spline Waves...</div>
            """, unsafe_allow_html=True)
            
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
            <div class='glass-card' style='border: 1px dashed rgba(255,255,255,0.08); text-align: center; padding: 50px; color: #64748b;'>
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
            <div class='hud-metric-label'>SECTORS OCCUPIED</div>
            <div class='hud-metric-value'>{len(history)} Blocks</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; padding: 20px 10px; border-color: rgba(181, 55, 242, 0.4);'>
            <div class='hud-metric-label' style='color:#b537f2;'>CYPHER ENCRYPTION</div>
            <div class='hud-metric-value' style='color:#b537f2; font-size: 1.8rem; text-shadow:0 0 15px rgba(181,55,242,0.4); margin-top:5px;'>AES-XTS-256</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; padding: 20px 10px; border-color: rgba(16, 185, 129, 0.4);'>
            <div class='hud-metric-label' style='color:#10b981;'>INTEGRITY BUFFER</div>
            <div class='hud-metric-value' style='color:#10b981; text-shadow:0 0 15px rgba(16,185,129,0.4);'>100%</div>
        </div>
        """, unsafe_allow_html=True)

    # Search Bar for logs
    st.markdown("<br>", unsafe_allow_html=True)
    search_query = st.text_input("🔍 Search Memory Arrays...", placeholder="Type to filter past prompt patterns...")
    
    if not history:
        st.info("Memory banks are currently empty.")
    else:
        st.markdown("<h4 style='color: #00e5ff; font-family: Syncopate; font-size: 0.80rem; letter-spacing: 2px;'>CHRONOLOGICAL NEURAL TRACES</h4>", unsafe_allow_html=True)
        
        filtered_history = [
            item for item in history 
            if not search_query.strip() or search_query.lower() in item[1].lower() or search_query.lower() in item[2].lower()
        ]
        
        if not filtered_history:
            st.warning("No memory records matched your filters.")
        else:
            for item in filtered_history:
                with st.expander(f"📌 [{item[3].split()[1] if len(item[3].split()) > 1 else item[3]}] - Prompt: {item[1][:60]}{'...' if len(item[1]) > 60 else ''}"):
                    st.markdown(f"<div style='color:#64748b; font-size:0.8rem; margin-bottom:12px; font-family:monospace;'>INDEX: {item[0]} | SYSTEM TIME: {item[3]}</div>", unsafe_allow_html=True)
                    st.markdown(f"**Prompt Pattern:**<br> <div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); padding:12px; border-radius:6px; margin:5px 0 15px 0;'>{item[1]}</div>", unsafe_allow_html=True)
                    st.markdown(f"**Cognitive Responders:**<br> <div style='background:rgba(181, 55, 242, 0.03); padding:12px; border-left:3px solid #b537f2; border-radius:0 6px 6px 0; margin-top:5px;'>{item[2]}</div>", unsafe_allow_html=True)

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
            <div class='hud-metric-label' style='color:#00e5ff;'>TOTAL RUN QUERIES</div>
            <div class='hud-metric-value' style='color:#ffffff; text-shadow:0 0 15px rgba(0,229,255,0.5);'>{len(history)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        max_load = max(sizes) if sizes else 0
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; padding: 20px 10px; border-color: rgba(181, 55, 242, 0.4);'>
            <div class='hud-metric-label' style='color:#b537f2;'>PEAK CHAR LOAD</div>
            <div class='hud-metric-value' style='color:#ffffff; text-shadow:0 0 15px rgba(181,55,242,0.5);'>{max_load}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        status_val = "OPTIMAL" if len(history) > 0 else "STANDBY"
        status_col = "#10b981" if status_val == "OPTIMAL" else "#b537f2"
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; padding: 20px 10px; border-color: rgba(16, 185, 129, 0.4);'>
            <div class='hud-metric-label' style='color:{status_col};'>OS CORE STATE</div>
            <div class='hud-metric-value' style='color:#ffffff; text-shadow: 0 0 15px {status_col};'>{status_val}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.5, 1])
    
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
        # Load simulated image or diagnostic logs
        st.markdown("<h4 style='font-family: Syncopate; font-size: 0.8rem; color:#00e5ff; letter-spacing:1px; margin-top:0;'>LIVE COGNITIVE LOGS</h4>", unsafe_allow_html=True)
        
        # Display custom system events in a terminal-like text box
        log_feed = ""
        for item in reversed(st.session_state.simulated_sys_logs):
            log_feed += f"{item}\n"
            
        st.markdown(f"""
        <pre style='background: rgba(0, 0, 0, 0.8); border: 1px solid rgba(0, 229, 255, 0.2); border-radius: 8px; color: #00ff7f; font-family: monospace; font-size: 0.8rem; padding: 15px; max-height: 330px; overflow-y: auto; box-shadow: inset 0 0 10px rgba(0,255,127,0.1);'>{log_feed}</pre>
        """, unsafe_allow_html=True)
