import streamlit as st
import requests
from backend.memory import get_history
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="OmniMind AI OS", page_icon="🌌", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;500;700&display=swap');

    /* Global styling */
    .stApp {
        background: radial-gradient(circle at 15% 50%, rgba(20, 10, 40, 1), transparent 50%),
                    radial-gradient(circle at 85% 30%, rgba(10, 30, 60, 1), transparent 50%),
                    #09090b; /* Very dark slate */
        background-attachment: fixed;
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }

    /* Floating glowing orbs background effect */
    .stApp::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(circle at 50% 50%, rgba(139, 92, 246, 0.05) 0%, transparent 60%);
        pointer-events: none;
        z-index: 0;
    }

    .stAppHeader { background-color: transparent !important; }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 15, 20, 0.6) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Headings */
    h1, h2, h3, h4 {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    .main-title {
        background: linear-gradient(120deg, #a78bfa 0%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: glow 3s ease-in-out infinite alternate;
    }

    .sub-title {
        text-align: center;
        color: #94a3b8;
        font-weight: 300;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }

    @keyframes glow {
        0% { text-shadow: 0 0 20px rgba(167, 139, 250, 0.1); }
        100% { text-shadow: 0 0 30px rgba(56, 189, 248, 0.4); }
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 30px;
        margin: 15px 0;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: rgba(167, 139, 250, 0.3);
        box-shadow: 0 20px 40px -10px rgba(139, 92, 246, 0.15);
    }

    .glass-card h3 {
        color: #f8fafc;
        margin-top: 0;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.5rem;
    }
    
    .glass-card p {
        color: #cbd5e1;
        font-size: 1rem;
        margin: 0;
    }

    /* Input Fields */
    .stTextArea textarea {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 15px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2) !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.5px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        width: auto !important;
        display: inline-block !important;
        box-shadow: 0 10px 20px -10px rgba(168, 85, 247, 0.6) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 15px 25px -10px rgba(168, 85, 247, 0.8) !important;
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%);
    }
    
    .stButton>button:active {
        transform: translateY(1px) scale(0.98) !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.02);
        border: 2px dashed rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(167, 139, 250, 0.5);
        background: rgba(167, 139, 250, 0.05);
    }
    
    /* Expanders for memory */
    .streamlit-expanderHeader {
        background-color: rgba(255,255,255,0.03) !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
    }
    
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>OmniMind AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Advanced Neural Operating System</p>", unsafe_allow_html=True)

# Custom Sidebar Styling
with st.sidebar:
    st.markdown("<h2 style='text-align: center; margin-bottom: 2rem; background: linear-gradient(90deg, #e2e8f0, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Modules</h2>", unsafe_allow_html=True)
    menu = st.radio("", ["🧠 Core Engine", "📄 Document Intel", "🎙️ Voice Synthesis", "💾 Neural Memory", "📈 System Analytics"], label_visibility="collapsed")

