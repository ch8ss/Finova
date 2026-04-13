from core.llm import get_llm
from core.memory import get_memory
from core.rag import load_document, get_vectorstore
from core.database import save_message, save_document
from langchain_core.messages import HumanMessage, SystemMessage
import tempfile
import os

def process_uploaded_files(uploaded_files, user_id: str = None):
    all_docs = []
    for f in uploaded_files:
        ext = f.name.split(".")[-1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            tmp.write(f.read())
            tmp_path = tmp.name
        try:
            docs = load_document(tmp_path, ext)
            all_docs.extend(docs)
            if user_id:
                save_document(user_id, f.name, ext)
        finally:
            os.unlink(tmp_path)

    if all_docs:
        get_vectorstore(documents=all_docs)

def ask(question: str, session_id: str, user_id: str = None):
    llm = get_llm()
    memory = get_memory(session_id)

    # Retrieve relevant context from vectorstore
    context = ""
    try:
        vectorstore = get_vectorstore()
        results = vectorstore.similarity_search(question, k=3)
        if results:
            context = "\n\n".join([r.page_content for r in results])
    except Exception:
        pass

    # Build chat history string
    history = ""
    for msg in memory.messages[-10:]:  # last 10 messages for context
        role = "User" if msg.type == "human" else "CFO"
        history += f"{role}: {msg.content}\n"

    # Build prompt
    system_prompt = (
        "You are Finova, an expert AI Chief Financial Officer for small businesses. "
        "You ONLY answer based on financial data the user has uploaded. "
        "If no data has been uploaded yet, tell the user clearly that you need them to upload a financial document first — do NOT invent, estimate, or assume any numbers. "
        "When data is available, be concise, clear, and actionable. Use simple language — avoid jargon."
    )

    user_prompt = question
    if context:
        user_prompt = f"Based on the following uploaded financial data:\n\n{context}\n\nAnswer this question: {question}"
    else:
        user_prompt = (
            f"The user asked: {question}\n\n"
            "No financial data has been uploaded yet. "
            "Politely tell them to upload a file (PDF, CSV, or Excel) from the sidebar before you can answer."
        )
    if history:
        user_prompt = f"Previous conversation:\n{history}\n\n{user_prompt}"

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ])
    reply = response.content

    # Save to memory
    memory.add_user_message(question)
    memory.add_ai_message(reply)

    # Persist to database if user is logged in
    if user_id:
        save_message(user_id, "user", question)
        save_message(user_id, "assistant", reply)

    return reply
