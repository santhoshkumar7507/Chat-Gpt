import subprocess
import os

# Using the correct Windows path for Ollama
ollama_path = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama.exe")

try:
    subprocess.Popen([
        ollama_path,
        "serve"
    ])
    print("Ollama Running successfully on Windows!")
except FileNotFoundError:
    print(f"Error: Could not find Ollama at {ollama_path}")
