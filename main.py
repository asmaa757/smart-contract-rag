# main.py

import os
import shutil
from app import demo
from config import Config

config = Config()

if os.path.exists(config.UPLOAD_DIR):
    for f in os.listdir(config.UPLOAD_DIR):
        os.remove(os.path.join(config.UPLOAD_DIR, f))

if os.path.exists(config.CHROMA_DIR):
    shutil.rmtree(config.CHROMA_DIR, ignore_errors=True)

os.makedirs(config.CHROMA_DIR, exist_ok=True)

print("✅ System ready...") 
demo.launch(debug=True)