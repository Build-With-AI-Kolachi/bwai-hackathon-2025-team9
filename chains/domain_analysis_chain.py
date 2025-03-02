import logging
from langchain.agents import AgentExecutor, Tool
from utils.utils import faiss_embeddings
from llms.llms import create_llm
from langchain.prompts import PromptTemplate
from prompts.templates import analysis_template
from langchain_core.output_parsers import JsonOutputParser
from pds.Analysis.AnalysisODS import AnalysisODS
from langchain.schema.runnable import RunnablePassthrough

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DomainAnalysisChain:
    def __init__(self):
        logger.info("Initializing Domain Analysis Chain")
        # Initialize the researcher, analyst, and verifier agents
        self.llm = create_llm()
        logger.info("Domain Analysis Chain initialized successfully")

    def classify_domain(self, inputs):
        logger.info("Starting analysis with inputs: %s", inputs)

        # Extract preprocessed data
        cleaned_query = inputs.get("cleaned_query")
        logger.info("Extracted cleaned_query: %s", cleaned_query) 

        # Analyze if domain specific or not.
        analysis_response = self._perform_domain_analysis(inputs)
        
        return analysis_response
    

    def _perform_domain_analysis(self,inputs):
        logger.info("Creating analysis chain")
        parser = JsonOutputParser(pydantic_object=AnalysisODS)
        logger.info("Initialized JsonOutputParser")

        format_instructions = parser.get_format_instructions()
        logger.info(f"Format instructions: {format_instructions}")

        prompt = PromptTemplate(template=analysis_template, input_variables=['query'], partial_variables={"format_instructions":format_instructions})        
        logger.info(f"Created PromptTemplate from analysis_template: {prompt}")
        
        query = inputs["cleaned_query"]
        logger.info(f"Received query: {query}")

        chain = ({"query" : RunnablePassthrough()} 
                 | prompt 
                 | self.llm 
                 | parser
                 )
        
        logger.info("Created chain with preprocessor_template and LLM")

        response = chain.invoke({"query":query})
        logger.info(f"Received response: {response}")

        # parsed_response = parser.parse(response)
        # self.logger.info(f"Parsed response: {parsed_response}")
        
        return {
            **inputs,
            "domain": response.get("domain"),
            "sub_category": response.get("sub_category")
        }