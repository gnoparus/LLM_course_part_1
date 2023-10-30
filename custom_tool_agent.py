from langchain.chat_models import ChatOpenAI
from langchain.tools import ShellTool

from langchain.agents import initialize_agent, AgentType, Tool
import os
import chainlit as cl


def multiplier(a, b):
    return a * b


def parse_multiplier(txt: str):
    a, b = txt.split(",")
    return multiplier(int(a), int(b))


@cl.on_chat_start
def start():
    llm = ChatOpenAI(temperature=0.9, max_tokens=2000)

    tools = [
        Tool(
            name="Multiplier",
            func=parse_multiplier,
            description="useful for when you need to multiply two numbers together. The input to this tool should be a comma separated list of numbers of length two, representing the two numbers you want to multiply together. For example, `1,2` would be the input if you wanted to multiply 1 by 2.",
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
    cl.user_session.set("agent", agent_chain)


# Sample Input: three times 4 x 5


@cl.on_message
async def main(message: cl.Message):
    agent_chain = cl.user_session.get("agent")
    cb = cl.LangchainCallbackHandler(stream_final_answer=True)

    res = await cl.make_async(agent_chain.run)(message.content, callbacks=[cb])
    await cl.Message(content=res).send()
