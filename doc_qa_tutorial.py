import os

from langchain.document_loaders import PyPDFLoader, TextLoader 
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain.embeddings.openai import OpenAIEmbeddings 
from langchain.vectorstores import Chroma 
from langchain.chains import RetrievalQAWithSourcesChain 
from langchain.chat_models import ChatOpenAI 
import chainlit as cl
from chainlit.types import AskFileResponse

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

embeddings = OpenAIEmbeddings()

welcome_message = """Welcome to Doc QA App. 
1. Upload PDF or text file.
2. Ask question about the file.
"""

def process_file(file: AskFileResponse):
    import tempfile 

    if file.type == "text/plain":
        Loader = TextLoader 
    elif file.type == "application/pdf":
        Loader = PyPDFLoader 

    with tempfile.NamedTemporaryFile() as tempfile:
        tempfile.write(file.content)
        loader = Loader(tempfile.name)
        documents = loader.load() 

        docs = text_splitter.split_documents(documents)
        for i, doc in enumerate(docs):
            doc.metadata["source"] = f"source_{i}"

        return docs

def get_docsearch(file: AskFileResponse):
    docs = process_file(file)

    cl.user_session.set("docs", docs)

    docsearch = Chroma.from_documents(docs, embeddings)

    return docsearch 

@cl.on_chat_start 
async def start():
    await cl.Message(content="You can now chat with you PDFs.").send() 

    files = None 

    while files is None: 
        files = await cl.AskFileMessage(
            content=welcome_message, 
            accept=["text/plain", "application/pdf"], 
            max_size_mb=20, 
            timeout=180, 
        ).send() 

    file = files[0] 

    msg = cl.Message(content=f"Processing {file.name} ...")
    await msg.send() 

    docsearch = await cl.make_async(get_docsearch)(file) 

    chain = RetrievalQAWithSourcesChain.from_chain_type(
        ChatOpenAI(temperature=1, streaming=True), 
        chain_type="stuff", 
        retriever=docsearch.as_retriever(max_tokens_limit=4097)         
    )

    msg.content = f"`{file.name}` processed. You can now ask questions!" 
    await msg.update() 

    cl.user_session.set("chain", chain) 

@cl.on_message 
async def main(message: cl.Message):

    chain:RetrievalQAWithSourcesChain = cl.user_session.get("chain")
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"] 
    )
    cb.answer_reached = True 
    res = await chain.acall(message.content, callbacks=[cb]) 

    answer = res["answer"]
    sources = res["sources"].strip()
    source_elements = [] 

    docs = cl.user_session.get("docs")
    metadatas = [doc.metadata for doc in docs]
    all_sources = [m["source"] for m in metadatas] 

    if sources: 
        found_sources = [] 

        for source in sources.split(","):
            source_name = source.strip().replace(".", "") 

            try: 
                index = all_sources.index(source_name) 
            except ValueError:
                continue 

            text = docs[index].page_content 
            found_sources.append(source_name) 

            source_elements.append(cl.Text(content=text, name=source_name)) 

        if found_sources:
            answer += f"\nSources: {', '.join(found_sources)}"
        else: 
            answer += "\nNo source found" 

    if cb.has_streamed_final_answer:
        cb.final_stream.elements = source_elements 
        await cb.final_stream.update() 
    else: 
        await cb.Message(content=answer, elements=source_elements).send()






