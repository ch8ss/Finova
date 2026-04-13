from langchain_community.document_loaders import PyPDFLoader, CSVLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import pandas as pd
import tempfile
import os

VECTORSTORE_PATH = "data/vectorstore"

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

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

def get_vectorstore(documents=None):
    embeddings = get_embeddings()
    os.makedirs(VECTORSTORE_PATH, exist_ok=True)

    if documents:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
        )
        chunks = splitter.split_documents(documents)
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=VECTORSTORE_PATH,
        )
    else:
        vectorstore = Chroma(
            persist_directory=VECTORSTORE_PATH,
            embedding_function=embeddings,
        )

    return vectorstore