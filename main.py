import logging
import os
import time
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
import requests
from fastapi import FastAPI, Body, HTTPException
from typing import List, Dict
import logging

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Custom Imports
from utils import *

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()
origins = ["http://localhost:8080", "https://your-vue-app.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)
embeddings = OpenAIEmbeddings()
faiss_embeddings = FAISS.load_local("./index", OpenAIEmbeddings())

@app.get("/check_status")
def check_status():
    if faiss_embeddings:
        return {"status": 1}
    else:
        return {"status": 0}

@app.post("/generate_vector")
def generate_vector(
    selectedOptions: List[str] = Body(...),
    categories: List[Dict[str, str]] = Body(...)
):
    logger.info("RequestIn: Generate Vector Function.")
    logger.info("Options: %s", selectedOptions)
    logger.info("Categories: %s", categories)
    global faiss_embeddings
    return {"success": True, "message": "Vector generated successfully."}

    # if not selectedOptions:
    #     logger.warning("No selectedOptions provided.")
    #     raise HTTPException(status_code=400, detail="No selectedOptions provided.")
    
    # if not categories:
    #     logger.warning("No categories provided.")
    #     raise HTTPException(status_code=400, detail="No categories provided.")
    
    # try:
    #     documents = []
    #     for option in selectedOptions:
    #         docs = get_categories_data(category=option, categories=categories)
    #         if docs:
    #             documents.extend(docs)
    #             time.sleep(0.5)
    #         else:
    #             logger.warning(f"No documents found for option: {option}")
        
    #     if not documents:
    #         logger.warning("No documents generated from provided selectedOptions.")
    #         raise HTTPException(status_code=400, detail="No documents generated from provided selectedOptions.")
        
    #     logger.info("Documents loaded and split successfully.")

    #     vectorstore = FAISS.from_documents(documents, embedding=OpenAIEmbeddings())
    #     vectorstore.save_local("../index")
        
    #     faiss_embeddings = FAISS.load_local("../index", OpenAIEmbeddings())
    #     logger.info("Vector store created and saved successfully.")
        
    #     return {"success": True, "message": "Vector generated successfully."}
    
    # except FileNotFoundError as e:
    #     logger.error(f"File not found: {e}", exc_info=True)
    #     raise HTTPException(status_code=404, detail="File not found.")
    
    # except Exception as e:
    #     logger.error(f"An unexpected error occurred: {e}", exc_info=True)
    #     raise HTTPException(status_code=500, detail="An unexpected error occurred.")

@app.get("/get_categories")
def get_categories():
    categories = []
    try:
        # Get the base URL from environment variable
        PAKISTAN_CODE_BASE_URL = os.getenv("PAKISTAN_CODE_BASE_URL")
        if not PAKISTAN_CODE_BASE_URL:
            raise ValueError("Environment variable 'PAKISTAN_CODE_BASE_URL' not set")

        try:
            response = requests.get(PAKISTAN_CODE_BASE_URL)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Error in fetching the URL '{PAKISTAN_CODE_BASE_URL}': {e}")
            return []

        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            category_div = soup.find('div', id='category')
            if not category_div:
                raise ValueError("Div with id 'category' not found")

            ul_element = category_div.find("ul")
            if not ul_element:
                raise ValueError("No <ul> element found within the category div")

            deptlist_divs = ul_element.find_all('div', class_='deptlist')
            if not deptlist_divs:
                logger.warning("No department list divs found")
                return []

            for i, div in enumerate(deptlist_divs):
                a = div.find('a')
                if a:
                    link_info = extract_links_info(a)
                    categories.append(link_info)
                    logger.info(f"Inserted: {link_info} in Categories")
                else:
                    logger.warning(f"No <a> tag found in deptlist div {i}")

        except (AttributeError, ValueError) as e:
            logger.error(f"Error processing HTML content: {e}")
            return []

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return []

    return categories

@app.post('/generate_response')
def generate_response(input: Dict[str, str] = Body(...)):
    input_text = input.get("input_text")
    if not input_text:
        raise HTTPException(status_code=400, detail="input_text is required")
    print("Received input_text:", input_text)  # Print received data
    vector_store_retriever = faiss_embeddings.as_retriever()
    return generate_response_util(input_text, vector_store_retriever)
