import streamlit as st
import requests

# Exact ChatGPT Layout Configuration
st.set_page_config(page_title="ChatGPT", page_icon="💬", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    /* CSS Reset for exact ChatGPT look */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        background-color: #212121 !important;
        color: #ececec !important;
    }
    
    /* Remove Streamlit specific elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main Background */
    .stApp {
        background-color: #212121 !important;
    }

    /* Container Spacing */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* Sidebar - Exact Dark Mode Color */
    section[data-testid="stSidebar"] {
        background-color: #171717 !important;
        border-right: none !important;
        width: 260px !important;
        padding-top: 10px !important;
    }
    
    /* Sidebar Text */
    .stSidebar p {
        color: #ececec !important;
    }

    /* Input area at bottom */
    div[data-testid="stChatInput"] {
        background-color: #212121 !important;
        border: none !important;
        padding: 10px 0 30px 0 !important;
    }
    
    div[data-testid="stChatInput"] > div {
        background-color: #2f2f2f !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 24px !important;
        padding: 4px 12px !important;
        max-width: 768px !important;
        margin: 0 auto !important;
        box-shadow: 0 0 15px rgba(0,0,0,0.1) !important;
    }
    
    div[data-testid="stChatInput"] textarea {
        color: #ececec !important;
        font-size: 1rem !important;
    }

    /* Chat Messages */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
        padding: 24px 0 !important;
        max-width: 768px !important;
        margin: 0 auto !important;
    }
    
    [data-testid="stChatMessageAvatar"] {
        border-radius: 4px !important;
        width: 28px !important;
        height: 28px !important;
    }

    /* Sidebar New Chat Button */
    .stButton>button {
        background-color: transparent !important;
        color: #ececec !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 14px !important;
        text-align: left !important;
        width: 100% !important;
        justify-content: flex-start !important;
        font-weight: 500 !important;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #2f2f2f !important;
    }
    
    /* Center Logo Text */
    .chatgpt-title {
        font-size: 2.2rem;
        font-weight: 600;
        color: #fff;
        text-align: center;
        margin-top: 25vh;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar Layout
with st.sidebar:
    if st.button("📝 New chat", use_container_width=True):
        st.session_state.chat_history = []
        try:
            requests.post("http://127.0.0.1:8000/clear_history")
        except:
            pass
        st.rerun()
        
    st.markdown("<div style='margin-top: 25px; color: #666; font-size: 0.75rem; font-weight: 600; padding-left: 14px; margin-bottom: 5px;'>Today</div>", unsafe_allow_html=True)
    if st.session_state.chat_history:
        st.button("Current Conversation", use_container_width=True)
        
    st.markdown("<div style='margin-top: auto; padding-top: 50vh;'></div>", unsafe_allow_html=True)
    
    # Optional settings in a clean expander
    with st.expander("⚙️ Settings", expanded=False):
        st.write("Connect to Local Ollama Model")

# Main Chat Area
if not st.session_state.chat_history:
    st.markdown("<div class='chatgpt-title'>ChatGPT</div>", unsafe_allow_html=True)
else:
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        avatar = "🧑" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

# Bottom Input
if user_input := st.chat_input("Message ChatGPT..."):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.rerun()

# Generation Block
if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
    user_msg = st.session_state.chat_history[-1]["content"]
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        message_placeholder.markdown("...")
        
        try:
            payload = {
                "question": user_msg, 
                "system_prompt": "You are ChatGPT, a large language model trained by OpenAI."
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
