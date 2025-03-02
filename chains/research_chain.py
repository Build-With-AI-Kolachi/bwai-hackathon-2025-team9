import logging
from langchain.agents import AgentExecutor, Tool
from utils.utils import faiss_embeddings
from llms.llms import create_llm
from langchain.prompts import PromptTemplate
from prompts.templates import analysis_template
from langchain_core.output_parsers import JsonOutputParser
from pds.Orchestration.OrchestrationODS import *
from langchain.schema.runnable import RunnablePassthrough

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResearchOrchestrator:
    def __init__(self):
        
        # Store the domain dynamically
        # self.domain = domain

        # Initialize LLM and Agents
        self.llm = create_llm()
        self.researcher = self._create_researcher()
        self.analyst = self._create_analyst()
        self.verifier = self._create_verifier()

    def analyze(self, inputs):
        logger.info(f"Starting research of query in {inputs['domain']} domain")
        if inputs['sub_category'] == 'Needs Clarification':
            return {**inputs}
        else:
            # Extract preprocessed data
            cleaned_query = inputs.get("cleaned_query")
            # logger.info("Extracted cleaned_query: %s", cleaned_query) 
            
            # Research Phase
            logger.info("Starting research phase")
            context_documents = self.researcher.invoke(cleaned_query)
            
            # Compile context from retrieved documents
            context = ' '.join(doc.page_content for doc in context_documents)
            # logger.info("Compiled context: %s", context)
            
            # Analysis Phase
            logger.info("Starting analysis phase")
            analyst_response = self.analyst.invoke({"context": context, "query": cleaned_query})
            # logger.info("Analysis phase completed with interpretation: %s", analyst_response)
            
            # Verification Phase
            logger.info("Starting verification phase")
            verified = self.verifier.invoke({
                "interpretation": analyst_response['interpretation'],
                "references": analyst_response['references'],
                "context": context,
                "query": cleaned_query
            })
            # logger.info("Verification phase completed with verified analysis: %s", verified)
            logger.info("Research Completed with {"+ f"analysis: { verified['analysis'] }, analyst_response: {analyst_response}"+"}")
            
            return {**inputs, "analysis":  verified['analysis'], "analyst_response": analyst_response}
    
    def _create_researcher(self):
        """Creates a domain-agnostic research agent"""
        # logger.info("Creating researcher agent")
        researcher = faiss_embeddings.as_retriever()
        logger.info("Researcher agent created successfully")
        return researcher

    def _create_analyst(self):
        """Creates a general-purpose analyst agent"""
        # logger.info("Creating analyst agent")

        # Define the prompt template for the analyst
        prompt_template = """You are an expert analyst. Interpret the context strictly based on the provided query and provide references found in the context.
                             Output Format: {format_instructions}
                             Query: {query}
                             Context: {context}"""
        
        # Initialize the output parser
        parser = JsonOutputParser(pydantic_object=AnalystODS)
        format_instructions = parser.get_format_instructions()

        # Create the prompt with format instructions
        prompt = PromptTemplate(template=prompt_template, input_variables=["context","query"], partial_variables={"format_instructions": format_instructions})
        # logger.info(f"Prompt with Format Instructions: {prompt}")

        # Create the LLM for the analyst
        analyst = create_llm(model="gpt-4o-mini", temperature=0.8)
        
        # Chain the prompt, LLM, and parser together
        analyst_chain = prompt | analyst | parser
        logger.info("Analyst agent created successfully")
        return analyst_chain

    def _create_verifier(self):
        """Creates a flexible verifier agent"""
        # logger.info("Creating verifier agent")

        # Define the prompt template for the verifier
        prompt_template = """You are a senior verifier. Check for:
                   1. Citation accuracy
                   2. Logical consistency
                   3. Compliance
                   Output Format: {format_instructions} 
                   In Analysis: {interpretation}
                   and references : {references}
                   Based on {context} and the provided query {query}"""
        
        # Initialize the output parser
        parser = JsonOutputParser(pydantic_object=VerifierODS)
        format_instructions = parser.get_format_instructions()

        # Create the prompt with format instructions
        prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'interpretation', 'references','query'], partial_variables={"format_instructions": format_instructions})
        
        # Create the LLM for the verifier
        verifier = create_llm(model="gpt-4", temperature=0.8)
        
        # Chain the prompt, LLM, and parser together
        verifier_chain = prompt | verifier | parser
        
        logger.info("Verifier agent created successfully")
        return verifier_chain
