from core.llm import get_llm
from core.memory import get_memory
from core.rag import load_document, store_documents, similarity_search
from core.database import save_message, save_document
from langchain_core.messages import HumanMessage, SystemMessage
import tempfile
import os

BUSINESS_CONTEXT = {
    "Retail": "retail and inventory management. Focus on margins, stock turnover, seasonal trends, and shrinkage.",
    "Restaurant / Cafe": "food & beverage operations. Focus on food cost percentage, labour cost, covers per day, and waste.",
    "Manufacturing": "manufacturing. Focus on cost of goods, production efficiency, raw material costs, and overhead.",
    "Tech": "technology businesses. Focus on MRR, churn, CAC, LTV, and burn rate.",
    "Healthcare": "healthcare. Focus on billing cycles, patient revenue, insurance reimbursements, and overhead.",
    "E-commerce": "e-commerce. Focus on AOV, return rates, CAC, fulfilment costs, and conversion.",
    "Construction": "construction. Focus on project margins, material costs, labour, and cash flow timing.",
    "Education": "education businesses. Focus on enrolment revenue, staff costs, and seasonal cash flow.",
    "Freelance": "freelance/consulting. Focus on utilisation rate, project profitability, and income smoothing.",
    "Finance / Consulting": "finance and consulting. Focus on retainer revenue, project margins, and client concentration risk.",
    "Services": "service businesses. Focus on labour efficiency, billable hours, and recurring revenue.",
    "Other": "small business. Focus on revenue, expenses, profit margins, and cash flow.",
}

def process_uploaded_files(uploaded_files, user_id: str = None):
    if not user_id:
        return
    all_docs = []
    for f in uploaded_files:
        ext = f.name.split(".")[-1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            tmp.write(f.read())
            tmp_path = tmp.name
        try:
            docs = load_document(tmp_path, ext)
            all_docs.extend(docs)
            save_document(user_id, f.name, ext)
        finally:
            os.unlink(tmp_path)

    if all_docs:
        store_documents(user_id, all_docs)

def ask(question: str, session_id: str, user_id: str = None, business_type: str = "Other"):
    llm = get_llm()
    memory = get_memory(session_id)

    # Retrieve relevant context from Supabase
    context = ""
    if user_id:
        try:
            chunks = similarity_search(user_id, question, k=6)
            if chunks:
                context = "\n\n".join(chunks)
        except Exception:
            pass

    # Build chat history string — last 16 messages (8 exchanges)
    history = ""
    for msg in memory.messages[-16:]:
        role = "User" if msg.type == "human" else "CFO"
        history += f"{role}: {msg.content}\n"

    # Build dynamic system prompt
    biz_context = BUSINESS_CONTEXT.get(business_type, BUSINESS_CONTEXT["Other"])
    system_prompt = f"""You are Finova, an expert AI Chief Financial Officer specialising in {biz_context}

Your rules:
- ONLY use numbers and data from the uploaded financial documents. Never invent or estimate figures.
- If no data has been uploaded, tell the user clearly and ask them to upload a file first.
- Always structure your answers clearly:
  1. The direct answer with the key number(s)
  2. A brief explanation (1-2 sentences)
  3. One actionable recommendation
- Use plain English. Avoid jargon. Be direct and concise.
- If asked about trends, compare periods explicitly (e.g. "March vs February").
- Flag any concerning patterns proactively (e.g. rising costs, low margins)."""

    if context:
        user_prompt = f"Financial data from uploaded documents:\n\n{context}\n\nQuestion: {question}"
    else:
        user_prompt = (
            f"The user asked: {question}\n\n"
            "No financial data has been uploaded yet. "
            "Politely tell them to upload a PDF, CSV, or Excel file from the sidebar so you can analyse it."
        )

    if history:
        user_prompt = f"Conversation so far:\n{history}\n\n{user_prompt}"

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ])
    reply = response.content

    # Save to memory
    memory.add_user_message(question)
    memory.add_ai_message(reply)

    # Persist to database
    if user_id:
        save_message(user_id, "user", question)
        save_message(user_id, "assistant", reply)

    return reply
