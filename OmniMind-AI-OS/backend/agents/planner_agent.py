from backend.ai_engine import ask_ai

def create_plan(goal):
    prompt = f"Create a detailed execution roadmap.\n\nGoal:\n{goal}"
    return ask_ai(prompt)
