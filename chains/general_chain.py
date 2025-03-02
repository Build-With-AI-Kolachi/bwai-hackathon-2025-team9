from langchain.prompts import PromptTemplate
from llms.llms import create_llm
from prompts.templates import general_prompt

class GeneralChain:
    def __init__(self):
        self.llm = create_llm(model="gpt-4o-mini", temperature=0)

    def run(self, inputs):
        context = inputs.get("context")
        cleaned_query = inputs.get("cleaned_query")
        is_fallback = inputs.get("is_fallback")
        intents = inputs.get("intents")

        prompt = PromptTemplate(template=general_prompt, input_variables=['query'])

        chain = (
            prompt | self.llm
        )

        return chain.invoke({'query':cleaned_query})