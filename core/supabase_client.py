from supabase import create_client
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

@st.cache_resource(show_spinner=False)
def get_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    return create_client(url, key)
