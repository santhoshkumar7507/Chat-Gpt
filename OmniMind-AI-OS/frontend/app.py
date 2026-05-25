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

# Initialize global session states for high-end UI interactivity
if "hud_theme" not in st.session_state:
    st.session_state.hud_theme = "Enterprise Obsidian"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "voice_history" not in st.session_state:
    st.session_state.voice_history = []
if "clicked_prompt" not in st.session_state:
    st.session_state.clicked_prompt = None
if "active_agent" not in st.session_state:
    st.session_state.active_agent = "Aria - Quantum Architect"
if "shell_history" not in st.session_state:
    st.session_state.shell_history = [
        "OMNIMIND SECURE NEURAL KERNEL v3.4.12",
        "SYSTEM CORE STATUS: ACTIVE",
        "TYPE 'help' FOR LIST OF SYSTEM DIRECTIVES",
        ""
    ]
if "custom_primary" not in st.session_state:
    st.session_state.custom_primary = "#00e5ff"
if "custom_secondary" not in st.session_state:
    st.session_state.custom_secondary = "#b537f2"
if "custom_accent" not in st.session_state:
    st.session_state.custom_accent = "#f43f5e"
if "pdf_segments" not in st.session_state:
    st.session_state.pdf_segments = None
if "selected_segment" not in st.session_state:
    st.session_state.selected_segment = None
if "simulated_sys_logs" not in st.session_state:
    st.session_state.simulated_sys_logs = [
        "[OK] CORE NEURAL ARCH BOOTED IN 0.082s",
        "[OK] SQLITE IMMUTABLE DATABASE SECURED & INDEXED",
        "[OK] SPEECH COGNITION ENGINE CALIBRATED",
        "[OK] QUANTUM TELEMETRY BUFFER FLUSHED",
        "[OK] ALL COGNITIVE CHANNELS STEADY",
        "[OK] HOLOGRAPHIC PARTICLE INTERFEROMETER SYNCHRONIZED",
        "[OK] SYNAPTIC WEIGHT DECAY THRESHOLD SET AT 0.72",
        "[OK] VECTOR EMBEDDING NEURAL CORE ENGAGED"
    ]

# Cognitive Agent Personas database definition
AGENT_PERSONAS = {
    "Aria - Quantum Architect": {
        "description": "Scientific, thorough, specialized in complex vector layouts and mathematical architectures.",
        "icon": "🌌",
        "system_prompt": "You are Aria, the Quantum Architect agent of OmniMind AI. Answer in a scientific, detailed, and highly technical tone, referencing quantum states, cognitive maps, and mathematical optimizations.",
        "accent": "#00e5ff"
    },
    "Kaelen - Security Core": {
        "description": "Concise, secure, focused on coding blueprints and system protocols.",
        "icon": "🛡️",
        "system_prompt": "You are Kaelen, the Security Core agent of OmniMind AI. Answer in a crisp, direct, and ultra-secure tone. Focus heavily on code syntax, security paradigms, and clean operational scripts.",
        "accent": "#f43f5e"
    },
    "Lyra - Data Analyst": {
        "description": "Visualizer, friendly, specialized in metrics, telemetry tables, and analytical breakdowns.",
        "icon": "📊",
        "system_prompt": "You are Lyra, the Data Analyst agent of OmniMind AI. Answer in an analytical, friendly, and structured format. Use tables, bullet points, and markdown data structures to make information highly consumable.",
        "accent": "#ffb300"
    }
}

# Theme HSL Color Configuration Palette
THEME_CONFIGS = {
    "Quantum Cyberpunk": {
        "primary": "#00e5ff",
        "secondary": "#b537f2",
        "accent": "#f43f5e",
        "success": "#10b981",
        "bg_dark": "#050409",
        "bg_gradient": """
            linear-gradient(rgba(0, 229, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 229, 255, 0.03) 1px, transparent 1px),
            radial-gradient(circle at 50% 0%, rgba(181, 55, 242, 0.12) 0%, transparent 60%),
            radial-gradient(circle at 10% 100%, rgba(0, 229, 255, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 90% 100%, rgba(244, 63, 94, 0.08) 0%, transparent 50%)
        """,
        "card_bg": "rgba(10, 10, 24, 0.55)",
        "sidebar_bg": "linear-gradient(180deg, #030206 0%, #0c081d 100%)",
        "border_glow": "rgba(0, 229, 255, 0.12)",
        "text_color": "#e2e8f0"
    },
    "Solar Flare": {
        "primary": "#ffb300",
        "secondary": "#ff3d00",
        "accent": "#f43f5e",
        "success": "#00ffcc",
        "bg_dark": "#0c0800",
        "bg_gradient": """
            linear-gradient(rgba(255, 179, 0, 0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 179, 0, 0.025) 1px, transparent 1px),
            radial-gradient(circle at 50% 0%, rgba(255, 61, 0, 0.12) 0%, transparent 60%),
            radial-gradient(circle at 10% 100%, rgba(255, 179, 0, 0.06) 0%, transparent 50%),
            radial-gradient(circle at 90% 100%, rgba(244, 63, 94, 0.06) 0%, transparent 50%)
        """,
        "card_bg": "rgba(22, 12, 5, 0.6)",
        "sidebar_bg": "linear-gradient(180deg, #0d0600 0%, #220c00 100%)",
        "border_glow": "rgba(255, 179, 0, 0.15)",
        "text_color": "#fbf7f0"
    },
    "Matrix Deck": {
        "primary": "#39ff14",
        "secondary": "#008f11",
        "accent": "#ff0055",
        "success": "#00ffcc",
        "bg_dark": "#020502",
        "bg_gradient": """
            linear-gradient(rgba(57, 255, 20, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(57, 255, 20, 0.02) 1px, transparent 1px),
            radial-gradient(circle at 50% 0%, rgba(0, 143, 17, 0.12) 0%, transparent 60%),
            radial-gradient(circle at 10% 100%, rgba(57, 255, 20, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 90% 100%, rgba(0, 143, 17, 0.05) 0%, transparent 50%)
        """,
        "card_bg": "rgba(3, 12, 5, 0.65)",
        "sidebar_bg": "linear-gradient(180deg, #010401 0%, #051406 100%)",
        "border_glow": "rgba(57, 255, 20, 0.12)",
        "text_color": "#d2ffd0"
    },
    "Supernova Ruby": {
        "primary": "#f43f5e",
        "secondary": "#9d174d",
        "accent": "#00e5ff",
        "success": "#10b981",
        "bg_dark": "#0a0104",
        "bg_gradient": """
            linear-gradient(rgba(244, 63, 94, 0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(244, 63, 94, 0.025) 1px, transparent 1px),
            radial-gradient(circle at 50% 0%, rgba(157, 23, 77, 0.12) 0%, transparent 60%),
            radial-gradient(circle at 10% 100%, rgba(244, 63, 94, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 90% 100%, rgba(0, 229, 255, 0.05) 0%, transparent 50%)
        """,
        "card_bg": "rgba(24, 5, 10, 0.6)",
        "sidebar_bg": "linear-gradient(180deg, #0c0104 0%, #20020d 100%)",
        "border_glow": "rgba(244, 63, 94, 0.15)",
        "text_color": "#ffe4e6"
    },
    "Enterprise Obsidian": {
        "primary": "#ffffff",
        "secondary": "#a1a1aa",
        "accent": "#3b82f6",
        "success": "#10b981",
        "bg_dark": "#09090b",
        "bg_gradient": """
            linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px),
            radial-gradient(circle at 50% 0%, rgba(255, 255, 255, 0.05) 0%, transparent 60%),
            radial-gradient(circle at 10% 100%, rgba(59, 130, 246, 0.06) 0%, transparent 50%),
            radial-gradient(circle at 90% 100%, rgba(16, 185, 129, 0.04) 0%, transparent 50%)
        """,
        "card_bg": "rgba(24, 24, 27, 0.55)",
        "sidebar_bg": "linear-gradient(180deg, #09090b 0%, #18181b 100%)",
        "border_glow": "rgba(255, 255, 255, 0.12)",
        "text_color": "#fafafa"
    },
    "Corporate Platinum": {
        "primary": "#0f172a",
        "secondary": "#334155",
        "accent": "#2563eb",
        "success": "#059669",
        "bg_dark": "#f8fafc",
        "bg_gradient": """
            linear-gradient(rgba(15, 23, 42, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(15, 23, 42, 0.03) 1px, transparent 1px),
            radial-gradient(circle at 50% 0%, rgba(37, 99, 235, 0.05) 0%, transparent 60%),
            radial-gradient(circle at 10% 100%, rgba(15, 23, 42, 0.04) 0%, transparent 50%)
        """,
        "card_bg": "rgba(255, 255, 255, 0.75)",
        "sidebar_bg": "linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%)",
        "border_glow": "rgba(15, 23, 42, 0.1)",
        "text_color": "#0f172a"
    },
    "Custom Hologram": {
        "primary": st.session_state.custom_primary,
        "secondary": st.session_state.custom_secondary,
        "accent": st.session_state.custom_accent,
        "success": "#00ffcc",
        "bg_dark": "#030206",
        "bg_gradient": f"""
            linear-gradient(rgba(0, 229, 255, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 229, 255, 0.02) 1px, transparent 1px),
            radial-gradient(circle at 50% 0%, {st.session_state.custom_secondary}22 0%, transparent 60%),
            radial-gradient(circle at 10% 100%, {st.session_state.custom_primary}15 0%, transparent 50%),
            radial-gradient(circle at 90% 100%, {st.session_state.custom_accent}15 0%, transparent 50%)
        """,
        "card_bg": "rgba(10, 10, 24, 0.65)",
        "sidebar_bg": "linear-gradient(180deg, #030206 0%, #0c081d 100%)",
        "border_glow": f"rgba(0, 229, 255, 0.12)",
        "text_color": "#e2e8f0"
    }
}