if menu == "🧠 Core Engine":
    st.markdown("""
    <div class='glass-card'>
        <h3><span style='font-size:1.8rem;'>✨</span> Global AI Intelligence</h3>
        <p>Interact with the primary cognitive module powered by Llama 3.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for response
    if "last_query" not in st.session_state:
        st.session_state.last_query = ""
    if "last_response" not in st.session_state:
        st.session_state.last_response = ""
        
    question = st.text_area("Initialize prompt sequence...", height=150, placeholder="Ask the system anything...")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Execute Neural Query", use_container_width=True):
            if question.strip():
                with st.spinner("Synthesizing response through neural pathways... (This may take 15-30 seconds depending on system load)"):
                    try:
                        response = requests.post("http://127.0.0.1:8000/chat", json={"question": question})
                        data = response.json()
                        st.session_state.last_query = question
                        st.session_state.last_response = data.get("response", "No response")
                    except Exception as e:
                        st.error(f"Neural Link Severed: {e}")
            else:
                st.warning("Please provide a prompt to execute.")
                
    # Display the stored response if it exists
    if st.session_state.last_response:
        st.markdown(f"""
        <div class='glass-card' style='border-left: 4px solid #a855f7; margin-top: 2rem;'>
            <h4 style='color: #a78bfa; margin-top: 0; font-family: Outfit;'>Transmission Received:</h4>
            <div style='line-height: 1.6; font-size: 1.05rem;'>{st.session_state.last_response}</div>
        </div>
        """, unsafe_allow_html=True)

elif menu == "📄 Document Intel":
    st.markdown("""
    <div class='glass-card'>
        <h3><span style='font-size:1.8rem;'>📑</span> Document Intelligence</h3>
        <p>Upload PDF datasets for automated extraction and contextual analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Select PDF Dataset", type="pdf")
    
    if uploaded_file is not None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("⚡ Process Document", use_container_width=True):
                with st.spinner("Analyzing document structure and content..."):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                        response = requests.post("http://127.0.0.1:8000/upload_pdf", files=files)
                        st.markdown(f"""
                        <div class='glass-card' style='border-left: 4px solid #38bdf8; margin-top: 2rem;'>
                            <h4 style='color: #7dd3fc; margin-top: 0; font-family: Outfit;'>Document Summary:</h4>
                            <div style='line-height: 1.6;'>{response.json().get("pdf_summary", "")}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Processing Error: {e}")

elif menu == "🎙️ Voice Synthesis":
    st.markdown("""
    <div class='glass-card' style='text-align: center; padding: 40px;'>
        <h3 style='justify-content: center; font-size: 2rem;'><span style='font-size:2.5rem;'>🎙️</span> Voice AI Module</h3>
        <p style='margin-bottom: 20px;'>Advanced Speech-to-Text & Text-to-Speech Engine</p>
    </div>
    """, unsafe_allow_html=True)
    
    if "voice_log" not in st.session_state:
        st.session_state.voice_log = []
        
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='text-align: center; margin-bottom: 20px;'><p style='color: #cbd5e1;'>Ensure your microphone is connected before initializing auditory link.</p></div>", unsafe_allow_html=True)
        if st.button("🎤 Initialize Auditory Link", use_container_width=True):
            with st.spinner("Listening... Speak now into your microphone..."):
                try:
                    response = requests.post("http://127.0.0.1:8000/voice")
                    data = response.json()
                    st.session_state.voice_log.append({
                        "q": data.get("question", "No audio detected"),
                        "a": data.get("response", "Voice Error")
                    })
                except Exception as e:
                    st.error(f"Auditory Link Severed: {e}")
                    
    if st.session_state.voice_log:
        st.markdown("<h4 style='color: #38bdf8; font-family: Outfit; margin-top: 30px;'>Recent Voice Transmissions:</h4>", unsafe_allow_html=True)
        for log in reversed(st.session_state.voice_log):
            st.markdown(f"""
            <div class='glass-card' style='border-left: 4px solid #f43f5e; margin-bottom: 10px;'>
                <div style='color: #94a3b8; font-size: 0.9rem; margin-bottom: 8px;'>You Said:</div>
                <div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:5px; margin-bottom: 15px;'>"{log['q']}"</div>
                <div style='color: #f43f5e; font-size: 0.9rem; margin-bottom: 8px;'>OmniMind Responded:</div>
                <div style='line-height: 1.5; font-size: 1.05rem;'>{log['a']}</div>
            </div>
            """, unsafe_allow_html=True)

elif menu == "💾 Neural Memory":
    st.markdown("""
    <div class='glass-card'>
        <h3><span style='font-size:1.8rem;'>🗄️</span> Immutable Memory Log</h3>
        <p>Access historical interaction data across the neural network.</p>
    </div>
    """, unsafe_allow_html=True)
    
    history = get_history()
    if not history:
        st.write("Memory banks are currently empty.")
    else:
        for item in history:
            with st.expander(f"Query: {item[1][:60]}{'...' if len(item[1]) > 60 else ''}"):
                st.markdown(f"<div style='color:#94a3b8; font-size:0.9rem; margin-bottom:10px;'>Timestamp: {item[3]}</div>", unsafe_allow_html=True)
                st.markdown(f"**Prompt:**<br> <div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:5px; margin:5px 0 15px 0;'>{item[1]}</div>", unsafe_allow_html=True)
                st.markdown(f"**Output:**<br> <div style='background:rgba(167, 139, 250, 0.05); padding:10px; border-left:3px solid #a855f7; border-radius:0 5px 5px 0; margin-top:5px;'>{item[2]}</div>", unsafe_allow_html=True)

elif menu == "📈 System Analytics":
    st.markdown("""
    <div class='glass-card'>
        <h3><span style='font-size:1.8rem;'>📊</span> Network Telemetry</h3>
        <p>Real-time analytical visualization of system load and usage patterns.</p>
    </div>
    """, unsafe_allow_html=True)
    
    history = get_history()
    questions = [item[1] for item in history]
    sizes = [len(q) for q in questions]
    
    if sizes:
        # Create a more beautiful plot
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Smooth line or just nice markers with gradient feel
        ax.plot(range(1, len(sizes)+1), sizes, marker='o', markersize=8, linestyle='-', linewidth=2, color='#a855f7', mfc='#38bdf8', mec='white')
        
        # Grid and styling
        ax.grid(color='rgba(255,255,255,0.1)', linestyle='--', linewidth=0.5)
        ax.set_title('Query Complexity Over Time', color='white', fontname='Outfit', fontsize=16, pad=20)
        ax.set_ylabel('Token / Character Load', color='#94a3b8', fontname='Inter')
        ax.set_xlabel('Sequence ID', color='#94a3b8', fontname='Inter')
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('rgba(255,255,255,0.2)')
        ax.spines['bottom'].set_color('rgba(255,255,255,0.2)')
        ax.tick_params(colors='#cbd5e1')
        
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)
        
        st.pyplot(fig)
    else:
        st.info("Insufficient data to generate telemetry. Please interact with the Core Engine.")
