import os
from typing import Any
from consts import INDEX_NAME
from dotenv import load_dotenv
load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI   
from langchain.chains import RetrievalQA
from pinecone import Pinecone
from langchain_community.vectorstores import Pinecone as PineconeLangChain

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])


def run_llm(query: str, chat_history:dict[str,Any]=[]) -> Any:
    
    embeddings = OpenAIEmbeddings()
    docsearch = PineconeLangChain.from_existing_index(index_name=INDEX_NAME, embedding=embeddings)
    chat = ChatOpenAI(verbose=True, temperature=0)
    #qa = RetrievalQA.from_chain_type(llm=chat, chain_type='stuff', retriever=docsearch.as_retriever(), return_source_documents=True)
    qa = ConversationalRetrievalChain.from_llm(llm=chat, retriever=docsearch.as_retriever(), return_source_documents=True)
    
    return qa({"question":query, "chat_history":chat_history})

if __name__ == "__main__":
    #abc = run_llm(query="What is RetrievalQA Chain")
    abc = run_llm(query="What is LangChain")

    print(abc)



