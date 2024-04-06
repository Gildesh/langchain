from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader, TextLoader
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import tiktoken, textwrap, urllib
from time import monotonic

load_dotenv()
def variables_init():
    OPENAI_API_KEY = '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'
    model_max_tokens = 4097
    verbose = True
    model_name = "gpt-3.5-turbo"
    prompt_template = """Write a concise summary of the following:
    {text}
    CONSCISE SUMMARY IN ENGLISH:"""
    url = "https://raw.githubusercontent.com/mauricio-seiji/Dataset-news-articles-pt-br/main/ciencia%20e%20tecnologia/30.txt"
    url = "https://raw.githubusercontent.com/mauricio-seiji/Dataset-news-articles-pt-br/main/ciencia%20e%20tecnologia/22.txt"
    choice = 'Character'
    return OPENAI_API_KEY, model_max_tokens, verbose, model_name, prompt_template, url, choice
def web_text(url):
    news_article = urllib.request.urlopen(url).read().decode("utf-8")
    return news_article
def num_tokens_from_string(string: str, encoding_name: str) -> int:    
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
def splitter_init(choice):   
   if choice == 'Character':
       text_splitter = CharacterTextSplitter.from_tiktoken_encoder(model_name=model_name)
   else:
      text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000,chunk_overlap=20,length_function=len,is_separator_regex=False,)
   return text_splitter
def file_text(filename):
   with open(filename, "r",  encoding='utf-8') as file:
       file_contents = file.read()
   return file_contents

OPENAI_API_KEY, model_max_tokens, verbose, model_name, prompt_template, url, choice = variables_init()
news_article = web_text(url)
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name=model_name)
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
file_contents = file_text("adventures.txt")
text_splitter = splitter_init('Character')

web_texts = text_splitter.split_text(news_article)
file_texts = text_splitter.split_text(file_contents)
file_docs = [Document(page_content=t) for t in file_texts]
web_docs = [Document(page_content=t) for t in web_texts]
web_tokens = num_tokens_from_string(news_article, model_name)
file_tokens = num_tokens_from_string(news_article, model_name)
print('file tokens hain itne')
print(file_tokens)
def chain_run(docs, tokens):
    if tokens < model_max_tokens:
        chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt, verbose=verbose)
        print('Stuff Chali')
    else:
        chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=prompt, combine_prompt=prompt, verbose=verbose)
        print('Map Reduce Chali')        
    summary = chain.run(docs)
    return summary, chain

start_time = monotonic()
print('File')
file_summary, file_chain = chain_run(file_docs, file_tokens)
print('Web')
web_summary, web_chain = chain_run(web_docs, web_tokens)

print(f"Chain type: {file_chain.__class__.__name__}")
print(f"Run time: {monotonic() - start_time}")
print(f"File Summary: {textwrap.fill(file_summary, width=100)}")
print(f"Web Summary: {textwrap.fill(web_summary, width=100)}")
