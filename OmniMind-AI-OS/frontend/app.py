import streamlit as st
import requests
import json
import base64
import os
from backend.memory import get_history

# Set page config for clean Chat-like layout
st.set_page_config(page_title="AI Chat", page_icon="💬", layout="centered")

# Custom CSS for a ChatGPT-like minimalist look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background-color: #343541; /* ChatGPT dark gray */
        color: #d1d5db;
    }

    /* Sidebar Background */
    section[data-testid="stSidebar"] {
        background-color: #202123 !important;
        border-right: none;
    }

    /* Input area at bottom */
    div[data-testid="stChatInput"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    div[data-testid="stChatInput"] > div {
        background-color: #40414f !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(0,0,0,0.1);
    }
    
    div[data-testid="stChatInput"] textarea {
        color: white !important;
    }

    /* Chat Messages */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 1.5rem 0 !important;
    }
    
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: transparent !important; /* User message */
    }
    
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #444654 !important; /* Assistant message */
        border-top: 1px solid rgba(0,0,0,0.1) !important;
        border-bottom: 1px solid rgba(0,0,0,0.1) !important;
    }

    /* Remove avatars border */
    [data-testid="stChatMessageAvatar"] {
        border-radius: 4px !important;
    }
    
    /* Buttons in sidebar */
    .stButton>button {
        background-color: #343541 !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        text-align: left !important;
        width: 100% !important;
        justify-content: flex-start !important;
        font-weight: 400 !important;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #2a2b32 !important;
        border-color: rgba(255,255,255,0.3) !important;
    }
    
    /* Hide top header and default padding */
    header {visibility: hidden;}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 10rem;
        max-width: 800px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "You are a helpful AI assistant."

# Sidebar Layout (ChatGPT Style)
with st.sidebar:
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.chat_history = []
        try:
            requests.post("http://127.0.0.1:8000/clear_history")
        except:
            pass
        st.rerun()
        
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("<div style='color: #8e8ea0; font-size: 0.8rem; margin-bottom: 10px;'>Tools</div>", unsafe_allow_html=True)
    
    # PDF Upload Tool
    uploaded_pdf = st.file_uploader("Upload PDF Document", type="pdf")
    if uploaded_pdf:
        if st.button("Extract Knowledge"):
            with st.spinner("Processing PDF..."):
                try:
                    files = {"file": (uploaded_pdf.name, uploaded_pdf, "application/pdf")}
                    res = requests.post("http://127.0.0.1:8000/upload_pdf", files=files)
                    st.success("PDF processed successfully. You can now ask questions about it.")
                except Exception as e:
                    st.error(f"Error processing PDF: {e}")
                    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='color: #8e8ea0; font-size: 0.8rem; margin-bottom: 10px;'>Agent Persona</div>", unsafe_allow_html=True)
    st.session_state.system_prompt = st.text_area("System Instructions", value=st.session_state.system_prompt, height=100)

# Main Chat Area
if not st.session_state.chat_history:
    st.markdown("""
    <div style='text-align: center; margin-top: 15vh;'>
        <h1 style='font-size: 2.5rem; color: white; font-weight: 600;'>ChatGPT</h1>
        <p style='color: #8e8ea0; font-size: 1.1rem; margin-top: 10px;'>How can I help you today?</p>
    </div>
    """, unsafe_allow_html=True)

# Display chat history
for msg in st.session_state.chat_history:
    # Use standard avatars instead of emojis for a cleaner look
    avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# Bottom Input
if user_input := st.chat_input("Message ChatGPT..."):
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(user_input)
        
    # Get Assistant Response
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        message_placeholder.markdown("...")
        
        try:
            payload = {
                "question": user_input, 
                "system_prompt": st.session_state.system_prompt
            }
            response = requests.post("http://127.0.0.1:8000/chat", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get("response", "No response received.")
                message_placeholder.markdown(reply)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
            else:
                message_placeholder.markdown(f"Error: {response.text}")
        except Exception as e:
            message_placeholder.markdown(f"Connection Error: {e}")
