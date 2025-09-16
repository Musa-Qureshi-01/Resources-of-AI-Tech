from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash") 

parser = StrOutputParser()
loader = PyPDFLoader(r'C:\Users\musaq\OneDrive\Desktop\LangChain\7. RAG\Docs_loaders\Research On How to build Tech Blog.pdf')

docs = loader.load()

print(len(docs))

print(docs[0].page_content)
print(docs[0].metadata)