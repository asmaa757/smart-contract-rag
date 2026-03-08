# qa_pipeline.py

from config import Config
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma

config = Config()

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=config.GOOGLE_API_KEY,
    dimensions=768
)

vectorstore = Chroma(
    collection_name="contracts",
    embedding_function=embeddings,
    persist_directory=config.CHROMA_DIR
)

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": config.RETRIEVER_K}
)

llm = ChatGoogleGenerativeAI(
    model=config.GEMINI_MODEL,
    temperature=config.TEMPERATURE,
    google_api_key=config.GOOGLE_API_KEY
)

def retrieve_documents(question):
    return retriever.invoke(question)

def generate_smart_answer(question, context_docs):
    all_texts = []
    sources_with_text = []
    
    for doc in context_docs:
        all_texts.append(doc.page_content)
        sources_with_text.append({
            "file": doc.metadata.get('source', 'Unknown'),
            "text": doc.page_content.strip()
        })
    
    full_context = "\n\n".join(all_texts)
    
    smart_prompt = f"""
    You are a smart document analyst.

    RULES:
    1. Answer the question in a NATURAL, CONVERSATIONAL way
    2. DO NOT copy-paste from the document
    3. Combine information from different parts if needed
    4. Be accurate and complete
    5. The source will be shown separately

    CONTEXT:
    {full_context}

    QUESTION: {question}

    Answer:
    """
    
    response = llm.invoke(smart_prompt)
    answer = response.content

    return answer, sources_with_text

def ask_question(question):
    try:
        docs = retrieve_documents(question)
        
        if not docs:
            return {
                "question": question,
                "answer": "No relevant documents found.",
                "sources": [],
                "num_chunks": 0
            }
        
        answer, sources = generate_smart_answer(question, docs)
        
        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "num_chunks": len(docs)
        }
        
    except Exception as e:
        return {
            "question": question,
            "answer": f"Error: {str(e)}",
            "sources": [],
            "num_chunks": 0
        }

print("✅ QA pipeline ready")