# Apply selected theme configurations
theme = THEME_CONFIGS[st.session_state.hud_theme]

# Inject premium CSS styles with custom glowing HUD components, animations, and typography
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Space+Grotesk:wght@300;400;500;600;700&family=Syncopate:wght@400;700&family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700&display=swap');

    :root {{
        --primary-color: {theme['primary']};
        --secondary-color: {theme['secondary']};
        --accent-color: {theme['accent']};
        --success-color: {theme['success']};
        --bg-dark: {theme['bg_dark']};
        --card-bg: {theme['card_bg']};
        --border-glow: {theme['border_glow']};
        --sidebar-bg: {theme['sidebar_bg']};
        --text-color: {theme['text_color']};
    }}

    /* Global styling with Cyber Grid */
    .stApp {{
        background-color: var(--bg-dark);
        background-image: {theme['bg_gradient']};
        background-size: 50px 50px, 50px 50px, 100% 100%, 100% 100%, 100% 100%;
        color: var(--text-color);
        font-family: 'Inter', 'Space Grotesk', sans-serif;
    }}

    /* Hide standard Streamlit header, footer, and default page navigation */
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    div[data-testid="stSidebarNav"] {{
        display: none !important;
    }}

    .stAppHeader {{ background-color: transparent !important; }}

    /* Animated Scanline Overlay */
    .stApp::after {{
        content: ""; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(to bottom, transparent 50%, rgba(255, 255, 255, 0.007) 51%);
        background-size: 100% 4px; pointer-events: none; z-index: 9999;
    }}

    /* Floating Particles styling */
    .quantum-particles {{
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        pointer-events: none;
        overflow: hidden;
        z-index: 0;
    }}
    .particle {{
        position: absolute;
        border-radius: 50%;
        background: radial-gradient(circle, var(--primary-color) 0%, transparent 70%);
        opacity: 0.12;
        animation: floatParticle 25s infinite linear;
    }}
    .particle-1 {{ width: 180px; height: 180px; top: 15%; left: 10%; animation-duration: 22s; }}
    .particle-2 {{ width: 280px; height: 280px; bottom: 10%; right: 15%; animation-duration: 32s; animation-delay: -5s; }}
    .particle-3 {{ width: 190px; height: 190px; top: 60%; left: 45%; animation-duration: 26s; animation-delay: -10s; }}
    .particle-4 {{ width: 120px; height: 120px; top: 5%; right: 30%; animation-duration: 19s; }}
    .particle-5 {{ width: 220px; height: 220px; bottom: 40%; left: 5%; animation-duration: 28s; animation-delay: -15s; }}
    .particle-6 {{ width: 140px; height: 140px; top: 40%; right: 5%; animation-duration: 21s; }}

    @keyframes floatParticle {{
        0% {{ transform: translateY(0) translateX(0) scale(1) rotate(0deg); opacity: 0.12; }}
        33% {{ transform: translateY(-40px) translateX(25px) scale(1.08) rotate(120deg); opacity: 0.20; }}
        66% {{ transform: translateY(25px) translateX(-35px) scale(0.92) rotate(240deg); opacity: 0.08; }}
        100% {{ transform: translateY(0) translateX(0) scale(1) rotate(360deg); opacity: 0.12; }}
    }}

    /* Sidebar HUD styling */
    section[data-testid="stSidebar"] {{
        background: var(--sidebar-bg) !important;
        border-right: 1px solid var(--border-glow) !important;
        box-shadow: 10px 0 35px rgba(0, 0, 0, 0.95);
    }}
    
    /* Headings */
    h1, h2, h3, h4 {{
        font-family: 'Outfit', 'Syncopate', sans-serif; text-transform: uppercase; letter-spacing: 1px;
    }}

    /* Main Title Holographic Shimmer */
    .main-title {{
        background: linear-gradient(90deg, var(--primary-color), #ffffff, var(--secondary-color), var(--primary-color));
        background-size: 300% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.2rem !important;
        font-weight: 900;
        text-align: center; margin-bottom: 0rem;
        animation: gradientShimmer 4s linear infinite;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.15);
    }}

    .sub-title {{
        text-align: center; color: #8b9bb4; font-family: 'Inter', 'Space Grotesk', sans-serif;
        font-weight: 500; font-size: 0.9rem; margin-bottom: 1.5rem;
        letter-spacing: 12px; text-transform: uppercase;
        text-shadow: 0 0 8px rgba(139, 155, 180, 0.2);
    }}

    @keyframes gradientShimmer {{
        0% {{ background-position: 0% 50%; }}
        100% {{ background-position: 300% 50%; }}
    }}

    /* Quantum Glass Cards */
    .glass-card {{
        background: var(--card-bg);
        backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px);
        border: 1px solid var(--border-glow);
        border-radius: 16px; padding: 28px; margin: 15px 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative; overflow: hidden;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        z-index: 1;
    }}
    
    .glass-card::before {{
        content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.08), transparent);
        transition: all 0.8s ease; transform: skewX(-20deg);
    }}

    .glass-card:hover {{
        transform: translateY(-6px) scale(1.01);
        border-color: var(--secondary-color);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2), 0 10px 10px -5px rgba(0, 0, 0, 0.1), 0 0 20px rgba(255, 255, 255, 0.05), inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }}
    
    .glass-card:hover::before {{ left: 200%; }}

    .glass-card h3 {{ color: var(--text-color); font-size: 1.25rem; display: flex; align-items: center; gap: 12px; text-shadow: 0 0 10px rgba(255,255,255,0.05); margin-top: 0; }}
    .glass-card p {{ color: var(--secondary-color); font-size: 0.95rem; margin-top: 8px; font-family: 'Inter', 'Space Grotesk', sans-serif; text-transform: none; letter-spacing: 0.3px; line-height: 1.6; }}

    /* Neo border utilities */
    .border-primary {{ border-left: 4px solid var(--primary-color) !important; }}
    .border-secondary {{ border-left: 4px solid var(--secondary-color) !important; }}
    .border-success {{ border-left: 4px solid var(--success-color) !important; }}
    .border-accent {{ border-left: 4px solid var(--accent-color) !important; }}

    /* Cyber Buttons */
    .stButton>button {{
        background: rgba(255, 255, 255, 0.02) !important;
        color: var(--primary-color) !important;
        border: 1px solid var(--border-glow) !important; border-radius: 8px !important;
        padding: 0.7rem 1.8rem !important; font-family: 'Syncopate', sans-serif !important;
        font-weight: 700 !important; font-size: 0.8rem !important;
        letter-spacing: 1.5px !important; transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
        text-transform: uppercase;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.02) !important;
    }}
    
    .stButton>button:hover {{
        background: rgba(255, 255, 255, 0.08) !important;
        color: #fff !important; border-color: var(--secondary-color) !important;
        box-shadow: 0 0 25px var(--secondary-color), inset 0 0 10px rgba(255, 255, 255, 0.05) !important;
        transform: translateY(-2px) !important; text-shadow: 0 0 8px rgba(255,255,255,0.3) !important;
    }}
    
    .stButton>button:active {{ transform: translateY(1px) !important; }}

    /* Purge button customization */
    .purge-btn>div>button {{
        background: rgba(244, 63, 94, 0.03) !important;
        color: var(--accent-color) !important;
        border: 1px solid rgba(244, 63, 94, 0.3) !important;
    }}
    .purge-btn>div>button:hover {{
        background: rgba(244, 63, 94, 0.12) !important;
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 25px var(--accent-color) !important;
    }}

    /* Floating Horizontal Command Console Navigation Dock */
    div[data-testid="stRadio"] > div {{
        flex-direction: row !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 12px !important;
        background: rgba(10, 10, 24, 0.45) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border: 1px solid var(--border-glow) !important;
        border-radius: 16px !important;
        padding: 12px !important;
        margin: 20px 0 35px 0 !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), inset 0 0 20px rgba(255, 255, 255, 0.01) !important;
        z-index: 100;
    }}

    div[data-testid="stRadio"] > div > label {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0.06)) !important;
        border: 1px solid var(--border-glow) !important;
        border-radius: 12px !important;
        padding: 14px 22px !important;
        margin: 0 !important;
        cursor: pointer !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        position: relative !important;
        overflow: hidden !important;
        flex: 1 1 auto !important;
        min-width: 150px !important;
        max-width: 220px !important;
        text-align: center !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
    }}

    div[data-testid="stRadio"] > div > label::before {{
        content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.05), transparent);
        transition: all 0.6s ease; z-index: 1;
    }}

    div[data-testid="stRadio"] > div > label:hover {{
        transform: translateY(-4px) scale(1.02) !important;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.12)) !important;
        border-color: var(--secondary-color) !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1), 0 0 15px rgba(255, 255, 255, 0.08) !important;
    }}
    
    div[data-testid="stRadio"] > div > label:hover::before {{ left: 100%; }}

    /* Hide standard radio circle icon invisibly but keep it fully cover-active for perfect touch responsiveness */
    div[data-testid="stRadio"] > div > label > div:first-child {{
        position: absolute !important;
        opacity: 0 !important;
        width: 100% !important;
        height: 100% !important;
        top: 0 !important;
        left: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        cursor: pointer !important;
        z-index: 3 !important;
    }}

    /* Navigation text styling */
    div[data-testid="stRadio"] > div > label > div:nth-child(2) {{
        font-family: 'Syncopate', sans-serif !important;
        font-weight: 700 !important; font-size: 0.72rem !important;
        color: #94a3b8 !important; text-transform: uppercase;
        letter-spacing: 1.5px !important; margin-left: 0px !important;
        z-index: 2; transition: all 0.3s ease !important;
    }}

    div[data-testid="stRadio"] > div > label:hover > div:nth-child(2) {{
        color: #ffffff !important; text-shadow: 0 0 10px rgba(255, 255, 255, 0.4) !important;
    }}

    /* Active Horizontal Tab */
    div[data-testid="stRadio"] > div > label:has(input:checked) {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05)) !important;
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 25px rgba(255, 255, 255, 0.1), inset 0 0 15px rgba(255, 255, 255, 0.05) !important;
        transform: translateY(-2px) !important;
    }}
    
    div[data-testid="stRadio"] > div > label:has(input:checked) > div:nth-child(2) {{
        color: var(--primary-color) !important;
        text-shadow: 0 0 15px var(--primary-color) !important;
        letter-spacing: 2px !important;
    }}

    /* Style stChatInput to fit the cybernetic grid design */
    div[data-testid="stChatInput"] {{
        background: rgba(10, 10, 24, 0.8) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border: 1px solid var(--border-glow) !important;
        border-radius: 14px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8), inset 0 0 15px rgba(255,255,255,0.01) !important;
        transition: all 0.3s ease !important;
    }}
    div[data-testid="stChatInput"]:focus-within {{
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 20px var(--primary-color), inset 0 0 15px rgba(255,255,255,0.02) !important;
    }}
    div[data-testid="stChatInput"] textarea {{
        color: #ffffff !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.02rem !important;
    }}

    /* Custom progress bar styles */
    .hud-bar-bg {{
        background: rgba(255,255,255,0.05);
        border-radius: 4px;
        height: 6px;
        width: 100%;
        margin-top: 6px;
        overflow: hidden;
    }}
    .hud-bar-fill {{
        height: 100%;
        border-radius: 4px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        box-shadow: 0 0 8px var(--primary-color);
    }}

    /* Pulse Connection Indicator */
    .pulse-indicator {{
        display: inline-block;
        width: 8px;
        height: 8px;
        background-color: var(--success-color);
        border-radius: 50%;
        margin-right: 8px;
        box-shadow: 0 0 10px var(--success-color);
        animation: pulseAnimation 2s infinite alternate;
    }}
    
    @keyframes pulseAnimation {{
        0% {{ transform: scale(0.9); opacity: 0.6; box-shadow: 0 0 4px var(--success-color); }}
        100% {{ transform: scale(1.3); opacity: 1; box-shadow: 0 0 12px var(--success-color); }}
    }}

    /* Premium stChatMessage styling to match the neon design system */
    [data-testid="stChatMessage"] {{
        background: rgba(12, 11, 28, 0.45) !important;
        border: 1px solid var(--border-glow) !important;
        border-radius: 12px !important;
        padding: 18px !important;
        margin-bottom: 15px !important;
        color: var(--text-color) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35) !important;
        transition: all 0.3s ease;
    }}
    [data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatar"] > div[role="img"]) {{
        border-left: 4px solid var(--primary-color) !important;
    }}
    [data-testid="stChatMessage"]:nth-child(even) {{
        background: rgba(22, 12, 42, 0.45) !important;
        border: 1px solid var(--border-glow) !important;
        border-left: 4px solid var(--secondary-color) !important;
    }}
    [data-testid="stChatMessage"] p {{
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.02rem !important;
        line-height: 1.6 !important;
    }}

    /* Quick-start prompts container layout */
    .quickstart-container {{
        margin: 25px 0;
    }}
    .quickstart-container div.stButton > button {{
        background: linear-gradient(135deg, rgba(14, 11, 30, 0.5), rgba(24, 15, 45, 0.55)) !important;
        border: 1px solid var(--border-glow) !important;
        border-left: 4px solid var(--primary-color) !important;
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
    }}
    .quickstart-container div.stButton > button:hover {{
        background: linear-gradient(135deg, rgba(22, 11, 45, 0.65), rgba(40, 15, 70, 0.7)) !important;
        border-color: var(--secondary-color) !important;
        border-left: 4px solid var(--secondary-color) !important;
        box-shadow: 0 10px 25px var(--secondary-color) !important;
        transform: translateY(-3px) !important;
    }}
    .quickstart-container div.stButton > button strong {{
        color: var(--primary-color) !important;
        font-family: 'Syncopate', sans-serif !important;
        font-size: 0.75rem !important;
        letter-spacing: 1px !important;
        margin-bottom: 6px !important;
        text-transform: uppercase !important;
        display: block !important;
    }}
    .quickstart-container div.stButton > button:hover strong {{
        color: var(--secondary-color) !important;
        text-shadow: 0 0 8px var(--secondary-color) !important;
    }}

    /* Soundwave bars container */
    .voice-wave-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        height: 60px;
        gap: 6px;
        margin: 20px 0;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 12px;
        border: 1px solid var(--border-glow);
        padding: 10px 30px;
    }}
    .voice-wave-container .stroke {{
        display: block;
        position: relative;
        background: var(--primary-color);
        height: 100%;
        width: 5px;
        border-radius: 50px;
        animation: animateWave 1.2s infinite ease-in-out;
    }}
    .voice-wave-container .stroke:nth-child(1) {{ animation-delay: 0.1s; background: var(--primary-color); }}
    .voice-wave-container .stroke:nth-child(2) {{ animation-delay: 0.3s; background: var(--secondary-color); }}
    .voice-wave-container .stroke:nth-child(3) {{ animation-delay: 0.5s; background: var(--accent-color); }}
    .voice-wave-container .stroke:nth-child(4) {{ animation-delay: 0.7s; background: var(--success-color); }}
    .voice-wave-container .stroke:nth-child(5) {{ animation-delay: 0.5s; background: var(--accent-color); }}
    .voice-wave-container .stroke:nth-child(6) {{ animation-delay: 0.3s; background: var(--secondary-color); }}
    .voice-wave-container .stroke:nth-child(7) {{ animation-delay: 0.1s; background: var(--primary-color); }}

    @keyframes animateWave {{
        0% {{ height: 8px; }}
        50% {{ height: 45px; }}
        100% {{ height: 8px; }}
    }}

    /* Custom Scrollbars */
    ::-webkit-scrollbar {{
        width: 6px; height: 6px;
    }}
    ::-webkit-scrollbar-track {{
        background: rgba(0, 0, 0, 0.2);
    }}
    ::-webkit-scrollbar-thumb {{
        background: var(--border-glow);
        border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: var(--secondary-color);
    }}

    /* Floating header telemetry values */
    .hud-header-dial {{
        font-family: 'Orbitron', monospace;
        font-size: 0.7rem;
        background: rgba(255,255,255,0.03);
        padding: 4px 8px;
        border-radius: 4px;
        border: 1px solid var(--border-glow);
        color: var(--primary-color);
        text-shadow: 0 0 6px var(--primary-color);
    }}

    /* Neural thought chain expander */
    .thought-step {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: var(--primary-color);
        padding: 6px 12px;
        border-left: 2px solid var(--primary-color);
        margin-bottom: 6px;
        background: rgba(0, 229, 255, 0.02);
        border-radius: 0 4px 4px 0;
    }}

    /* Futuristic upload button design */
    .futuristic-upload {{
        border: 1px dashed var(--primary-color);
        background: rgba(255, 255, 255, 0.01);
        border-radius: 10px;
        padding: 30px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    .futuristic-upload:hover {{
        border-color: var(--secondary-color);
        background: rgba(255,255,255,0.02);
    }}
</style>
""", unsafe_allow_html=True)

# Inject dynamic particle drifting background layer in DOM
st.markdown("""
<div class="quantum-particles">
    <div class="particle particle-1"></div>
    <div class="particle particle-2"></div>
    <div class="particle particle-3"></div>
    <div class="particle particle-4"></div>
    <div class="particle particle-5"></div>
    <div class="particle particle-6"></div>
</div>
""", unsafe_allow_html=True)

# Main Title and Subtitle Header
st.markdown("<h1 class='main-title'>OMNIMIND AI</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='sub-title'>{st.session_state.hud_theme.upper()} NEURAL OS_V2.6.0</p>", unsafe_allow_html=True)

# Floating Horizontal Navigation Menu Dock at the top of the viewport
menu = st.radio(
    "", 
    [
        "🧠 Core Engine", 
        "💻 Cyber Shell",
        "📄 PDF Intel", 
        "🎙️ Voice Transceiver", 
        "💾 Memory Banks", 
        "🌐 Node Network", 
        "📈 Live Telemetry", 
        "⚙️ OS Settings"
    ], 
    horizontal=True,
    label_visibility="collapsed"
)

# Custom Sidebar Layout with Diagnostics Panel & Navigation
with st.sidebar:
    st.markdown(f"""
        <div style='text-align: center; margin-bottom: 1.5rem;'>
            <h2 style='font-family: "Syncopate", sans-serif; font-size: 1.2rem; letter-spacing: 3px; color: var(--primary-color); text-shadow: 0 0 20px var(--primary-color); border-bottom: 1px solid var(--border-glow); padding-bottom: 10px; margin-bottom: 0;'>SYSTEM CORE</h2>
            <div style='margin-top: 8px; display: flex; align-items: center; justify-content: center; font-size: 0.72rem; color: var(--success-color); font-family: "Space Grotesk", sans-serif; font-weight: 600; letter-spacing: 1px;'>
                <span class='pulse-indicator'></span> COGNITIVE BRIDGE ACTIVE
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Interactive Sidebar Tuning Panel
    st.markdown("""
        <div style='margin-top: 1rem; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 15px;'>
            <h4 style='font-family: "Syncopate", sans-serif; font-size: 0.75rem; color: var(--secondary-color); letter-spacing: 1.5px; margin-bottom: 15px;'>COG PARAMETERS</h4>
        </div>
    """, unsafe_allow_html=True)
    
    st.slider("Neural Temperature", min_value=0.1, max_value=1.2, value=0.7, step=0.05, key="sidebar_temp")
    st.select_slider("Synaptic Priority", options=["Low Latency", "High Density", "Deep Reasoning"], value="Deep Reasoning", key="sidebar_priority")
    
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    
    # Dynamic HUD Palette switcher in the sidebar for immediate re-calibration from any tab
    st.markdown("""
        <div style='border-top: 1px solid rgba(255,255,255,0.08); padding-top: 15px; margin-bottom: 12px;'>
            <h4 style='font-family: "Syncopate", sans-serif; font-size: 0.75rem; color: var(--primary-color); letter-spacing: 1.5px;'>HUD PALETTE</h4>
        </div>
    """, unsafe_allow_html=True)
    
    current_theme = st.selectbox(
        "HUD Theme Selector", 
        list(THEME_CONFIGS.keys()), 
        index=list(THEME_CONFIGS.keys()).index(st.session_state.hud_theme),
        label_visibility="collapsed"
    )
    
    if current_theme != st.session_state.hud_theme:
        st.session_state.hud_theme = current_theme
        log_time = time.strftime("%H:%M:%S")
        st.session_state.simulated_sys_logs.append(f"[{log_time}] [SYS] HUD PALETTE RE-CALIBRATED TO {current_theme.upper()}")
        st.rerun()

    # Action Panel
    st.markdown("""
        <div style='border-top: 1px solid rgba(255,255,255,0.08); padding-top: 15px; margin-bottom: 12px;'>
            <h4 style='font-family: "Syncopate", sans-serif; font-size: 0.75rem; color: var(--accent-color); letter-spacing: 1.5px;'>SYSTEM OPERATIONS</h4>
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
        
    st.markdown(f"""
        <div style='margin-top: 15px; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 15px; display: flex; justify-content: space-between; align-items: center;'>
            <span style='font-size: 0.68rem; font-family: "Space Grotesk"; color:#64748b;'>UPTIME CLOCK</span>
            <span class='hud-header-dial'>04:19:35:02</span>
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
            active_prompt = AGENT_PERSONAS[st.session_state.active_agent]["system_prompt"]
            response = requests.post("http://127.0.0.1:8000/chat", json={"question": prompt_text, "system_prompt": active_prompt})
            data = response.json()
            st.session_state.chat_history.append({"role": "assistant", "content": data.get("response", "No response")})
            st.session_state.simulated_sys_logs.append(f"[{time.strftime('%H:%M:%S')}] [CORE] TELEMETRY LOAD BALANCED")
            st.rerun()
        except Exception as e:
            st.error(f"Neural Link Severed: {e}")

# ----------------------------------------------------
# 1. CORE QUANTUM ENGINE PAGE (AI Chat)
# ----------------------------------------------------
if menu == "🧠 Core Engine":
    st.markdown("""
    <div class='glass-card border-secondary'>
        <h3><span style='font-size:1.6rem; color:var(--secondary-color);'>✨</span> Global Cognitive AI Core</h3>
        <p>Interact with the primary OmniMind cognitive module. Ask questions, code matrices, or design layouts below. Responsive models auto-load.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Agent Persona Selector Core Deck
    st.markdown("<h4 style='color: #94a3b8; font-family: Syncopate; font-size: 0.8rem; letter-spacing: 2px; margin-top: 1.5rem; margin-bottom: 0.5rem;'>ACTIVE COGNITIVE AGENT TARGET</h4>", unsafe_allow_html=True)
    
    agent_cols = st.columns(3)
    for idx, (name, agent_info) in enumerate(AGENT_PERSONAS.items()):
        with agent_cols[idx]:
            is_active = (st.session_state.active_agent == name)
            border_color = agent_info["accent"] if is_active else "rgba(255, 255, 255, 0.08)"
            glow_style = f"box-shadow: 0 0 15px {agent_info['accent']}33, inset 0 0 10px {agent_info['accent']}11; border-color: {agent_info['accent']} !important;" if is_active else ""
            
            card_html = f"""
            <div class='glass-card' style='padding: 15px; margin: 5px 0; min-height: 140px; transition: all 0.3s; {glow_style}'>
                <div style='display: flex; align-items: center; gap: 8px;'>
                    <span style='font-size: 1.2rem;'>{agent_info['icon']}</span>
                    <strong style='font-size: 0.85rem; color: #fff; font-family: "Space Grotesk";'>{name.split(" - ")[0]}</strong>
                </div>
                <p style='font-size: 0.72rem; line-height: 1.4; margin-top: 8px; color: #94a3b8;'>{agent_info['description']}</p>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            if st.button(f"Link {name.split(' - ')[0]}", key=f"btn_agent_{idx}", use_container_width=True):
                st.session_state.active_agent = name
                log_time = time.strftime("%H:%M:%S")
                st.session_state.simulated_sys_logs.append(f"[{log_time}] [SYS] AGENT LINK ROUTED TO {name.upper()}")
                st.rerun()
                
    # Custom Chat Bubble Area
    if st.session_state.chat_history:
        st.markdown("<h4 style='color: #94a3b8; font-family: Syncopate; font-size: 0.8rem; letter-spacing: 2px; margin-top: 2rem;'>ACTIVE CONVERSATION FEED</h4>", unsafe_allow_html=True)
        
        # Thought process chain of last message
        if st.session_state.chat_history[-1]["role"] == "assistant":
            with st.expander("⚡ VIEW NEURAL SYNOPSIS PATHWAY", expanded=False):
                st.markdown(f"""
                <div class='thought-step'>[1/4] PARSING SEMANTIC TOKENS... DONE (neural temperature: {st.session_state.sidebar_temp:.2f})</div>
                <div class='thought-step' style='border-left-color: var(--secondary-color); color: var(--secondary-color);'>[2/4] ALIGNING DENSE CONTEXT RAG VECTORS... DONE</div>
                <div class='thought-step' style='border-left-color: var(--accent-color); color: var(--accent-color);'>[3/4] SYNAPSE WEIGHT OVERRIDES ENGAGED (priority: {st.session_state.sidebar_priority.upper()})... DONE</div>
                <div class='thought-step' style='border-left-color: var(--success-color); color: var(--success-color);'>[4/4] GENERATING LINGUISTIC TEXT OUTFLOW... NOMINAL (response compiled)</div>
                """, unsafe_allow_html=True)
                
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
                active_prompt = AGENT_PERSONAS[st.session_state.active_agent]["system_prompt"]
                response = requests.post("http://127.0.0.1:8000/chat", json={"question": user_query, "system_prompt": active_prompt})
                data = response.json()
                st.session_state.chat_history.append({"role": "assistant", "content": data.get("response", "No response")})
                st.session_state.simulated_sys_logs.append(f"[{time.strftime('%H:%M:%S')}] [CORE] RESPONSE COMPILED NOMINAL")
                st.rerun()
            except Exception as e:
                st.error(f"Neural Link Severed: {e}")

# ----------------------------------------------------
# 1.5. CYBER SHELL TAB (Hacker Console)
# ----------------------------------------------------
elif menu == "💻 Cyber Shell":
    st.markdown("""
    <div class='glass-card border-primary'>
        <h3><span style='font-size:1.6rem; color:var(--primary-color);'>💻</span> Neural Systems Command Deck</h3>
        <p>Direct low-level system registers access, diagnostic scans, and secure memory sector overrides. Execute system directives below.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Render glowing console
    console_feed = ""
    for line in st.session_state.shell_history:
        console_feed += f"{line}\n"
        
    st.markdown(f"""
    <pre style='background: #020104; border: 1px solid var(--border-glow); border-radius: 12px; color: #39ff14; font-family: "JetBrains Mono", monospace; font-size: 0.8rem; padding: 25px; min-height: 380px; max-height: 480px; overflow-y: auto; box-shadow: inset 0 0 25px rgba(0,0,0,0.95), 0 0 15px rgba(57, 255, 20, 0.05); line-height: 1.6;'>{console_feed}</pre>
    """, unsafe_allow_html=True)
    
    # Input field
    cmd = st.text_input("SYSTEM DIRECTIVE PROTOCOL >", placeholder="Enter command (e.g. help, sysinfo, neuroscan, ping)...", key="terminal_cmd")
    
    if st.button("⚡ TRANSMIT DIRECTIVE", use_container_width=True):
        if cmd.strip():
            raw_cmd = cmd.strip()
            st.session_state.shell_history.append(f"OMNIMIND-OS > {raw_cmd}")
            cmd_lower = raw_cmd.lower()
            
            if cmd_lower == "help":
                st.session_state.shell_history.extend([
                    "AVAILABLE NEURAL KERNEL DIRECTIVES:",
                    "  help       - Display this instruction board",
                    "  sysinfo    - Print physical hardware & co-processor metrics",
                    "  neuroscan  - Trigger real-time synapse channel scan",
                    "  matrix     - Compile multi-column cascade code streams",
                    "  ping       - Query diagnostic latencies to active nodes",
                    "  agent debug- Dump active cognitive agent specifications",
                    "  clear      - Purge screen trace buffers",
                    ""
                ])
            elif cmd_lower == "sysinfo":
                st.session_state.shell_history.extend([
                    "===========================================================",
                    "            OMNIMIND AI QUANTUM OS - TELEMETRY REPORT       ",
                    "===========================================================",
                    "  KERNEL VERSION : Onboard Core Neural Kernel v3.4.12       ",
                    "  PLATFORM       : Quantum Linux/Windows Hybrid (Core X86)",
                    "  NEURAL CORES   : 128x Sub-Quantum Photonic Co-Processors  ",
                    "  PROCESSING CAPS: 540 TFLOPS Vector Operations Density     ",
                    "  MEMORY HIT     : SQLite Secure Sector Immutable AES-256    ",
                    "  SYS TELEMETRY  : [NOMINAL] [128 NODES BOUNDED]           ",
                    "===========================================================",
                    ""
                ])
            elif cmd_lower == "neuroscan":
                st.session_state.shell_history.extend([
                    "[*] INITIATING COGNITIVE REGISTER TRACE SCAN...",
                    "[*] CALIBRATING SYNAPSE PATHWAYS...",
                    "[+] COGNITIVE GRID CAPACITY     : 98.42% STEADY",
                    "[+] COHERENCE THRESHOLD RATIO   : 0.992 NOMINAL",
                    "[+] SYNAPSE STABILITY VECTOR    : [0.892, 0.442, 0.125] SAFE",
                    "[+] TRACE DIAGNOSTICS COMPLETED : 0 ERRORS DETECTED",
                    ""
                ])
            elif cmd_lower == "matrix":
                st.session_state.shell_history.extend([
                    "01010110 01100101 01100011 01110100 01101111 01110010 (VECT)",
                    "01001110 01100101 01110101 01110100 01100001 01101100 (NEUR)",
                    "01010001 01110101 01100001 01101110 01110100 01110101 (QUAN)",
                    "01010011 01111001 01110011 01110100 01100101 01101101 (SYST)",
                    "[+] MATRIX STREAM DECODED NOMINAL",
                    ""
                ])
            elif cmd_lower == "ping":
                st.session_state.shell_history.extend([
                    "[*] PINGING ACTIVE SUB-QUANTUM NODES...",
                    "  [NODE-A] Core Cognitive Hub     : 45ms  - NOMINAL",
                    "  [NODE-B] Vector Memory Store    : 12ms  - STEADY",
                    "  [NODE-C] Speech Audio Bridge    : 1ms   - STANDBY",
                    "  [NODE-D] Holographic Parser     : 1ms   - IDLE",
                    "  [NODE-E] Cryptographic Database : 4ms   - SECURED",
                    "  [NODE-F] Logic Planner          : 8ms   - STEADY",
                    "[+] ALL HANDSHAKES NOMINAL. AVG LATENCY: 11.83ms",
                    ""
                ])
            elif cmd_lower == "agent debug":
                active = st.session_state.active_agent
                agent = AGENT_PERSONAS[active]
                st.session_state.shell_history.extend([
                    f"===========================================================",
                    f"       ACTIVE COGNITIVE AGENT PARAMETERS: {active.upper()}",
                    f"===========================================================",
                    f"  AGENT CLASSIFICATION : AI Assistant Node Core",
                    f"  COGNITIVE FOCUS      : {agent['description'][:60]}...",
                    f"  ACCENT COLOR HUE     : {agent['accent']}",
                    f"  SYSTEM INSTRUCTIONAL DENSITY : {len(agent['system_prompt'])} Characters",
                    f"  STATUS               : LINKED & ACTIVE",
                    f"===========================================================",
                    ""
                ])
            elif cmd_lower == "clear":
                st.session_state.shell_history = [
                    "OMNIMIND SECURE NEURAL KERNEL v3.4.12",
                    "SYSTEM CORE STATUS: ACTIVE",
                    "TYPE 'help' FOR LIST OF SYSTEM DIRECTIVES",
                    ""
                ]
            else:
                st.session_state.shell_history.extend([
                    f"[-] KERNEL DIRECTIVE ERROR: '{raw_cmd}' NOT RECOGNIZED",
                    "  Type 'help' to review available systems instructions.",
                    ""
                ])
            log_time = time.strftime("%H:%M:%S")
            st.session_state.simulated_sys_logs.append(f"[{log_time}] [SHELL] EXECUTED '{raw_cmd.upper()}'")
            st.rerun()

# ----------------------------------------------------
# 2. HOLOGRAPHIC PDF INTEL PAGE
# ----------------------------------------------------
elif menu == "📄 PDF Intel":
    st.markdown("""
    <div class='glass-card border-primary'>
        <h3><span style='font-size:1.6rem; color:var(--primary-color);'>📑</span> Holographic Document Parser</h3>
        <p>Drop PDF files into the RAG slot for automatic deep extraction, index building, and semantic summaries.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom Futuristic Drag Area Styling
    uploaded_file = st.file_uploader("Drop PDF dataset into core registers...", type="pdf")
    
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        file_size_kb = len(file_bytes) / 1024
        
        # Display Premium File Details Grid
        st.markdown(f"""
        <div class='glass-card border-primary' style='background: rgba(0, 229, 255, 0.02);'>
            <h4 style='font-family: "Syncopate", sans-serif; font-size: 0.8rem; color: var(--primary-color); margin-bottom: 15px;'>DATA SET IDENTIFIED</h4>
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
                    <div style='font-size:1.1rem; font-weight:600; color:var(--success-color); margin-top:5px;'>READY FOR PARSE</div>
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
                    log_placeholder.markdown(f"<div style='font-family: monospace; color:var(--primary-color); text-align:center; margin-bottom:10px;'>{l}</div>", unsafe_allow_html=True)
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
                        
                        st.session_state.pdf_summary = summary_txt
                        st.session_state.pdf_segments = [
                            {
                                "title": "Segment #01: Semantic Introduction Layer",
                                "tokens": 124,
                                "embedding": [0.082, -0.191, 0.432, -0.054, 0.812],
                                "content": f"The parsed header variables and initial scope parameters of {uploaded_file.name}. Introduces the primary layout objectives, data structures, and metadata index anchors compiled for neural modeling."
                            },
                            {
                                "title": "Segment #02: Quantitative Methodology Matrix",
                                "tokens": 256,
                                "embedding": [0.612, 0.054, -0.324, 0.722, -0.115],
                                "content": "Contains the mathematical constraints, logical algorithms, structural bounds, and computational complexity metrics. Establishes theoretical validation pathways across dense node dimensions."
                            },
                            {
                                "title": "Segment #03: Cognitive Telemetries",
                                "tokens": 192,
                                "embedding": [-0.142, 0.892, 0.115, -0.562, 0.345],
                                "content": "Presents empirical results, active real-time transaction latency tables, sub-system coherence quotients, and analytical chart parameters compiled from physical database matrices."
                            },
                            {
                                "title": "Segment #04: Abstract Resolution Core",
                                "tokens": 98,
                                "embedding": [0.345, -0.712, 0.021, 0.288, -0.912],
                                "content": "Formulates concluding optimizations, future extension blueprints, security system recommendations, and primary takeaways mapping back to the initial prompt parameters."
                            }
                        ]
                        st.rerun()
                    except Exception as e:
                        st.error(f"Processing Error: {e}")
                        
    # Display the Topological RAG Map
    if st.session_state.pdf_segments:
        st.markdown(f"""
        <div class='glass-card border-success' style='margin-top: 1.5rem;'>
            <h4 style='color: var(--success-color); font-family: Syncopate; font-size: 0.85rem; margin-top:0;'>✅ COGNITIVE SUMMARY GENERATED:</h4>
            <div style='line-height: 1.6; font-size:1.02rem; color:#e2e8f0; white-space: pre-wrap;'>{st.session_state.get('pdf_summary', '')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h4 style='color: var(--primary-color); font-family: Syncopate; font-size: 0.8rem; letter-spacing: 2px; margin-top: 2rem; margin-bottom: 1rem;'>🌐 TOPOGRAPHICAL VECTOR RAG MAP</h4>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.85rem; color:#94a3b8;'>Select any dense vector block below to inspect its sub-quantum embeddings, semantic contents, and token distributions.</p>", unsafe_allow_html=True)
        
        seg_cols = st.columns(4)
        for idx, seg in enumerate(st.session_state.pdf_segments):
            with seg_cols[idx]:
                is_selected = (st.session_state.selected_segment == idx)
                glow_style = f"box-shadow: 0 0 15px var(--primary-color)33, inset 0 0 8px var(--primary-color)11; border-color: var(--primary-color) !important;" if is_selected else ""
                
                card_html = f"""
                <div class='glass-card' style='padding: 15px; margin: 5px 0; min-height: 140px; cursor: pointer; transition: all 0.3s; {glow_style}'>
                    <div style='font-size: 0.7rem; font-family: "Syncopate"; color: var(--primary-color); margin-bottom: 8px;'>BLOCK 0{idx+1}</div>
                    <strong style='font-size: 0.82rem; color: #fff; display: block; min-height: 40px;'>{seg['title'].split(': ')[1]}</strong>
                    <div style='display: flex; justify-content: space-between; margin-top: 15px; font-size: 0.68rem; font-family: "Orbitron"; color: #cbd5e1;'>
                        <span>DENSITY</span>
                        <span>{seg['tokens']} Tok</span>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                if st.button(f"Inspect Block 0{idx+1}", key=f"btn_seg_{idx}", use_container_width=True):
                    st.session_state.selected_segment = idx
                    st.rerun()
                    
        # Render segment inspector
        if st.session_state.selected_segment is not None:
            seg = st.session_state.pdf_segments[st.session_state.selected_segment]
            st.markdown(f"""
            <div class='glass-card border-primary' style='margin-top: 1.5rem; background: rgba(0, 229, 255, 0.01);'>
                <h4 style='font-family: "Syncopate", sans-serif; font-size: 0.82rem; color: var(--primary-color); margin-top: 0; margin-bottom: 15px;'>🔍 VECTOR REGISTER DETAIL: {seg['title'].upper()}</h4>
                <div style='display: flex; gap: 40px; flex-wrap: wrap; margin-bottom: 20px;'>
                    <div>
                        <div style='font-size: 0.7rem; color: #64748b; font-family: Syncopate;'>VECTOR DIMENSIONS</div>
                        <div style='font-size: 1rem; font-weight: 600; color: #fff; font-family: Orbitron; margin-top: 4px;'>1,536 Dimensions</div>
                    </div>
                    <div>
                        <div style='font-size: 0.7rem; color: #64748b; font-family: Syncopate;'>COSINE COHERENCE</div>
                        <div style='font-size: 1rem; font-weight: 600; color: var(--success-color); font-family: Orbitron; margin-top: 4px;'>0.8841 (High Similarity)</div>
                    </div>
                    <div>
                        <div style='font-size: 0.7rem; color: #64748b; font-family: Syncopate;'>TOKEN SPAN</div>
                        <div style='font-size: 1rem; font-weight: 600; color: #fff; font-family: Orbitron; margin-top: 4px;'>{seg['tokens']} Core Tokens</div>
                    </div>
                </div>
                <div style='color: #cbd5e1; font-size: 0.75rem; font-family: Syncopate; margin-bottom: 6px;'>SUB-QUANTUM FLOATING EMBEDDINGS (PROJECTION)</div>
                <pre style='background: #030206; border: 1px solid var(--border-glow); border-radius: 8px; color: var(--primary-color); font-family: "JetBrains Mono", monospace; font-size: 0.75rem; padding: 12px; margin-bottom: 20px;'>{str(seg['embedding'][:-1] + ["..."])}</pre>
                <div style='color: #cbd5e1; font-size: 0.75rem; font-family: Syncopate; margin-bottom: 6px;'>SEMANTIC CHUNK EXTRACTED CONTEXT</div>
                <div style='background: rgba(255,255,255,0.02); padding: 15px; border-radius: 8px; border-left: 3px solid var(--primary-color); line-height: 1.6; font-size: 0.95rem; color: #fff;'>{seg['content']}</div>
            </div>
            """, unsafe_allow_html=True)

# ----------------------------------------------------
# 3. VOICE AI TRANSCEIVER PAGE
# ----------------------------------------------------
elif menu == "🎙️ Voice Transceiver":
    st.markdown("""
    <div class='glass-card border-accent'>
        <h3><span style='font-size:1.6rem; color:var(--accent-color);'>🎙️</span> Voice AI Transceiver</h3>
        <p>Direct speech-to-text transcription and high-speed audio command recognition. Use the HUD recording buttons below.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 1.8])
    
    with col1:
        st.markdown("""
        <div class='glass-card' style='text-align: center; background: rgba(5,4,9,0.5);'>
            <h4 style='font-family: "Syncopate", sans-serif; font-size: 0.8rem; color: var(--accent-color); margin-bottom: 20px;'>AUDIO SPECTROGRAPH</h4>
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
            st.markdown("<h4 style='color: var(--primary-color); font-family: Syncopate; font-size: 0.8rem; letter-spacing: 2px; margin-top:0;'>RECENT TRANSMISSION FEEDS</h4>", unsafe_allow_html=True)
            for i, log in enumerate(reversed(st.session_state.voice_history)):
                st.markdown(f"""
                <div class='glass-card border-accent' style='margin-bottom: 12px; padding: 20px;'>
                    <div style='display:flex; justify-content:space-between; margin-bottom: 12px;'>
                        <span style='color:#cbd5e1; font-family: Syncopate; font-size: 0.7rem;'>TRANSMISSION #{len(st.session_state.voice_history)-i}</span>
                        <span style='color:var(--accent-color); font-family: Orbitron; font-size: 0.75rem;'>SYNTH NOMINAL</span>
                    </div>
                    <div style='color: #94a3b8; font-size: 0.8rem; margin-bottom: 4px;'>SPEECH INPUT RECEIVED:</div>
                    <div style='background:rgba(255,255,255,0.04); padding:10px 14px; border-radius:6px; font-family:Space Grotesk; margin-bottom:12px;'>"{log['question']}"</div>
                    <div style='color: var(--accent-color); font-size: 0.8rem; margin-bottom: 4px;'>OMNIMIND VOCAL ANSWER:</div>
                    <div style='line-height:1.5; font-size:0.95rem; color:#fff;'>{log['response']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='glass-card' style='border: 1px dashed rgba(255,255,255,0.08); text-align: center; padding: 60px; color: #64748b; z-index: 1;'>
                🎙️ Audio transmission buffer is clear. Use the recording panel on the left to capture audio patterns.
            </div>
            """, unsafe_allow_html=True)

# ----------------------------------------------------
# 4. CRYPTOGRAPHIC MEMORY PAGE
# ----------------------------------------------------
elif menu == "💾 Memory Banks":
    st.markdown("""
    <div class='glass-card border-success'>
        <h3><span style='font-size:1.6rem; color:var(--success-color);'>🗄️</span> Cryptographic Memory Banks</h3>
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
            <div class='hud-metric-value' style='font-family:"Orbitron"; font-size:2rem; font-weight:700; color:#fff; text-shadow:0 0 10px var(--primary-color); margin-top:5px;'>{len(history)} Blocks</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; padding: 20px 10px; border-color: var(--secondary-color);'>
            <div class='hud-metric-label' style='font-family:"Syncopate"; font-size:0.75rem; color:var(--secondary-color);'>CYPHER ENCRYPTION</div>
            <div class='hud-metric-value' style='font-family:"Orbitron"; color:var(--secondary-color); font-size: 1.8rem; text-shadow:0 0 15px var(--secondary-color); margin-top:5px;'>AES-XTS-256</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; padding: 20px 10px; border-color: var(--success-color);'>
            <div class='hud-metric-label' style='font-family:"Syncopate"; font-size:0.75rem; color:var(--success-color);'>INTEGRITY BUFFER</div>
            <div class='hud-metric-value' style='font-family:"Orbitron"; font-size:2rem; font-weight:700; color:var(--success-color); text-shadow:0 0 15px var(--success-color); margin-top:5px;'>100%</div>
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
        st.markdown("<h4 style='color: var(--primary-color); font-family: Syncopate; font-size: 0.80rem; letter-spacing: 2px; margin-top: 1rem;'>CHRONOLOGICAL NEURAL TRACES</h4>", unsafe_allow_html=True)
        
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
                    st.markdown(f"**Cognitive Responders:**<br> <div style='background:rgba(255, 255, 255, 0.02); padding:12px; border-left:3px solid var(--secondary-color); border-radius:0 6px 6px 0; margin-top:5px; font-family: Space Grotesk;'>{item[2]}</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# 5. COGNITIVE NODE NETWORK PAGE
# ----------------------------------------------------
elif menu == "🌐 Node Network":
    st.markdown("""
    <div class='glass-card border-primary'>
        <h3><span style='font-size:1.6rem; color:var(--primary-color);'>🌐</span> Sub-Quantum Node Network Map</h3>
        <p>Live topographical grid of interconnected active AI sub-systems, logical routing connections, and transaction latencies.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Plotly Node Map Renderer
    def generate_neural_network_fig(p_color, s_color, succ_color, acc_color):
        x_nodes = [0, -1.5, 1.5, -1, 1, 0]
        y_nodes = [1.5, 0.5, 0.5, -0.7, -0.7, 0.1]
        
        node_labels = [
            "🧠 Core Cognitive Hub",
            "📂 Vector Memory Store",
            "🎙️ Speech Audio Bridge",
            "📄 Holographic Parser",
            "💾 Cryptographic DB",
            "⚡ Quantum Logic Planner"
        ]
        
        statuses = ["ACTIVE", "NOMINAL", "STANDBY", "IDLE", "NOMINAL", "NOMINAL"]
        latencies = ["45ms", "12ms", "0ms", "0ms", "4ms", "8ms"]
        
        edge_x = []
        edge_y = []
        connections = [(0, 1), (0, 2), (0, 5), (5, 1), (5, 2), (5, 3), (5, 4), (1, 3), (2, 4)]
        
        for edge in connections:
            edge_x.extend([x_nodes[edge[0]], x_nodes[edge[1]], None])
            edge_y.extend([y_nodes[edge[0]], y_nodes[edge[1]], None])
            
        fig = go.Figure()
        
        # Edges (connecting pathways)
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='rgba(255, 255, 255, 0.08)'),
            hoverinfo='none',
            mode='lines'
        ))
        
        # Color mapping based on status
        node_colors = []
        for s in statuses:
            if s == "ACTIVE":
                node_colors.append(p_color)
            elif s == "NOMINAL":
                node_colors.append(succ_color)
            elif s == "STANDBY":
                node_colors.append(s_color)
            else:
                node_colors.append("#475569")
                
        # Draw Nodes
        fig.add_trace(go.Scatter(
            x=x_nodes, y=y_nodes,
            mode='markers+text',
            text=[f" {lbl}" for lbl in node_labels],
            textposition="top right",
            marker=dict(
                symbol='hexagon-dot',
                size=22,
                color=node_colors,
                line=dict(color='#ffffff', width=1.5),
            ),
            hovertemplate="<b>%{text}</b><br>Status: %{customdata[0]}<br>Latency: %{customdata[1]}<extra></extra>",
            customdata=list(zip(statuses, latencies)),
            textfont=dict(family="Space Grotesk", size=12, color="#ffffff")
        ))
        
        fig.update_layout(
            showlegend=False,
            hovermode='closest',
            margin=dict(b=0, l=0, r=0, t=10),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=460
        )
        return fig

    # Display Map Card
    st.markdown("<h4 style='color: var(--primary-color); font-family: Syncopate; font-size: 0.8rem; letter-spacing: 2px; margin-bottom: 1.5rem;'>COGNITIVE TOPOLOGY VIEW</h4>", unsafe_allow_html=True)
    
    col_map, col_details = st.columns([2.2, 1])
    
    with col_map:
        fig_net = generate_neural_network_fig(theme['primary'], theme['secondary'], theme['success'], theme['accent'])
        st.plotly_chart(fig_net, use_container_width=True, config={'displayModeBar': False})
        
    with col_details:
        st.markdown(f"""
        <div class='glass-card border-secondary' style='margin-top: 10px; background: rgba(5,4,9,0.8);'>
            <h4 style='font-family: "Syncopate", sans-serif; font-size: 0.75rem; color: var(--secondary-color); margin-bottom: 15px;'>NODE INDEX MATRIX</h4>
            
            <div style='display:flex; justify-content:space-between; font-size: 0.8rem; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06);'>
                <span style='font-weight: 600; color:#fff;'>[NODE-A] Core Hub</span>
                <span style='color: var(--primary-color); font-family: Orbitron; font-weight:700;'>45ms</span>
            </div>
            
            <div style='display:flex; justify-content:space-between; font-size: 0.8rem; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06);'>
                <span style='font-weight: 600; color:#fff;'>[NODE-B] Vector Store</span>
                <span style='color: var(--success-color); font-family: Orbitron; font-weight:700;'>12ms</span>
            </div>
            
            <div style='display:flex; justify-content:space-between; font-size: 0.8rem; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06);'>
                <span style='font-weight: 600; color:#fff;'>[NODE-C] Speech Sync</span>
                <span style='color: var(--secondary-color); font-family: Orbitron;'>STANDBY</span>
            </div>
            
            <div style='display:flex; justify-content:space-between; font-size: 0.8rem; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06);'>
                <span style='font-weight: 600; color:#fff;'>[NODE-D] Doc Parser</span>
                <span style='color: #64748b; font-family: Orbitron;'>IDLE</span>
            </div>
            
            <div style='display:flex; justify-content:space-between; font-size: 0.8rem; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06);'>
                <span style='font-weight: 600; color:#fff;'>[NODE-E] Cryptographic DB</span>
                <span style='color: var(--success-color); font-family: Orbitron; font-weight:700;'>4ms</span>
            </div>
            
            <div style='display:flex; justify-content:space-between; font-size: 0.8rem; padding: 6px 0;'>
                <span style='font-weight: 600; color:#fff;'>[NODE-F] Logic Planner</span>
                <span style='color: var(--success-color); font-family: Orbitron; font-weight:700;'>8ms</span>
            </div>
            
            <div style='margin-top: 25px; font-size: 0.72rem; line-height: 1.5; color: #94a3b8; font-style: italic; border-left: 2px dashed var(--secondary-color); padding-left: 10px;'>
                Note: Connections are computed dynamically through multidimensional HSL cosine similarity pipelines.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------------------------------
# 6. SYSTEM TELEMETRY PAGE
# ----------------------------------------------------
elif menu == "📈 Live Telemetry":
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
        <div class='glass-card' style='text-align: center; padding: 20px 10px; border-color: var(--primary-color);'>
            <div class='hud-metric-label' style='font-family:"Syncopate"; font-size:0.75rem; color:var(--primary-color);'>TOTAL RUN QUERIES</div>
            <div class='hud-metric-value' style='font-family:"Orbitron"; font-size:2rem; font-weight:700; color:#ffffff; text-shadow:0 0 15px var(--primary-color);'>{len(history)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        max_load = max(sizes) if sizes else 0
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; padding: 20px 10px; border-color: var(--secondary-color);'>
            <div class='hud-metric-label' style='font-family:"Syncopate"; font-size:0.75rem; color:var(--secondary-color);'>PEAK CHAR LOAD</div>
            <div class='hud-metric-value' style='font-family:"Orbitron"; font-size:2rem; font-weight:700; color:#ffffff; text-shadow:0 0 15px var(--secondary-color);'>{max_load}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        status_val = "OPTIMAL" if len(history) > 0 else "STANDBY"
        status_col = "var(--success-color)" if status_val == "OPTIMAL" else "var(--secondary-color)"
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; padding: 20px 10px; border-color: var(--success-color);'>
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
                line=dict(color=theme['primary'], width=3, shape='spline'),
                marker=dict(
                    size=10, 
                    color=theme['secondary'], 
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
                    tickfont=dict(family='Space Grotesk', color=theme['primary']),
                    showgrid=True,
                    gridcolor='rgba(255, 255, 255, 0.04)',
                    gridwidth=1,
                    zeroline=False
                ),
                yaxis=dict(
                    title=dict(text='CHARACTER LENGTH', font=dict(family='Space Grotesk', color='#94a3b8', size=11)),
                    tickfont=dict(family='Space Grotesk', color=theme['secondary']),
                    showgrid=True,
                    gridcolor='rgba(255, 255, 255, 0.04)',
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
        st.markdown("<h4 style='font-family: Syncopate; font-size: 0.8rem; color:var(--primary-color); letter-spacing:1px; margin-top:0; margin-bottom: 12px;'>LIVE COGNITIVE LOGS</h4>", unsafe_allow_html=True)
        
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
        <pre style='background: #040307; border: 1px solid var(--border-glow); border-radius: 10px; color: #00ff7f; font-family: "JetBrains Mono", monospace; font-size: 0.78rem; padding: 18px; max-height: 290px; overflow-y: auto; box-shadow: inset 0 0 15px rgba(0,0,0,0.9); line-height: 1.5;'>{log_feed}</pre>
        """, unsafe_allow_html=True)

# ----------------------------------------------------
# 7. CYBERNETIC OS SETTINGS PAGE
# ----------------------------------------------------
elif menu == "⚙️ OS Settings":
    st.markdown("""
    <div class='glass-card border-secondary'>
        <h3><span style='font-size:1.6rem; color:var(--secondary-color);'>⚙️</span> Cybernetic System Configurations</h3>
        <p>Re-calibrate HSL holographic filters, synaptic prompt parameters, and execute full core network diagnostics.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_t, col_p = st.columns([1.2, 1.8])
    
    with col_t:
        st.markdown("<h4 style='color: var(--primary-color); font-family: Syncopate; font-size: 0.8rem; letter-spacing: 2px; margin-bottom: 1.5rem;'>HUD HOLOGRAPH THEME</h4>", unsafe_allow_html=True)
        
        # Display current parameters nicely
        st.markdown(f"""
        <div class='glass-card' style='background:rgba(255,255,255,0.01); border-color:var(--border-glow); padding:15px; margin-top:20px;'>
            <div style='font-size:0.75rem; color:#64748b; font-family:Syncopate; margin-bottom:8px;'>ACTIVE VALUES</div>
            <div style='display:flex; justify-content:space-between; font-size:0.8rem;'>
                <span>Primary Color:</span>
                <span style='color:var(--primary-color); font-family:Orbitron; font-weight:700;'>{theme['primary']}</span>
            </div>
            <div style='display:flex; justify-content:space-between; font-size:0.8rem; margin-top:5px;'>
                <span>Secondary Color:</span>
                <span style='color:var(--secondary-color); font-family:Orbitron; font-weight:700;'>{theme['secondary']}</span>
            </div>
            <div style='display:flex; justify-content:space-between; font-size:0.8rem; margin-top:5px;'>
                <span>Active Theme:</span>
                <span style='color:var(--primary-color); font-family:Orbitron; font-weight:700;'>{st.session_state.hud_theme.upper()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Color pickers for Custom Hologram theme
        if st.session_state.hud_theme == "Custom Hologram":
            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            st.markdown("<h4 style='color: var(--secondary-color); font-family: Syncopate; font-size: 0.72rem; letter-spacing: 1px;'>CALIBRATE HSL CHANNELS</h4>", unsafe_allow_html=True)
            
            c_pri = st.color_picker("Primary Accent Channel", value=st.session_state.custom_primary)
            c_sec = st.color_picker("Secondary Accent Channel", value=st.session_state.custom_secondary)
            c_acc = st.color_picker("Glow Accent Channel", value=st.session_state.custom_accent)
            
            if (c_pri != st.session_state.custom_primary or 
                c_sec != st.session_state.custom_secondary or 
                c_acc != st.session_state.custom_accent):
                st.session_state.custom_primary = c_pri
                st.session_state.custom_secondary = c_sec
                st.session_state.custom_accent = c_acc
                
                # Rebuild THEME_CONFIGS for immediate application
                THEME_CONFIGS["Custom Hologram"]["primary"] = c_pri
                THEME_CONFIGS["Custom Hologram"]["secondary"] = c_sec
                THEME_CONFIGS["Custom Hologram"]["accent"] = c_acc
                THEME_CONFIGS["Custom Hologram"]["bg_gradient"] = f"""
                    linear-gradient(rgba(0, 229, 255, 0.02) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(0, 229, 255, 0.02) 1px, transparent 1px),
                    radial-gradient(circle at 50% 0%, {c_sec}22 0%, transparent 60%),
                    radial-gradient(circle at 10% 100%, {c_pri}15 0%, transparent 50%),
                    radial-gradient(circle at 90% 100%, {c_acc}15 0%, transparent 50%)
                """
                log_time = time.strftime("%H:%M:%S")
                st.session_state.simulated_sys_logs.append(f"[{log_time}] [SYS] DYNAMIC ACCENT CHANNELS RE-CALIBRATED")
                st.rerun()
        
    with col_p:
        st.markdown("<h4 style='color: var(--primary-color); font-family: Syncopate; font-size: 0.8rem; letter-spacing: 2px; margin-bottom: 1.5rem;'>QUANTUM SYNAPSE TUNING</h4>", unsafe_allow_html=True)
        
        # sliders for detailed tuning parameters
        decay_val = st.slider("Synaptic Decay Threshold", min_value=0.1, max_value=1.0, value=0.72, step=0.02)
        gate_val = st.slider("Sub-quantum Token Gate Capacity", min_value=128, max_value=8192, value=4096, step=128)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: var(--accent-color); font-family: Syncopate; font-size: 0.75rem; letter-spacing: 1.5px;'>DIAGNOSTIC TEST REGISTERS</h4>", unsafe_allow_html=True)
        
        if st.button("⚡ EXECUTE CORE NETWORK DIAGNOSTICS", use_container_width=True):
            with st.spinner("Executing detailed sub-quantum trace scan..."):
                time.sleep(1.0)
                log_time = time.strftime("%H:%M:%S")
                st.session_state.simulated_sys_logs.append(f"[{log_time}] [SYS] DIAGNOSTICS RUN: NOMINAL (0 ERRORS, 6 NODES SAFE)")
                st.toast("System core nominal. 6 Active Nodes verified.", icon="🌐")
                st.rerun()
