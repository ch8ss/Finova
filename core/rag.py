from langchain_community.document_loaders import PyPDFLoader, CSVLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import streamlit as st
import pandas as pd
import tempfile
import os

BASE_VECTORSTORE_PATH = "data/vectorstore"

@st.cache_resource(show_spinner=False)
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

def _user_path(user_id: str) -> str:
    path = os.path.join(BASE_VECTORSTORE_PATH, user_id)
    os.makedirs(path, exist_ok=True)
    return path

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

def get_vectorstore(user_id: str, documents=None):
    embeddings = get_embeddings()
    path = _user_path(user_id)

    if documents:
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(documents)
        return Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=path)
    else:
        return Chroma(persist_directory=path, embedding_function=embeddings)