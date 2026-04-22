# Finova — AI Financial Advisor for Small Business

Finova is an AI-powered financial advisory platform built for small and medium-sized business owners. It acts as an on-demand CFO: upload your financial documents, ask questions in plain English, and get expert analysis, KPI tracking, and actionable insights tailored to your industry.

---

## Features

- **AI CFO Chat** — Conversational interface powered by Llama 3.3 70B via Groq for fast, expert-level financial responses
- **Document Analysis** — Upload PDF, CSV, or Excel files; the AI reads and reasons over your actual business data using RAG
- **Industry-Specific Insights** — Tailored analysis across 12 business types (Retail, Restaurant, Manufacturing, Tech, Healthcare, E-commerce, Construction, Education, Freelance, Finance/Consulting, Services, and more)
- **Red Flag Detection** — Proactively identifies financial warning signs specific to your business type
- **Interactive Charts** — Auto-generated Plotly visualizations (line, bar, area, pie) from conversation context
- **Persistent Memory** — Conversation history stored per user; sessions auto-restore across logins
- **Secure Auth** — Sign-up/sign-in via Supabase Auth with 7-day cookie-based auto-login

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Streamlit |
| LLM | Groq API — `llama-3.3-70b-versatile` |
| LLM Orchestration | LangChain |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Database & Auth | Supabase (Postgres + Auth + Vector search) |
| Charts | Plotly |
| File Parsing | PyPDF, Pandas, openpyxl |
| Session | streamlit-cookies-controller |

---

## Project Structure

```
business-ai-assistant/
├── app.py                  # Entry point — auth/login page
├── requirements.txt
├── .env                    # API keys (not committed)
│
├── core/
│   ├── auth.py             # Supabase sign-up / sign-in
│   ├── chain.py            # Core AI CFO logic & system prompts
│   ├── rag.py              # Document chunking, embedding, similarity search
│   ├── database.py         # Message persistence
│   ├── memory.py           # In-session chat history
│   ├── session.py          # Session restoration from user_id
│   ├── llm.py              # Groq LLM init
│   ├── supabase_client.py  # Supabase client
│   └── theme.py            # Dark/light theme CSS
│
└── pages/
    ├── 1_Chat.py           # Main CFO chat interface + file upload
    └── 2_Dashboard.py      # User dashboard & conversation history
```

---

## Getting Started

### Prerequisites

- Python 3.12
- A [Groq API key](https://console.groq.com)
- A [Supabase](https://supabase.com) project with the tables below

### Installation

```bash
git clone https://github.com/ch8ss/Finova.git
cd business-ai-assistant

python3.12 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
```

### Supabase Setup

Create the following tables in your Supabase project:

**users**
```sql
create table users (
  id uuid primary key references auth.users(id),
  email text,
  business_name text,
  business_type text,
  created_at timestamp default now()
);
```

**conversations**
```sql
create table conversations (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id),
  role text,
  content text,
  created_at timestamp default now()
);
```

**embeddings** (with pgvector for similarity search)
```sql
create extension if not exists vector;

create table embeddings (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id),
  content text,
  embedding vector(384),
  created_at timestamp default now()
);

create or replace function match_embeddings(
  query_embedding vector(384),
  match_user_id uuid,
  match_count int
)
returns table (content text, similarity float)
language sql stable
as $$
  select content, 1 - (embedding <=> query_embedding) as similarity
  from embeddings
  where user_id = match_user_id
  order by embedding <=> query_embedding
  limit match_count;
$$;
```

### Run

```bash
streamlit run app.py
```

The app starts at `http://localhost:8501`.

---

## How It Works

1. **Sign up** and select your business type
2. **Upload** your financial documents (PDF, CSV, or Excel)
3. **Chat** with your AI CFO — ask about revenue trends, expenses, cash flow, KPIs, or anything else
4. Finova retrieves relevant chunks from your documents (RAG), applies industry-specific context, and returns analysis with optional charts

Document chunks are embedded using HuggingFace and stored in Supabase with per-user scoping. Each query runs a vector similarity search to ground the LLM response in your actual data.

---

## Supported Business Types

Retail · Restaurant/Cafe · Manufacturing · Technology · Healthcare · E-commerce · Construction · Education · Freelance · Finance & Consulting · Services · Other

---

## License

MIT
