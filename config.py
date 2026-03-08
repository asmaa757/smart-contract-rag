# config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_DIR = os.path.join(BASE_DIR, "uploaded_files")
    CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")
    
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 100
    GEMINI_MODEL = "models/gemma-3-1b-it"
    TEMPERATURE = 0.3
    RETRIEVER_K = 5

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(CHROMA_DIR, exist_ok=True)

config = Config()
print("✅ Config loaded successfully")  
