from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent, AgentType
import os
import chainlit as cl


@cl.on_chat_start
def start():
    llm = ChatOpenAI(temperature=0.9)
    tools = load_tools(["arxiv"])

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
    cb = cl.AsyncLangchainCallbackHandler(stream_final_answer=True)

    await cl.make_async(agent_chain.run)(message.content, callbacks=[cb])
