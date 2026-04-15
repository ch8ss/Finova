from langchain_community.document_loaders import PyPDFLoader, CSVLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from core.supabase_client import get_supabase
import streamlit as st
import pandas as pd
import tempfile
import os

@st.cache_resource(show_spinner=False)
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def load_document(file_path: str, file_type: str):
    if file_type == "pdf":
        loader = PyPDFLoader(file_path)
    elif file_type == "csv":
        loader = CSVLoader(file_path)
    elif file_type == "txt":
        loader = TextLoader(file_path)
    elif file_type in ["xlsx", "xls"]:
        df = pd.read_excel(file_path)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        df.to_csv(tmp.name, index=False)
        loader = CSVLoader(tmp.name)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    return loader.load()


def store_documents(user_id: str, documents: list):
    """Chunk documents and store embeddings in Supabase."""
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
