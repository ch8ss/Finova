from langchain_community.chat_message_histories import ChatMessageHistory

# In-memory store keyed by session_id — no stale files, resets on restart
_store: dict[str, ChatMessageHistory] = {}

def get_memory(session_id: str) -> ChatMessageHistory:
    if session_id not in _store:
        _store[session_id] = ChatMessageHistory()
    return _store[session_id]
