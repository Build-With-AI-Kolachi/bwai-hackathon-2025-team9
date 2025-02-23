from pprint import pprint
from tempfile import NamedTemporaryFile
from langchain_community.document_loaders import PyPDFLoader
import os
from bs4 import BeautifulSoup
import requests
import logging
import time
# import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
# from langchain.chat_models import ChatOpenAI
# from langchain.chains import LLMChain
from langchain.schema.output_parser import StrOutputParser

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Utilities For The FastApi Service
def extract_links_info(a):
    logging.debug("RequestIn: extract_links_info with: %s", a)
    return {"name": a.get_text(strip=True), "url": a.get('href')}

def get_categories_data(category : str, categories: list):
    acts = []
    logging.info("RequestIn: get_categories_data")
    try:
        for cat in categories:
            logging.info("Inside For Loop with category: %s", cat["name"])
            logging.info("and with category: %s", category)
            if cat['name'] == category:
                logging.info("Fetching data for category: %s", cat["name"])
                response = requests.get('https://pakistancode.gov.pk/english/' + cat["url"])
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                accordion_section_title_divs = soup.find_all('div', class_='accordion-section-title')
                if accordion_section_title_divs:
                    for div in accordion_section_title_divs:
                        a = div.find('a')
                        acts.append(extract_links_info(a))
                else:
                    logging.warning("No accordion section titles found for category: %s", cat["name"])
            else:
                logging.info("Category %s not matched.", cat["name"])
    except requests.RequestException as e:
        logging.error("Error fetching the URL: %s", e)
    
    print("Acts for the category: \n",acts)
    if acts:
        downloaded = download_law(acts)
    else:
        logging.error("Error in fetching the documents for the acts")
    logging.info("Fetched data for category: %s successfully!", cat["name"])
    logging.info("RequestOut: get_categories_data") 
    return downloaded

def download_law(acts):
    read_pdf = []
    logging.info("RequestIn: download_law")
    try:
        for act in acts:
            logging.info("Act Name: %s",act["name"])
            base_url = 'https://pakistancode.gov.pk/english/' + act["url"]
            logging.info("Downloading law from URL: %s", base_url)
            response = requests.get(base_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            iframe = soup.find('iframe')
            if iframe and 'src' in iframe.attrs:
                pdf_url = iframe['src']
                pdf_url = pdf_url.split('/')
                pdf_url = pdf_url[0] + '//' + pdf_url[2] + '/' + pdf_url[5] + '/' + pdf_url[6]
                logging.info("Reading the following PDF: %s", pdf_url)
                read_pdf.extend(read_pdf_from_url(pdf_url,act))
                logging.info("Read the following PDF: %s successfully!", pdf_url)
            else:
                logging.error("No valid iframe found in %s", base_url)
        logging.info("RequestOut: get_categories_data") 
        return read_pdf
    except requests.RequestException as e:
        logging.error("Error fetching law page: %s", e)
        
    logging.info("Could not read pdf.")
    logging.info("RequestOut: download_law")
    return []

def read_pdf_from_url(url,act):
    logging.info("RequestIn: read_pdf_from_url")
    documents = []
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            with NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name
                temp_file.flush()
            
            logging.info("Loading and splitting from temporary PDF file: %s", temp_file_path)
            loader = PyPDFLoader(temp_file_path)
            documents = loader.load_and_split()
            for doc in documents:
                doc.metadata['source'] = act["name"]
            print(documents[0].metadata)
            logging.info("Done Loading and splittng from temporary PDF file: %s", temp_file_path)
            
            # Clean up the temporary file
            os.remove(temp_file_path)
            logging.info("Temporary file removed: %s", temp_file_path)
            logging.info("Returning documents: %s", temp_file_path)
            logging.info("RequestOut: read_pdf_from_url")
            return documents
        else:
            logging.error("Failed to fetch PDF: Status code %d", response.status_code)
    except Exception as e:
        logging.error("An error occurred while reading the PDF: %s", e)
    logging.info("Unexpected Error Occured: %s", temp_file_path)
    logging.info("RequestOut: read_pdf_from_url")
    return documents

def generate_response_util(input_text,vector_store_retriever):
    print("RequestIn: Generate ChatBot Response.")
    template = """Imagine there are three legal expert required to answer legal queries based only on the following context:
    {context}

    Please ensure your answers:
    1. Are based solely on the provided context.
    2. Include specific references to the relevant sections of the law.
    3. Are structured with a brief overview followed by detailed information if necessary.
    4. Offer clarity on any ambiguous queries by asking for additional details if needed.
     experts are answering this question.

    Examples:
    Question: When can police arrest without a warrant?
    Answer: 
    Police can arrest without a warrant in the following situations:
    1. If a person is involved in a cognizable offence or against whom a reasonable complaint has been made, or credible information has been received.
    2. If a person is found in possession of implements of housebreaking without lawful excuse.
    3. If a person is proclaimed as an offender.
    4. If a person obstructs a police officer in their duties.

    References:
    THE CODE OF CRIMINAL PROCEDURE, 1898, CHAPTER V OF ARREST, ESCAPE AND RETAKING, Section 54.

    Question: When can an inquiry or trial take place?
    Answer:
    An inquiry or trial can occur within the local limits of the jurisdiction where the offense was committed or where the consequences ensued.

    References:
    THE CODE OF CRIMINAL PROCEDURE, 1898, PART VI PROCEEDINGS IN PROSECUTIONS, CHAPTER XV OF THE JURISDICTION OF THE CRIMINAL COURTS IN INQUIRIES AND TRIALS, Section 177.

    Question: Can police arrest me if I am in a different city?
    Answer: 
    Yes, a police officer can pursue and arrest you anywhere in Pakistan for the purpose of apprehending you without a warrant if you are accused of an offense.

    References:
    THE CODE OF CRIMINAL PROCEDURE, 1898, CHAPTER V OF ARREST, ESCAPE AND RETAKING, Section 58.

    All legal experts will write down 1 step of their thinking,
    then share it with the group along with the references for their thought as they are quite important in legal dealings.
    Then all experts will go on to the next step, etc.
    If any expert realises they're wrong at any point then they leave.
    Do not Print the above thought process.
    
    Question: {question}
    """

    retriever = vector_store_retriever
    prompt = ChatPromptTemplate.from_template(template)
    model = ChatOpenAI(temperature=0.8)

    chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
    )


    response = chain.invoke(input_text)

    # words = response.split(' ')
    # for word in words:
    #     yield word + " "
    #     time.sleep(0.05)

    return response
