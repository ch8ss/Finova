from core.memory import get_memory

memory = get_memory("test_session")

memory.add_user_message("Hello, my name is Srivani.")
memory.add_ai_message("Hi Srivani! Nice to meet you.")

print("Saved messages:")
for msg in memory.messages:
    print(f"  {msg.type}: {msg.content}")
