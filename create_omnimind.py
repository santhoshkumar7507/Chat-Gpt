import os

base_dir = r"d:\chat-gpt\OmniMind-AI-OS"

directories = [
    "backend/agents",
    "backend/database",
    "frontend/pages",
    "models/local_models",
    "uploads",
    "memory",
    "logs"
]

for d in directories:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

files = {
    "requirements.txt": "fastapi\nuvicorn\nstreamlit\nlangchain\nsqlalchemy\npytest\n",
    "backend/main.py": "from fastapi import FastAPI\nfrom fastapi.middleware.cors import CORSMiddleware\n\napp = FastAPI(title='OmniMind AI OS')\n\napp.add_middleware(\n    CORSMiddleware,\n    allow_origins=['*'],\n    allow_credentials=True,\n    allow_methods=['*'],\n    allow_headers=['*'],\n)\n\n@app.get('/')\ndef read_root():\n    return {'status': 'OmniMind AI OS Backend is running efficiently.'}\n",
    "backend/ai_engine.py": "class AIEngine:\n    pass\n",
    "backend/memory.py": "class MemoryManager:\n    pass\n",
    "backend/vector_store.py": "class VectorStore:\n    pass\n",
    "backend/speech_engine.py": "class SpeechEngine:\n    pass\n",
    "backend/pdf_engine.py": "class PDFEngine:\n    pass\n",
    "backend/image_engine.py": "class ImageEngine:\n    pass\n",
    "backend/agents/coder_agent.py": "class CoderAgent:\n    pass\n",
    "backend/agents/research_agent.py": "class ResearchAgent:\n    pass\n",
    "backend/agents/planner_agent.py": "class PlannerAgent:\n    pass\n",
    "backend/agents/automation_agent.py": "class AutomationAgent:\n    pass\n",
    "frontend/app.py": """import streamlit as st

st.set_page_config(page_title="OmniMind AI OS", page_icon="🧠", layout="wide")

st.markdown('''
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: white;
    }
    .stAppHeader {
        background-color: transparent !important;
    }
    .css-1d391kg {
        background-color: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(10px);
    }
    h1 {
        background: -webkit-linear-gradient(45deg, #60a5fa, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 24px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-5px);
    }
</style>
''', unsafe_allow_html=True)

st.title("🧠 OmniMind AI OS")

st.markdown("<div class='glass-card'><h3>Welcome to OmniMind</h3><p>The next-generation AI operating system is now online. Please select a module from the sidebar to begin orchestration.</p></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='glass-card'><h3>🤖 Agents</h3><p style='color:#4ade80;'>4/4 Active</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='glass-card'><h3>🧠 Memory</h3><p style='color:#60a5fa;'>Optimized & Synced</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='glass-card'><h3>⚡ Core</h3><p style='color:#c084fc;'>All Systems Nominal</p></div>", unsafe_allow_html=True)
""",
    "frontend/pages/dashboard.py": "import streamlit as st\nst.title('📊 Dashboard')\nst.write('System metrics will appear here.')\n",
    "frontend/pages/analytics.py": "import streamlit as st\nst.title('📈 Analytics')\nst.write('AI performance insights.')\n",
    "frontend/pages/settings.py": "import streamlit as st\nst.title('⚙️ Settings')\nst.write('Configure system parameters.')\n",
    "backend/database/sqlite.db": ""
}

for filepath, content in files.items():
    full_path = os.path.join(base_dir, filepath)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Scaffold complete!")
