# smart-contract-rag

📄 Smart Document Assistant (RAG System)

📌 Overview

AI-powered system that lets you upload documents and ask questions about their content using RAG (Retrieval-Augmented Generation).

---

🚀 Features

· Upload PDF, DOCX, TXT files
· Automatic document processing & chunking
· Semantic search via vector embeddings
· Intelligent QA using LLM
· Clean Gradio chat interface
· Shows source text used for answers

---

🧠 How It Works

Upload → Process → Chunk → Embed → Store (ChromaDB) → Ask → Retrieve → Generate → Answer + Source

---

📂 Project Structure

├── app.py           # Gradio UI
├── qa_pipeline.py   # QA logic (retrieval + generation)
├── ingestion.py     # Document processing & storage
├── config.py        # Settings (API keys, paths, models)
├── main.py          # Entry point
├── chroma_db/       # Vector database
└── uploaded_files/  # Uploaded documents
---

🔧 Tech Stack

· Python
· Gradio (UI)
· LangChain (RAG pipeline)
· Google Generative AI (Embeddings + LLM)
· ChromaDB (Vector store)
· Gemini Models

---

🤖 AI Models

· models/gemini-embedding-001 → Text to embeddings
· models/gemma-3-1b-it → Answer generation

---

👩‍💻 Author

Educational project for learning RAG systems and LLM applications.
