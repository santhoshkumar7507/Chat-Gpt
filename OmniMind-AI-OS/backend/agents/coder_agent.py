from backend.ai_engine import ask_ai

def generate_code(task):
    prompt = f"Generate production-level Python code.\n\nTask:\n{task}"
    return ask_ai(prompt)
