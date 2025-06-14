import logging
from llms.llms import create_llm
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pds.Orchestration.OrchestrationODS import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResearchOrchestrator:
    def __init__(self):
        # Initialize LLM
        self.llm = create_llm()

    def analyze(self, inputs):
        logger.info(f"Processing query in {inputs['domain']} domain")
        if inputs['sub_category'] == 'Needs Clarification':
            return {**inputs}
        
        # Get the cleaned query
        cleaned_query = inputs.get("cleaned_query")
        
        # Create a simple prompt for direct response
        prompt_template = """Provide a clear and concise response to the following query:
        Query: {query}
        
        Output Format: {format_instructions}"""
        
        # Initialize the output parser
        parser = JsonOutputParser(pydantic_object=AnalystODS)
        format_instructions = parser.get_format_instructions()
        
        # Create the prompt
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["query"],
            partial_variables={"format_instructions": format_instructions}
        )
        
        # Create the chain
        response_chain = prompt | self.llm | parser
        
        # Get the response
        response = response_chain.invoke({"query": cleaned_query})
        
        logger.info("Response generated successfully")
        return {**inputs, "priority": response['priority'], "analyst_response": response}
