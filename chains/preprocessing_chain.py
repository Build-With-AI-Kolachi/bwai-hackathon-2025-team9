import logging
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from llms.llms import create_llm
from prompts.templates import preprocessor_template
from pds.Preprocessing.PreprocessingODS import PreprocessingODS
from langchain.schema.runnable import RunnablePassthrough

class PreprocessingChain:
    def __init__(self):
        self.llm = create_llm(model="gpt-4o-mini", temperature=0.3)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def process(self, inputs):
        self.logger.info("Starting the preprocessing chain")
        
        parser = JsonOutputParser(pydantic_object=PreprocessingODS)

        format_instructions = parser.get_format_instructions()

        prompt = PromptTemplate(template=preprocessor_template, input_variables=["query"], partial_variables={"format_instructions":format_instructions})

        query = inputs["query"]

        chain = ({"query" : RunnablePassthrough()} 
                 | prompt 
                 | self.llm 
                 | parser
                 )
        

        response = chain.invoke({"query":query})
        self.logger.info(f"Received response: {response}")

        # parsed_response = parser.parse(response)
        # self.logger.info(f"Parsed response: {parsed_response}")
        
        return {
            **inputs,
            "cleaned_query": response.get("cleaned_query"),
        }