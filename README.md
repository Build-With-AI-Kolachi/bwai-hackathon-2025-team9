# Chatbot Utility Service

This project provides utility services for a chatbot application. It includes various helper functions and modules to enhance the chatbot's functionality and performance.

## Features

- Easy integration with existing chatbot frameworks
- Modular design for flexibility
- Comprehensive documentation and examples
- FastAPI for API endpoints
- LangChain for language model integration
- Routes, Chain, Output Parsers are used for a more robust response.
- FAISS for vector store and document retrieval

## Installation

To install the necessary dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

### FastAPI Endpoints

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

### Example Endpoints

- **Check Status**: `GET /check_status`
- **Generate Vector**: `POST /generate_vector` currently under development
- **Get Categories**: `GET /get_categories` currently under development
- **Generate Response**: `POST /generate_response`

### Importing Modules

Import the required modules and use the provided functions in your chatbot application:

```python
from utils.utils import generate_response_util
from chains.preprocessing_chain import PreprocessingChain
from chains.domain_analysis_chain import DomainAnalysisChain
from chains.research_chain import ResearchOrchestrator
from chains.general_chain import GeneralChain
from chains.response_builer_chain import ResponseBuilder
from chains.valiator_chain import ValidatorChain
```

### Example Usage

```python
from utils.utils import faiss_embeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from entrypoint.mainChain import Chatbot


# Generate response
input_text = "What are the legal implications of breaking a contract?"
bot = Chatbot(vector_store=faiss_embeddings)
response = bot.chat(input_text)
print(response)
```

## Project Structure

```
utility-services/
├── agents/
│   ├── Agents.py
│   └── __init__.py
├── chains/
│   ├── domain_analysis_chain.py
│   ├── general_chain.py
│   ├── preprocessing_chain.py
│   ├── research_chain.py
│   ├── response_builer_chain.py
│   ├── valiator_chain.py
│   └── __init__.py
├── llms/
│   ├── llms.py
│   └── __init__.py
├── main.py
├── mainChain.py
├── pds/
│   ├── Analysis/AnalysisODS.py
│   ├── BuildResponse/BuildResponseODS.py
│   ├── Orchestration/OrchestrationODS.py
│   ├── Preprocessing/PreprocessingODS.py
│   ├── ResponseODS.py
│   ├── Validation/ValidationODS.py
│   └── __init__.py
├── prompts/
│   ├── templates.py
│   └── __init__.py
├── utils/
│   ├── errors.py
│   ├── memory.py (currently under development)
│   ├── tools.py (currently under development)
│   ├── utils.py
│   └── __init__.py
├── .gitignore
├── Procfile
├── README.md
└── requirements.txt
```
