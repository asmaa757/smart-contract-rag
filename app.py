# app.py

import gradio as gr
import os
import shutil
from config import Config
from ingestion import ingest_document
from qa_pipeline import ask_question

config = Config()
current_file = None

def upload_file(file):
    global current_file
    if not file:
        return "❌ Please select a file"
    
    try:
        file_name = os.path.basename(file.name)
        file_path = os.path.join(config.UPLOAD_DIR, file_name)
        shutil.copy(file.name, file_path)
        result = ingest_document(file_path)
        
        if result["status"] == "success":
            current_file = file_name
            return f"✅ File '{file_name}' uploaded!\n📄 {result['chunks']} chunks created."
        return f"❌ Error: {result['message']}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def respond(message, chat_history):
    if not message.strip():
        return "", chat_history

    if not current_file:
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": "⚠️ Please upload a file first"})
        return "", chat_history

    result = ask_question(message)
    answer = result["answer"]
    sources = result["sources"]
    full_response = f"{answer}\n\n"
    
    if sources:
        import re
        answer_words = set(re.findall(r'\b\w+\b', answer.lower()))
        scored_sources = []
        
        for src in sources:
            src_words = set(re.findall(r'\b\w+\b', src['text'].lower()))
            score = len(answer_words & src_words)
            scored_sources.append((score, src))
        
        scored_sources.sort(key=lambda x: x[0], reverse=True)
        full_response += "📄 Sources:\n\n"
        for i, (_, src) in enumerate(scored_sources[:1]):
            full_response += f"{i+1}. {src['file']}\n{src['text'][:300]}...\n\n"
    
    chat_history.append({"role": "user", "content": message})
    chat_history.append({"role": "assistant", "content": full_response})
    return "", chat_history

with gr.Blocks(title="📄 Smart Assistant", theme=gr.themes.Soft(primary_hue="sky")) as demo:
    gr.Markdown(
        """
        <div style="text-align: center; margin-bottom: 10px;">
            <h1 style="color: #0284c7;">📄 Smart Document Assistant</h1>
            <p style="color: #475569;">Upload any document and ask questions. I'll think step by step.</p>
        </div>
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1, min_width=300):
            gr.Markdown("### 📎 Upload")
            file_input = gr.File(
                label="",
                file_types=[".pdf", ".docx", ".txt"],
                show_label=False
            )
            upload_btn = gr.Button("📤 Upload Document", variant="primary", size="lg")
            upload_output = gr.Textbox(label="Status", interactive=False)
        
        with gr.Column(scale=2):
            gr.Markdown("### 💬 Chat")
            chatbot = gr.Chatbot(label="", height=450, show_label=False)
            
            with gr.Row():
                msg = gr.Textbox(
                    label="",
                    placeholder="Ask anything... e.g. When will she graduate?",
                    lines=2,
                    scale=4,
                    show_label=False
                )
                send_btn = gr.Button("📤 Send", variant="primary", scale=1, size="lg")
            
            clear_btn = gr.Button("🧹 Clear Chat", variant="secondary", size="sm")
    
    upload_btn.click(upload_file, inputs=[file_input], outputs=[upload_output])
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    send_btn.click(respond, [msg, chatbot], [msg, chatbot])
    clear_btn.click(lambda: None, None, chatbot, queue=False)