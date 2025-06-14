from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

def create_llm(model: str = "gpt-4o-mini", temperature: float = 0.3) -> ChatOpenAI | ChatGoogleGenerativeAI:
    if model.startswith("gemini"):
        return ChatGoogleGenerativeAI(model=model)
    return ChatOpenAI(model=model, temperature=temperature)