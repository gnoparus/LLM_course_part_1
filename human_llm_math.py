from langchain.chat_models import ChatOpenAI
from langchain.llms.openai import OpenAI
from langchain.agents import load_tools, initialize_agent, AgentType
import os

llm = ChatOpenAI(temperature=0.9, max_tokens=2000)
math_llm = OpenAI(temperature=0.3, max_tokens=1000)

tools = load_tools(["human", "llm-math"], llm=math_llm)

agent_chain = initialize_agent(
    tools=tools,
    llm=llm,
    max_iterations=5,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)

agent_chain.run("What is my math problem and solution?")
