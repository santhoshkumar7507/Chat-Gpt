import streamlit as st
import requests
from backend.memory import get_history
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="OmniMind AI OS", page_icon="🌌", layout="wide")

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

    /* Sidebar HUD styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(3,3,5,0.95) 0%, rgba(10,5,20,0.98) 100%) !important;
        border-right: 1px solid rgba(0, 229, 255, 0.2);
        box-shadow: 5px 0 30px rgba(0, 229, 255, 0.05);
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
        font-size: 4.5rem !important;
        text-align: center; margin-bottom: 0rem;
        animation: gradientShimmer 4s linear infinite;
        text-shadow: 0 0 30px rgba(0, 229, 255, 0.4);
    }

    .sub-title {
        text-align: center; color: #8b9bb4; font-family: 'Space Grotesk', sans-serif;
        font-weight: 400; font-size: 1.1rem; margin-bottom: 4rem;
        letter-spacing: 8px; text-transform: uppercase;
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
        border-radius: 8px; padding: 35px; margin: 20px 0;
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
        transform: translateY(-8px) scale(1.01);
        border-color: rgba(181, 55, 242, 0.6);
        box-shadow: 0 20px 50px rgba(181, 55, 242, 0.15), inset 0 0 20px rgba(181, 55, 242, 0.05);
    }
    
    .glass-card:hover::before { left: 200%; }

    .glass-card h3 { color: #ffffff; font-size: 1.4rem; display: flex; align-items: center; gap: 15px; text-shadow: 0 0 10px rgba(255,255,255,0.2); }
    .glass-card p { color: #94a3b8; font-size: 1.1rem; margin-top: 15px; font-family: 'Space Grotesk', sans-serif; text-transform: none; letter-spacing: 0.5px; line-height: 1.6; }

    /* Input Fields Terminal Style */
    .stTextArea textarea {
        background: rgba(0, 0, 0, 0.6) !important;
        border: 1px solid rgba(0, 229, 255, 0.2) !important;
        color: #00e5ff !important; border-radius: 6px !important;
        padding: 20px !important; font-size: 1.1rem !important;
        transition: all 0.4s ease !important; font-family: 'Space Grotesk', monospace !important;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5) !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #b537f2 !important;
        box-shadow: 0 0 20px rgba(181, 55, 242, 0.2), inset 0 0 15px rgba(181, 55, 242, 0.1) !important;
    }

    /* Cyber Buttons */
    .stButton>button {
        background: rgba(0, 229, 255, 0.05) !important;
        color: #00e5ff !important;
        border: 1px solid #00e5ff !important; border-radius: 4px !important;
        padding: 1rem 2.5rem !important; font-family: 'Syncopate', sans-serif !important;
        font-weight: 700 !important; font-size: 0.95rem !important;
        letter-spacing: 3px !important; transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
        text-transform: uppercase; position: relative; overflow: hidden;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.1) !important;
    }
    
    .stButton>button:hover {
        background: rgba(181, 55, 242, 0.15) !important;
        color: #fff !important; border-color: #b537f2 !important;
        box-shadow: 0 0 30px rgba(181, 55, 242, 0.4), inset 0 0 15px rgba(181, 55, 242, 0.2) !important;
        transform: translateY(-3px) !important; text-shadow: 0 0 8px rgba(255,255,255,0.5) !important;
    }
    
    .stButton>button:active { transform: translateY(2px) !important; box-shadow: 0 0 10px rgba(181, 55, 242, 0.2) !important; }

    /* File uploader HUD */
    [data-testid="stFileUploader"] {
        background: rgba(0, 229, 255, 0.02);
        border: 1px dashed rgba(0, 229, 255, 0.4);
        border-radius: 6px; padding: 30px; transition: all 0.4s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #b537f2; background: rgba(181, 55, 242, 0.08); box-shadow: 0 0 25px rgba(181, 55, 242, 0.15);
    }
    
    /* Expanders Memory Log */
    .streamlit-expanderHeader {
        background-color: rgba(0, 229, 255, 0.03) !important;
        border-radius: 6px !important; font-family: 'Space Grotesk', sans-serif !important;
        border: 1px solid rgba(0, 229, 255, 0.1) !important; color: #00e5ff !important;
        transition: all 0.3s ease !important;
    }
    .streamlit-expanderHeader:hover { background-color: rgba(0, 229, 255, 0.08) !important; border-color: #00e5ff !important; }
    
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>OMNIMIND AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>QUANTUM NEURAL OS_V2</p>", unsafe_allow_html=True)

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
        st.markdown("<div style='text-align: center; margin-bottom: 20px;'><p style='color: #cbd5e1;'>Record directly from your browser to bypass hardware driver issues.</p></div>", unsafe_allow_html=True)
        from streamlit_mic_recorder import mic_recorder
        
        audio = mic_recorder(
            start_prompt="🎤 Start Recording",
            stop_prompt="🛑 Stop Recording",
            just_once=True,
            use_container_width=True
        )
        
        if audio:
            with st.spinner("Processing neural audio..."):
                try:
                    files = {"file": ("audio.wav", audio['bytes'], "audio/wav")}
                    response = requests.post("http://127.0.0.1:8000/voice_file", files=files)
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
        import plotly.graph_objects as go
        
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
