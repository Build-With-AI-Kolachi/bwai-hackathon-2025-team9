#Importing utilities used in chain
import logging
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.runnables import RunnableBranch

# Importing Chains
from chains.preprocessing_chain import PreprocessingChain
from chains.domain_analysis_chain import DomainAnalysisChain
from chains.research_chain import ResearchOrchestrator
from chains.general_chain import GeneralChain
from chains.response_builer_chain import ResponseBuilder
from chains.valiator_chain import ValidatorChain
# from utils.utils import faiss_embeddings

# from operator import itemgetter


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Chatbot:
    def __init__(self, vector_store):

        # Initialize the different chains
        self.preprocessor = PreprocessingChain()
        self.domain_analysis = DomainAnalysisChain()
        self.orchestrator = ResearchOrchestrator()
        self.general_chain = GeneralChain()
        self.builder = ResponseBuilder()
        self.validator = ValidatorChain(vector_store)
        
        # Define the legal chain
        self.branch_chain = (
            RunnablePassthrough()
            | self.orchestrator.analyze 
            | self.builder.build 
            | self.validator.validate
        )
        
        # Define the branch logic
        self.branch = RunnableBranch(
            # Check if the topic is not "legal" and execute general_chain if true.
            (lambda x: x["domain"] != "legal", self.general_chain.run),
            # If none of the above conditions match, execute branch_chain.
            self.branch_chain,
        )

        # Define the main chain
        self.chain = (
            RunnablePassthrough()
            | self.preprocessor.process
            | self.domain_analysis.classify_domain
            | self.branch
        )
        

    def chat(self, query, history=None):
        logger.info(f"Received query: {query}")
        response = self.chain.invoke({
            "query": query,
            "history": history or []
        })
        logger.info(f"Generated response: {response}")
        return response
