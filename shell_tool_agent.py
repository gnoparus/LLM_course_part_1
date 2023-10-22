from langchain.chat_models import ChatOpenAI
from langchain.tools import ShellTool

from langchain.agents import initialize_agent, AgentType, Tool
import os
import chainlit as cl


@cl.on_chat_start
def start():
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

    # print(shell_tool.description)
    # print(shell_tool.args)

    agent_chain = initialize_agent(
        tools=tools,
        llm=llm,
        max_iterations=5,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
    )
    cl.user_session.set("agent", agent_chain)


@cl.on_message
async def main(message: cl.Message):
    agent_chain = cl.user_session.get("agent")
    agent_chain.run(message.content)
