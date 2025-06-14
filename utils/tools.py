import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from typing import Dict, Optional
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool

# from utils.utils import faiss_embeddings

# @tool
# def vector_retriever_tool() -> Optional[Dict]:
#     """ Retrieve legal documents based on query """
#     return create_retriever_tool(
#             faiss_embeddings.as_retriever(),
#             name="vector_retriever_tool",
#             description="Retrieve legal documents based on query",
#     )

# PDF Search Tool







# Register all the tools
tools = [vector_retriever_tool]

