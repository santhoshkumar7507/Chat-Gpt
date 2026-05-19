import ollama

SYSTEM_PROMPT = """
You are OmniMind AI.
You are an advanced offline AI Operating System.
Answer professionally.
"""

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
        return f"System Error - Engine offline or model not found: {e}"
