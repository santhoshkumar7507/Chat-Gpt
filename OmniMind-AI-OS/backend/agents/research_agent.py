from backend.ai_engine import ask_ai

def research(topic):
    prompt = f"Explain deeply:\n\n{topic}"
    return ask_ai(prompt)
