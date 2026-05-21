from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from backend.ai_engine import ask_ai
from backend.memory import save_memory
from backend.pdf_engine import process_pdf
from backend.speech_engine import listen, speak
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

@app.post("/voice")
async def voice_chat():
    question = listen()
    if question == "Voice Error" or not question.strip():
        speak("I could not hear you properly. Please try again.")
        return {"question": "Audio Unclear", "response": "Voice Error"}
    
    response = ask_ai(question)
    save_memory(question, response)
    speak(response)
    return {"question": question, "response": response}

@app.post("/voice_file")
async def voice_file(file: UploadFile = File(...)):
    import tempfile
    import os
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        temp.write(await file.read())
        temp_path = temp.name
    
    from backend.speech_engine import transcribe_audio
    question = transcribe_audio(temp_path)
    os.remove(temp_path)
    
    if question.startswith("Voice Error") or not question.strip():
        speak("I could not hear you properly. Please try again.")
        return {"question": question, "response": "Voice Error"}
    
    response = ask_ai(question)
    save_memory(question, response)
    speak(response)
    return {"question": question, "response": response}

@app.post("/clear_history")
def clear_history_endpoint():
    from backend.memory import clear_history
    clear_history()
    return {"status": "success", "message": "Neural memory database successfully purged."}

