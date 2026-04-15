from langchain_groq import ChatGroq
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

@st.cache_resource(show_spinner=False)
def get_llm():
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile",
        temperature=0.2,
    )

@st.cache_resource(show_spinner=False)
def get_vision_llm():
    # llama-4-scout supports image input on Groq
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0.2,
    )