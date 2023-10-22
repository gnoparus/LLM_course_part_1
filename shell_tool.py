from langchain.chat_models import ChatOpenAI
from langchain.tools import ShellTool

from langchain.agents import initialize_agent, AgentType, Tool
import os

llm = ChatOpenAI(temperature=0.9, max_tokens=2000)

shell_tool = ShellTool()

tools = [
    Tool(
        name="Bash",
        func=shell_tool.run,
        description=shell_tool.description
        + f"args {shell_tool.args}".replace("{", "{{").replace("}", "}}"),
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

agent_chain.run(
    "create a text file called 'number400.txt' and inside it, add text '400' in the file"
)
