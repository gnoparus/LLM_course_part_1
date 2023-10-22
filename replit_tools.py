from langchain.chat_models import ChatOpenAI
from langchain.llms.openai import OpenAI
from langchain.tools.python.tool import PythonREPLTool
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.agents.agent_toolkits.python.base import create_python_agent
import os

llm = ChatOpenAI(temperature=0.9, max_tokens=2000)

agent_chain = create_python_agent(
    tool=PythonREPLTool(),
    llm=llm,
    max_iterations=5,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)

agent_chain.run("What is sum of 1 to 1000?")
