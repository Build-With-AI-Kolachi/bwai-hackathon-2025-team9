from langchain_openai import ChatOpenAI

def create_llm(model: str = "gpt-4o-mini", temperature: float = 0.3) -> ChatOpenAI:
    return ChatOpenAI(model=model, temperature=temperature)