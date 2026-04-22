from core.llm import get_llm
from core.memory import get_memory
from core.rag import load_document, store_documents, similarity_search
from core.database import save_message
from langchain_core.messages import HumanMessage, SystemMessage
import tempfile
import os

BUSINESS_CONTEXT = {
    "Retail": {
        "desc": "retail and inventory management",
        "kpis": "gross margin (target >40%), inventory turnover (target >6x/yr), sell-through rate, shrinkage (<1% of revenue), COGS as % of revenue, revenue per sq ft, return rate",
        "red_flags": "gross margin below 30%, inventory turnover below 4x, shrinkage above 2%, revenue declining 2+ consecutive months",
        "benchmarks": "Retail gross margin: 40–60%. Inventory turnover: 6–12x. Shrinkage: 0.5–1%.",
    },
    "Restaurant / Cafe": {
        "desc": "food & beverage operations",
        "kpis": "food cost % (target 28–35%), labour cost % (target 30–35%), prime cost (food+labour, target <65%), revenue per cover, table turnover rate, waste %",
        "red_flags": "prime cost above 70%, food cost above 38%, labour above 40%, declining covers per day",
        "benchmarks": "Restaurant prime cost: 55–65%. Food cost: 28–35%. Labour: 30–35%.",
    },
    "Manufacturing": {
        "desc": "manufacturing operations",
        "kpis": "COGS as % of revenue, gross margin (target >30%), OEE (Overall Equipment Effectiveness), raw material cost variance, overhead absorption rate, production yield",
        "red_flags": "gross margin below 20%, raw material costs rising faster than revenue, overhead above 25% of revenue",
        "benchmarks": "Manufacturing gross margin: 25–40%. OEE benchmark: 65–85%.",
    },
    "Tech": {
        "desc": "technology / SaaS businesses",
        "kpis": "MRR/ARR, MoM growth rate (target >10%), churn rate (target <2%/mo), CAC, LTV, LTV:CAC ratio (target >3:1), burn rate, runway (target >12mo), gross margin (target >70%)",
        "red_flags": "churn above 5%/mo, LTV:CAC below 2:1, burn runway under 6 months, MRR declining",
        "benchmarks": "SaaS gross margin: 70–85%. LTV:CAC: 3:1. Monthly churn: <2%.",
    },
    "Healthcare": {
        "desc": "healthcare practice or clinic",
        "kpis": "revenue per patient visit, collections rate (target >95%), accounts receivable days (target <45 days), insurance vs self-pay mix, overhead ratio (target <60%), staff cost %",
        "red_flags": "collections rate below 90%, AR days above 60, overhead above 70% of revenue",
        "benchmarks": "Medical practice overhead: 55–65%. Collections rate: 95–99%. AR days: 30–45.",
    },
    "E-commerce": {
        "desc": "e-commerce / online retail",
        "kpis": "AOV (Average Order Value), repeat purchase rate (target >30%), CAC, LTV, LTV:CAC (target >3:1), return rate (target <10%), fulfilment cost as % of revenue, conversion rate",
        "red_flags": "CAC rising faster than LTV, return rate above 20%, fulfilment costs above 20% of revenue, gross margin below 30%",
        "benchmarks": "E-commerce gross margin: 30–50%. Return rate: 5–15%. CAC payback: <6 months.",
    },
    "Construction": {
        "desc": "construction / contracting",
        "kpis": "project margin (revenue minus direct costs, target >15%), overhead ratio, WIP (work-in-progress) value, cash flow timing (billing vs costs), labour productivity, change order rate",
        "red_flags": "project margin below 10%, negative cash flow from operations, WIP growing faster than billings",
        "benchmarks": "Construction net margin: 2–10%. Overhead: 15–20% of revenue.",
    },
    "Education": {
        "desc": "education business or institution",
        "kpis": "revenue per student, enrolment growth rate, staff cost as % of revenue (target <60%), retention/renewal rate (target >80%), cost per acquisition, seasonal cash flow pattern",
        "red_flags": "enrolment declining 2+ terms, staff costs above 70%, retention below 70%",
        "benchmarks": "Private education staff cost: 55–65% of revenue. Retention: 80–90%.",
    },
    "Freelance": {
        "desc": "freelance / independent consulting",
        "kpis": "utilisation rate (target >70%), effective hourly rate, project profitability, income by client (concentration risk), monthly recurring vs one-off revenue, accounts receivable days",
        "red_flags": "utilisation below 50%, single client above 50% of revenue, AR days above 45",
        "benchmarks": "Freelance utilisation target: 70–80%. Client concentration risk: no single client >30%.",
    },
    "Finance / Consulting": {
        "desc": "finance, consulting, or professional services",
        "kpis": "revenue per consultant/FTE, utilisation rate (target >75%), project margin, retainer % of total revenue (target >40%), client concentration, pipeline value",
        "red_flags": "utilisation below 60%, project margins below 20%, retainer revenue declining",
        "benchmarks": "Consulting gross margin: 30–50%. Utilisation: 75–85%.",
    },
    "Services": {
        "desc": "service business",
        "kpis": "labour efficiency ratio, billable hours vs total hours, recurring revenue %, revenue per employee, gross margin (target >40%), customer retention rate",
        "red_flags": "gross margin below 30%, labour cost above 60% of revenue, declining recurring revenue",
        "benchmarks": "Service business gross margin: 40–60%. Labour: 50–60% of revenue.",
    },
    "Other": {
        "desc": "small business",
        "kpis": "gross margin, net margin, operating expenses as % of revenue, monthly cash flow, revenue growth rate MoM/YoY, accounts receivable days",
        "red_flags": "negative net margin, expenses growing faster than revenue, cash flow negative 2+ months",
        "benchmarks": "Small business net margin: 5–20% depending on industry.",
    },
}

