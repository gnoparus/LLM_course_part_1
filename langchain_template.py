import chainlit as cl
from langchain import PromptTemplate, OpenAI, LLMChain
import openai
import os 

template = """Question: {question}

Answer: Let's think step by step."""

template.format(question="What is Oracle?")