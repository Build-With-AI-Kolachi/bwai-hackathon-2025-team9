from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


# A dictionary to store session history.
store = {}


# A function to retrieve session history based on the session ID.
def get_session_history(session_ids):
    print(f"[Conversation session ID]: {session_ids}")
    if session_ids not in store:  # When the session ID is not in the store.
        # Create a new ChatMessageHistory object and save it in the store.
        store[session_ids] = ChatMessageHistory()
    return store[session_ids]  # Return the session history for the given session ID