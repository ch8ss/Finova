import logging
from core.supabase_client import get_supabase

logger = logging.getLogger(__name__)


def save_message(user_id: str, role: str, content: str, conversation_id: str = None):
    try:
        sb = get_supabase()
        row = {"user_id": user_id, "role": role, "content": content}
        if conversation_id:
            row["conversation_id"] = conversation_id
        sb.table("Conversations").insert(row).execute()
    except Exception as e:
        logger.error(f"save_message failed: {e}")


def load_messages(user_id: str, conversation_id: str = None, limit: int = 100):
    sb = get_supabase()
    query = (
        sb.table("Conversations")
        .select("role, content")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(limit)
    )
    if conversation_id:
        query = query.eq("conversation_id", conversation_id)
    res = query.execute()
    return [{"role": r["role"], "content": r["content"]} for r in reversed(res.data or [])]


def load_conversations(user_id: str, limit: int = 20):
    """Return one entry per conversation (most recent first), showing the first user message."""
    sb = get_supabase()
    res = (
        sb.table("Conversations")
        .select("conversation_id, content, created_at")
        .eq("user_id", user_id)
        .eq("role", "user")
        .not_.is_("conversation_id", "null")
        .order("created_at")
        .execute()
    )
    seen = {}
    for row in res.data:
        cid = row["conversation_id"]
        if cid not in seen:
            seen[cid] = {
                "id": cid,
                "first_message": row["content"],
                "created_at": row["created_at"],
            }
    convos = sorted(seen.values(), key=lambda x: x["created_at"], reverse=True)
    return convos[:limit]


def get_last_conversation_id(user_id: str):
    """Return the most recent conversation_id for this user, or None."""
    try:
        sb = get_supabase()
        res = (
            sb.table("Conversations")
            .select("conversation_id")
            .eq("user_id", user_id)
            .not_.is_("conversation_id", "null")
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        if res.data:
            return res.data[0]["conversation_id"]
    except Exception:
        pass
    return None


def delete_conversation(user_id: str, conversation_id: str):
    try:
        sb = get_supabase()
        sb.table("Conversations").delete().eq("user_id", user_id).eq("conversation_id", conversation_id).execute()
    except Exception as e:
        logger.error(f"delete_conversation failed: {e}")
