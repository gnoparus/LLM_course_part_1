import chainlit as cl
# from langchain import PromptTemplate, OpenAI, LLMChain

from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain

import openai
import os 

template = """Question: {question}

Answer: Let's think step by step."""

# print(template.format(question="What is Oracle?"))

@cl.on_chat_start
def main():
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(
        prompt = prompt, 
        llm = OpenAI(temperature=1, streaming=True, ),         
        verbose=True,        
    )
    cl.user_session.set("llm_chain", llm_chain)

@cl.on_message
async def main(message: cl.Message):
    llm_chain = cl.user_session.get("llm_chain")

    res = await llm_chain.acall(message.content, callbacks = [cl.AsyncLangchainCallbackHandler()])

    await cl.Message(res["text"]).send()