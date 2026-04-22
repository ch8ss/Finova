from core.supabase_client import get_supabase
import streamlit as st
import tempfile
import os

@st.cache_resource(show_spinner=False)
def get_embeddings():
    from langchain_huggingface import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def load_document(file_path: str, file_type: str):
    if file_type == "pdf":
        from langchain_community.document_loaders import PyPDFLoader
        loader = PyPDFLoader(file_path)
    elif file_type == "csv":
        from langchain_community.document_loaders import CSVLoader
        loader = CSVLoader(file_path)
    elif file_type == "txt":
        from langchain_community.document_loaders import TextLoader
        loader = TextLoader(file_path)
    elif file_type in ["xlsx", "xls"]:
        import pandas as pd
        from langchain_community.document_loaders import CSVLoader
        df = pd.read_excel(file_path)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        try:
            df.to_csv(tmp.name, index=False)
            loader = CSVLoader(tmp.name)
            return loader.load()
        finally:
            os.unlink(tmp.name)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    return loader.load()


def store_documents(user_id: str, documents: list):
    """Chunk documents and store embeddings in Supabase."""
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    sb = get_supabase()
    embedder = get_embeddings()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(documents)

    # Delete existing embeddings for this user (fresh upload)
    sb.table("embeddings").delete().eq("user_id", user_id).execute()

    rows = []
    for chunk in chunks:
        embedding = embedder.embed_query(chunk.page_content)
        rows.append({
            "user_id": user_id,
            "content": chunk.page_content,
            "metadata": chunk.metadata,
            "embedding": embedding,
        })

    # Insert in batches of 50
    for i in range(0, len(rows), 50):
        sb.table("embeddings").insert(rows[i:i+50]).execute()


def load_from_url(url: str) -> list:
    """Download a CSV/XLSX/PDF URL (or Google Sheets share link) and return documents."""
    import re
    import requests

    url = url.strip()

    # Convert Google Sheets share URL → CSV export URL
    sheets_match = re.search(r'docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
    if sheets_match:
        sheet_id = sheets_match.group(1)
        gid_match = re.search(r'gid=(\d+)', url)
        gid = gid_match.group(1) if gid_match else '0'
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
        ext = "csv"
    else:
        ext = url.split("?")[0].split(".")[-1].lower()
        if ext not in ["csv", "xlsx", "xls", "pdf"]:
            ext = "csv"

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    try:
        return load_document(tmp_path, ext)
    finally:
        os.unlink(tmp_path)


def has_embeddings(user_id: str) -> bool:
    """Return True if this user has any stored embeddings."""
    try:
        sb = get_supabase()
        result = sb.table("embeddings").select("id").eq("user_id", user_id).limit(1).execute()
        return bool(result.data)
    except Exception:
        return False


def similarity_search(user_id: str, query: str, k: int = 6) -> list:
    """Search for similar chunks in Supabase for this user."""
    embedder = get_embeddings()
    sb = get_supabase()

    query_embedding = embedder.embed_query(query)

    result = sb.rpc("match_embeddings", {
        "query_embedding": query_embedding,
        "match_user_id": user_id,
        "match_count": k,
    }).execute()

    return [row["content"] for row in result.data] if result.data else []
