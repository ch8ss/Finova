from core.supabase_client import get_supabase


def save_message(user_id: str, role: str, content: str):
    sb = get_supabase()
    sb.table("conversations").insert({
        "user_id": user_id,
        "role": role,
        "content": content,
    }).execute()


def load_messages(user_id: str):
    sb = get_supabase()
    res = (
        sb.table("conversations")
        .select("role, content")
        .eq("user_id", user_id)
        .order("created_at")
        .execute()
    )
    return [{"role": r["role"], "content": r["content"]} for r in res.data]


def save_document(user_id: str, filename: str, file_type: str):
    sb = get_supabase()
    sb.table("documents").insert({
        "user_id": user_id,
        "filename": filename,
        "file_type": file_type,
    }).execute()