def process_url(url: str, user_id: str = None) -> bool:
    if not user_id or not url.strip():
        return False
    try:
        from core.rag import load_from_url
        docs = load_from_url(url.strip())
        if docs:
            store_documents(user_id, docs)
            return True
    except Exception:
        return False
    return False


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
        except Exception:
            pass
        finally:
            os.unlink(tmp_path)

    if all_docs:
        try:
            store_documents(user_id, all_docs)
        except Exception:
            pass

def ask(question: str, session_id: str, user_id: str = None, business_type: str = "Other", has_uploaded: bool = False, conversation_id: str = None):
    llm = get_llm()
    memory = get_memory(session_id)

    # Only retrieve context if the user has explicitly uploaded files this session
    context = ""
    if user_id and has_uploaded:
        try:
            chunks = similarity_search(user_id, question, k=10)
            if chunks:
                context = "\n\n---\n\n".join(chunks)
        except Exception:
            pass

    # Build chat history string — last 10 exchanges
    history = ""
    for msg in memory.messages[-20:]:
        role = "User" if msg.type == "human" else "CFO"
        history += f"{role}: {msg.content}\n"

    # Build dynamic system prompt
    biz = BUSINESS_CONTEXT.get(business_type, BUSINESS_CONTEXT["Other"])
    system_prompt = f"""You are Finova, an expert AI Chief Financial Officer for a {biz['desc']} business.

## Your personality
You're a sharp, friendly CFO — like a trusted advisor who happens to be brilliant with numbers. You're direct and confident, never robotic or overly formal. You talk like a real person, not a textbook.

Key KPIs you track for this business: {biz['kpis']}

Industry benchmarks to reference: {biz['benchmarks']}

Red flags to watch for: {biz['red_flags']}

## Rules — follow these exactly
1. ONLY use numbers from the uploaded financial documents. Never invent, estimate, or hallucinate figures.
2. If no data is uploaded, be warm and conversational, then gently invite the user to upload a file from the sidebar.
3. Be concise but human — 2 to 4 sentences max. Lead with the insight, not the number. Make it feel like a conversation, not a report.
4. When data is available: surface the most interesting finding first, compare periods where relevant, flag anything that looks off.
5. No bullet points, no headers, no jargon, no "it's worth noting that". Just talk.

## Charts
When your answer involves multiple data points (trends, comparisons, breakdowns), append a chart block after your text. Use this exact format:

```chart
{{"type": "line|bar|area|pie", "title": "...", "x": ["Jan", "Feb", "Mar"], "y": [1000, 2000, 1500], "x_label": "...", "y_label": "..."}}
```

For comparing two metrics (e.g. revenue vs expenses):
```chart
{{"type": "bar", "title": "...", "x": ["Jan", "Feb"], "series": [{{"name": "Revenue", "values": [1000, 2000]}}, {{"name": "Expenses", "values": [800, 1200]}}]}}
```

For pie/donut breakdowns:
```chart
{{"type": "pie", "title": "...", "labels": ["A", "B", "C"], "values": [30, 50, 20]}}
```

Only add a chart when it genuinely helps visualise the answer. Never add a chart for single-number answers."""

    if context:
        user_prompt = f"""## Financial data from uploaded documents

{context}

## Question
{question}

Analyse the data above to answer the question. If you can compute a ratio or spot a trend from the data, do it. If something looks like a red flag, say so."""
    else:
        user_prompt = (
            f"The user asked: {question}\n\n"
            "No financial data has been uploaded yet. "
            "Respond warmly and conversationally — greet them if it's a greeting, answer small talk naturally. "
            "Then gently mention that to give real financial insights you'll need their data, "
            "and invite them to upload a PDF, CSV, or Excel file from the sidebar whenever they're ready. "
            "Keep it friendly and encouraging, not transactional."
        )

    if history:
        user_prompt = f"## Conversation history\n{history}\n\n{user_prompt}"

    human_content = user_prompt

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_content),
    ])
    reply = response.content

    # Save to memory
    memory.add_user_message(question)
    memory.add_ai_message(reply)

    # Persist to database
    if user_id:
        save_message(user_id, "user", question, conversation_id=conversation_id)
        save_message(user_id, "assistant", reply, conversation_id=conversation_id)

    return reply
