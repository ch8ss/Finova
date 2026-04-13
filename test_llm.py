from core.llm import get_llm

llm = get_llm()
response = llm.invoke("Say 'LLM is working!' and nothing else.")
print(response.content)
