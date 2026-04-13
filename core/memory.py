from langchain_community.chat_message_histories import FileChatMessageHistory
import os

def get_memory(session_id: str):
    os.makedirs("memory_store", exist_ok=True)
    return FileChatMessageHistory(
        file_path=f"memory_store/{session_id}.json"
    )
