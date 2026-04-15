import streamlit as st
from core.supabase_client import get_supabase
from core.database import load_messages


def restore_session(user_id: str) -> bool:
    """Restore session state from a stored user_id. Returns True if successful."""
    try:
        sb = get_supabase()
        result = sb.table("Users").select("owner_name, business_name, business_type").eq("id", user_id).execute()
        if not result.data or len(result.data) == 0:
            # Profile genuinely doesn't exist — clear uid
            st.query_params.clear()
            return False
        profile = result.data[0]
        st.session_state["user_id"]       = user_id
        st.session_state["owner_name"]    = profile["owner_name"]
        st.session_state["business_name"] = profile["business_name"]
        st.session_state["business_type"] = profile["business_type"]
        if "messages" not in st.session_state:
            st.session_state["messages"]      = load_messages(user_id)
            st.session_state["total_queries"] = len([m for m in st.session_state["messages"] if m["role"] == "user"])
        return True
    except Exception:
        # Transient error — don't clear uid, let the next load retry
        return False
