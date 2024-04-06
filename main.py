from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA
import os
os.environ['OPENAI_API_KEY'] = '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'
if __name__=='__main__':
    print('hi')
    pdf_path = 'C:\\Users\\admin\\Desktop\\vectorstore-in-memory\\2210.03629.pdf'
    loader = PyPDFLoader(file_path =pdf_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap = 30, separator="\n")
    docs = text_splitter.split_documents(documents=documents)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local('faiss_index_react')
    new_vectorstore = FAISS.load_local('faiss_index_react',embeddings,allow_dangerous_deserialization=True)
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type='stuff', retriever= new_vectorstore.as_retriever())
    res = qa.run("Give me the gist of ReACT in 3 sentences")
    print(res)




    



