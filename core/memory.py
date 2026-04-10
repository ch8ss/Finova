from langchain_classic.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
import os

def get_memory(session_id: str):
    os.makedirs("memory_store", exist_ok=True)

    history = FileChatMessageHistory(
        file_path=f"memory_store/{session_id}.json"
    )

    memory = ConversationBufferMemory(
        chat_memory=history,
        memory_key="chat_history",
        return_messages=True,
    )

    return memory