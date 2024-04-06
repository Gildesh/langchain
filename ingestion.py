from dotenv import load_dotenv
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain.text_splitter   import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
import pinecone
from langchain_community.vectorstores import Pinecone
import os
from consts import INDEX_NAME
load_dotenv()
def ingest_docs()->None:
    print(os.getcwd())
    loader = ReadTheDocsLoader('langchain-docs\\',encoding="utf8")
    #loader = ReadTheDocsLoader("rtdocs", features="html.parser")
    raw_documents = loader.load()
    print('Chuny')
    print(raw_documents)
    print(f"loaded {len(raw_documents)}documents")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50, separators=["\n\n", "\n", " ", ""])
    documents = text_splitter.split_documents(documents=raw_documents)
    print(f"Splitted into {len(documents)} chunks")
    for doc in documents:
        old_path = doc.metadata['source']
        new_url = old_path.replace("langchain_docs", "https:/")
        doc.metadata.update({'source': new_url})

    print(f"Going to insert {len(documents)} to Pinecone")
    embeddings = OpenAIEmbeddings()
    Pinecone.from_documents(documents, embeddings, index_name=INDEX_NAME)
    print(f"Inserted {len(documents)}")
    print("Added to Pinecone Vectorstores vectors")
if __name__ == '__main__':

    ingest_docs() 