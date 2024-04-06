from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone
from langchain.chains import RetrievalQA
import pinecone
from langchain.llms import OpenAI

load_dotenv()
pinecone.Pinecone(
   api_key="1c23dccd-8a6a-4b05-b7da-f480353a8938",
   environment="default",
)
import os


if __name__=="__main__":
    print('Hello Vector Store')
    print(os.getcwd())
    loader = TextLoader('mediumblogs\\mediumblog1.txt',encoding='utf-8')
    documents = loader.load()
    print(documents)
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    texts= text_splitter.split_documents(documents)
    print(len(texts))
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
    docsearch = Pinecone.from_documents(texts, embeddings, index_name='medium-blogs-embeddings-index')
    qa = RetrievalQA.from_chain_type(
        llm =OpenAI(), chain_type='stuff', retriever=docsearch.as_retriever()
    )
    query = "What is a vector database? Give me a 15 word answer for a beginner"
    result = qa({"query": query})
    print("dick")
    print(result)
