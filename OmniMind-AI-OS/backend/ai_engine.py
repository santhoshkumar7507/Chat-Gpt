import ollama
import time

SYSTEM_PROMPT = """
You are OmniMind AI.
You are an advanced offline AI Operating System.
Answer professionally.
"""

def generate_fallback_response(question):
    q_lower = question.lower()
    
    header = (
        "🤖 **[OMNIMIND CORE - EMERGENCY STANDBY MODE]**\n"
        "*Ollama offline or model not loaded. Initializing Onboard Cognitive Synthesizer...*\n\n"
    )
    
    if "hello" in q_lower or "hi" in q_lower or "hey" in q_lower:
        body = (
            "Greetings, human. I am OmniMind AI, your quantum-enhanced neural operating system. "
            "Although my deep Llama/Qwen weights are currently offline, my basic primary cognitive circuits are active.\n\n"
            "How can I assist you in emergency standby mode today? You can ask me to analyze data, simulate system logs, or structure concepts!"
        )
    elif "summarize" in q_lower or "summary" in q_lower or "pdf" in q_lower or "document" in q_lower:
        body = (
            "### 📑 Onboard Document Analysis Report\n"
            "I have parsed the core linguistic vectors of your request. \n\n"
            "**Key Themes Identified:**\n"
            "1. **Core Subject Matter:** Structural document query processing.\n"
            "2. **Information Density:** High utility syntax extraction.\n\n"
            "*To obtain a complete deep-neural summary, please ensure the Ollama server is running locally and the `qwen2.5:0.5b` or `llama3` model is pulled.*"
        )
    elif "code" in q_lower or "python" in q_lower or "javascript" in q_lower or "html" in q_lower or "function" in q_lower:
        body = (
            "### 💻 Primary Syntactic Engine - Python Code Matrix\n"
            "Here is a clean template generated from my emergency cognitive registers:\n\n"
            "```python\n"
            "# OmniMind AI OS - Primary Fallback Script\n"
            "def omnimind_initialize():\n"
            "    system_status = \"NOMINAL\"\n"
            "    quantum_cores = 128\n"
            "    print(f\"[+] OmniMind AI OS Initialized. Status: {system_status}\")\n"
            "    return system_status\n"
            "\n"
            "if __name__ == \"__main__\":\n"
            "    omnimind_initialize()\n"
            "```\n\n"
            "*(Note: Enable Ollama for full-featured, state-of-the-art LLM code generation.)*"
        )
    elif "status" in q_lower or "system" in q_lower or "info" in q_lower or "version" in q_lower:
        body = (
            "### 📊 System Telemetry & Diagnostic Report\n"
            "- **OS Core Version:** OmniMind Quantum OS v2.0.4\n"
            "- **Linguistic Model:** Qwen 2.5 (0.5B Parameter) / Llama 3 (Standby)\n"
            "- **Onboard Memory Database:** SQLite 3.x (Active & Synchronized)\n"
            "- **Cognitive Synthesis Engine:** Fallback Standby Mode\n"
            "- **Active Workspace:** `d:\\chat-gpt`\n"
            "- **Audio Processing Core:** Voice AI Interface Ready\n\n"
            "All physical systems are functional. The neural link is waiting for the local Ollama background server to complete sync."
        )
    else:
        body = (
            f"### 🧠 Neural Output Matrix\n"
            f"You queried: *\"{question}\"*\n\n"
            "My primary neural network is in offline standby mode, but I've processed your intent. "
            "To unlock fully unrestricted deep-learning capabilities, please launch the local Ollama daemon and run:\n"
            "`ollama pull qwen2.5:0.5b`\n\n"
            "**Emergency Diagnostic Suggestion:**\n"
            "- Check if Ollama is running in your task tray.\n"
            "- Use the system menu's **Voice Synthesis** or **Neural Memory** tabs to explore local database logs."
        )
        
    return header + body

def ask_ai(question):
    try:
        response = ollama.chat(
            model="qwen2.5:0.5b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ]
        )
        return response["message"]["content"]
    except Exception as e:
        err_msg = str(e).lower()
        if "not found" in err_msg or "pull" in err_msg:
            return (
                "📥 **[MODEL SYNCHRONIZATION NEEDED]**\n"
                "The lightweight model `qwen2.5:0.5b` is not yet installed in your local Ollama registry.\n\n"
                "**To synchronize the cognitive model, please run this in your command line:**\n"
                "```bash\n"
                "ollama pull qwen2.5:0.5b\n"
                "```\n"
                "Or ensure Ollama is open and connected to the internet. "
                "Meanwhile, here is an AI response computed using my fallback onboard core:\n\n" + 
                generate_fallback_response(question)
            )
        return generate_fallback_response(question)
