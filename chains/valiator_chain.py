import logging
from utils.errors import ValidationError
from langchain_core.prompts import PromptTemplate
from prompts.templates import finding_absolutes_template
from llms.llms import create_llm
from langchain_core.output_parsers import JsonOutputParser
from pds.Validation.ValidationODS import ValidationODS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ValidatorChain:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.llm = create_llm(model="gpt-4o-mini", temperature=0.3)

    def validate(self, inputs):
        logger.info("Starting validation process")
        if inputs['sub_category'] == 'Needs Clarification':
            return inputs['response']
        else:
            # Initialize the JSON output parser with the ValidationODS schema
            parser = JsonOutputParser(pydantic_object=ValidationODS)

            # Create a prompt template using the finding_absolutes_template
            prompt = PromptTemplate(template=finding_absolutes_template, input_variables=["analysis"], partial_variables={"format_instructions": parser.get_format_instructions()})


            # Create the chain of prompt, LLM, and parser
            abs_chain = prompt | self.llm | parser

            # Invoke the chain with the analysis from the response
            abs_response = abs_chain.invoke({"analysis": inputs['response']})

            # Check if the response contains an overly absolute statement
            if abs_response['is_true']:
                raise ValidationError("Overly absolute statement detected")

            # Cross-check references
            for ref in inputs["analyst_response"]['references']:
                # Verify each reference using the vector store
                if not self._verify_reference(ref):
                    raise ValidationError(f"Invalid reference: {ref}")

            logger.info("Validation process completed successfully")
            return inputs['response']

    def _verify_reference(self, reference):
        # Perform a similarity search in the vector store to verify the reference
        result = bool(self.vector_store.similarity_search(reference, k=1))
        return result