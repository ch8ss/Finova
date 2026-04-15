from core.supabase_client import get_supabase


def save_message(user_id: str, role: str, content: str):
    sb = get_supabase()
    sb.table("Conversations").insert({
        "user_id": user_id,
        "role": role,
        "content": content,
    }).execute()


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


def delete_messages(user_id: str):
    try:
        sb = get_supabase()
        sb.table("Conversations").delete().eq("user_id", user_id).execute()
    except Exception:
        pass
