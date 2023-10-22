from langchain.chat_models import ChatOpenAI
from langchain.tools import YouTubeSearchTool

from langchain.agents import initialize_agent, AgentType, Tool
import os

llm = ChatOpenAI(temperature=0.9, max_tokens=2000)

tool = YouTubeSearchTool()

tools = [
    Tool(
        name="YouTube Search",
        func=tool.run,
        description="useful for when you need to give links to youtube videos. Remember to put https://youtube.com/ in front of every link to complete it",
    )
]

agent_chain = initialize_agent(
    tools=tools,
    llm=llm,
    max_iterations=5,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)

agent_chain.run("What is VFX Artists React youtube video about starwars?")
