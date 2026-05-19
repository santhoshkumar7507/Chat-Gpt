import os

base_dir = r"d:\chat-gpt\OmniMind-AI-OS"

files = {
    "backend/main.py": """from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from backend.ai_engine import ask_ai
from backend.memory import save_memory
from backend.pdf_engine import process_pdf
from pydantic import BaseModel

app = FastAPI(title="OmniMind AI OS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "OmniMind AI OS Running"}

@app.post("/chat")
async def chat(data: ChatRequest):
    question = data.question
    response = ask_ai(question)
    save_memory(question, response)
    return {"response": response}

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()
    result = process_pdf(content)
    return {"pdf_summary": result}
""",
    "backend/ai_engine.py": """import ollama

SYSTEM_PROMPT = \"\"\"
You are OmniMind AI.
You are an advanced offline AI Operating System.
Answer professionally.
\"\"\"

def ask_ai(question):
    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"System Error - Engine offline or model not found: {e}"
""",
    "backend/memory.py": """import sqlite3
import os
from datetime import datetime

os.makedirs("backend/database", exist_ok=True)
conn = sqlite3.connect("backend/database/sqlite.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute(\"\"\"
    CREATE TABLE IF NOT EXISTS memory(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT,
        created_at TEXT
    )
\"\"\")
conn.commit()

def save_memory(question, answer):
    cursor.execute(
        "INSERT INTO memory(question, answer, created_at) VALUES (?, ?, ?)",
        (question, answer, str(datetime.now()))
    )
    conn.commit()

def get_history():
    cursor.execute("SELECT * FROM memory ORDER BY id DESC")
    return cursor.fetchall()
""",
    "backend/pdf_engine.py": """from pypdf import PdfReader
import tempfile
import os
from backend.ai_engine import ask_ai

def process_pdf(pdf_content):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_content)
        tmp_path = tmp.name

    try:
        reader = PdfReader(tmp_path)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
                
        prompt = f"Summarize this document:\\n\\n{text[:5000]}"
        return ask_ai(prompt)
    finally:
        os.unlink(tmp_path)
""",
    "backend/vector_store.py": """import chromadb
import os

os.makedirs("memory", exist_ok=True)
client = chromadb.PersistentClient(path="./memory")
collection = client.get_or_create_collection(name="omnimind_memory")

def add_memory(text, uid):
    collection.add(documents=[text], ids=[uid])

def search_memory(query):
    results = collection.query(query_texts=[query], n_results=3)
    return results
""",
    "backend/speech_engine.py": """import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        return "Voice Error"
""",
    "backend/agents/coder_agent.py": """from backend.ai_engine import ask_ai

def generate_code(task):
    prompt = f"Generate production-level Python code.\\n\\nTask:\\n{task}"
    return ask_ai(prompt)
""",
    "backend/agents/research_agent.py": """from backend.ai_engine import ask_ai

def research(topic):
    prompt = f"Explain deeply:\\n\\n{topic}"
    return ask_ai(prompt)
""",
    "backend/agents/planner_agent.py": """from backend.ai_engine import ask_ai

def create_plan(goal):
    prompt = f"Create a detailed execution roadmap.\\n\\nGoal:\\n{goal}"
    return ask_ai(prompt)
""",
    "backend/image_engine.py": """from PIL import Image
import cv2

def analyze_image(path):
    image = cv2.imread(path)
    height, width, channels = image.shape
    return {
        "width": width,
        "height": height,
        "channels": channels
    }
""",
    "frontend/app.py": """import streamlit as st
import requests
from backend.memory import get_history
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="OmniMind AI OS", page_icon="🧠", layout="wide")

st.markdown(\"\"\"
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: white;
    }
    .stAppHeader { background-color: transparent !important; }
    .css-1d391kg { background-color: rgba(15, 23, 42, 0.6); backdrop-filter: blur(10px); }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 24px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        background: -webkit-linear-gradient(45deg, #60a5fa, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Inter', sans-serif;
    }
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
        color: white; border: none; border-radius: 8px;
        padding: 0.5rem 1rem; transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px); box-shadow: 0 4px 12px rgba(139, 92, 246, 0.5);
    }
</style>
\"\"\", unsafe_allow_html=True)

st.title("🧠 OmniMind AI Operating System")

menu = st.sidebar.radio("Navigation", ["AI Chat", "PDF AI", "Voice Assistant", "Memory", "Analytics"])

if menu == "AI Chat":
    st.markdown("<div class='glass-card'><h3>💬 Global AI Chat</h3><p>Engage with the OmniMind core engine powered by Llama 3.</p></div>", unsafe_allow_html=True)
    question = st.text_area("Ask Anything to the System...")
    if st.button("Generate Intelligence"):
        with st.spinner("Processing through neural pathways..."):
            try:
                response = requests.post("http://127.0.0.1:8000/chat", json={"question": question})
                data = response.json()
                st.markdown("<div class='glass-card'><h4>Response:</h4>" + str(data.get("response", "No response")) + "</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")

elif menu == "PDF AI":
    st.markdown("<div class='glass-card'><h3>📄 PDF Document Intelligence</h3><p>Upload a document for instantaneous summary.</p></div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        if st.button("Analyze PDF"):
            with st.spinner("Extracting insights..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                    response = requests.post("http://127.0.0.1:8000/upload_pdf", files=files)
                    st.markdown("<div class='glass-card'><h4>Summary:</h4>" + str(response.json().get("pdf_summary", "")) + "</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")

elif menu == "Voice Assistant":
    st.markdown("<div class='glass-card'><h3>🎙️ Voice AI Mode</h3><p>Speech synthesis and recognition module.</p></div>", unsafe_allow_html=True)
    st.info("Voice assistant functions are available in the backend engine.")

elif menu == "Memory":
    st.markdown("<div class='glass-card'><h3>💾 Immutable Memory Log</h3><p>Recent interactions stored in the AI OS.</p></div>", unsafe_allow_html=True)
    history = get_history()
    for item in history:
        with st.expander(f"Question: {item[1][:50]}..."):
            st.write(f"**Q:** {item[1]}")
            st.write(f"**A:** {item[2]}")
            st.caption(f"Time: {item[3]}")

elif menu == "Analytics":
    st.markdown("<div class='glass-card'><h3>📈 AI Analytics Dashboard</h3><p>Real-time metrics on AI processing.</p></div>", unsafe_allow_html=True)
    history = get_history()
    questions = [item[1] for item in history]
    sizes = [len(q) for q in questions]
    if sizes:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(sizes, marker='o', linestyle='-', color='#8b5cf6')
        ax.set_title('Query Length Over Time', color='white')
        ax.set_ylabel('Character Count', color='white')
        ax.set_xlabel('Interaction #', color='white')
        ax.tick_params(colors='white')
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)
        st.pyplot(fig)
    else:
        st.write("No interactions yet.")
"""
}

for filepath, content in files.items():
    full_path = os.path.join(base_dir, filepath)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Setup Complete")
