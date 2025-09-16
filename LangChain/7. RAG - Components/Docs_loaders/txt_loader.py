from langchain_community.document_loaders import TextLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

loader = TextLoader("C:/Users/musaq/OneDrive/Desktop/LangChain/7. RAG/Docs_loaders/txt.txt", encoding="utf-8")
docs = loader.load()
print(type(docs))
print(len(docs))
print(type(docs[0]))

print(docs[0].metadata)
print(docs[0].page_content)

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash") 

parser = StrOutputParser()

prompt = PromptTemplate(
    template = 'Write a summary for the peom of - \n {poem}.',
    input_varibles = ['poem']
)

chain = prompt | model | parser 

result = chain.invoke({'poem':docs[0].page_content})

print(result)