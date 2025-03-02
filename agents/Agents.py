from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from llms.llms import create_llm
from utils.tools import tools
from prompts.templates import tool_calling_template

llm = create_llm(model="gpt-4o-mini", temperature=0)

prompt = PromptTemplate.from_template(tool_calling_template)

# Creating Agent
agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

# Example usage:
# agent = LangChainAgent(api_key="your_openai_api_key")
# response = agent.run("What is the capital of France?")
# print(response)