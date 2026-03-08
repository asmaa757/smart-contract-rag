# ingestion.py

import os
from config import Config
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

config = Config()

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",p[]
    google_api_key=config.GOOGLE_API_KEY,
    dimensions=768 
)

vectorstore = Chroma(
    collection_name="contracts",
    embedding_function=embeddings,
    persist_directory=config.CHROMA_DIR
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=config.CHUNK_SIZE,
    chunk_overlap=config.CHUNK_OVERLAP
)

def load_and_split_document(file_path):
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith('.docx'):
        loader = Docx2txtLoader(file_path)
    elif file_path.endswith('.txt'):
        loader = TextLoader(file_path, encoding='utf-8')
    else:
        raise ValueError(f"File type not supported: {file_path}")

    documents = loader.load()
    chunks = text_splitter.split_documents(documents)
    
    for i, chunk in enumerate(chunks):
        chunk.metadata["source"] = os.path.basename(file_path)
        chunk.metadata["chunk_id"] = i
    
    return chunks

def ingest_document(file_path):
    try:
        chunks = load_and_split_document(file_path)
        vectorstore.add_documents(chunks)
        vectorstore.persist()
        
        return {
            "status": "success",
            "chunks": len(chunks),
            "file": os.path.basename(file_path)
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

print("✅ Ingestion complete")

