from core.supabase_client import get_supabase


def save_message(user_id: str, role: str, content: str):
    try:
        sb = get_supabase()
        sb.table("Conversations").insert({
            "user_id": user_id,
            "role": role,
            "content": content,
        }).execute()
    except Exception:
        pass  # Don't crash the app if DB write fails


def load_messages(user_id: str):
    sb = get_supabase()
    res = (
        sb.table("Conversations")
        .select("role, content")
        .eq("user_id", user_id)
        .order("created_at")
        .execute()
    )
    return [{"role": r["role"], "content": r["content"]} for r in res.data]


def save_document(user_id: str, filename: str, file_type: str):
    sb = get_supabase()
    sb.table("Documents").insert({
        "user_id": user_id,
        "filename": filename,
        "file_type": file_type,
    }).execute()
