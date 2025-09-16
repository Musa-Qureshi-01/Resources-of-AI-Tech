from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash") 

parser = StrOutputParser()

prompt = PromptTemplate(
    template = 'Answer the following questions \n {question} from the following text - \n {text}.',
    input_variables = ['question','text']
)

url = 'https://www.flipkart.com/apple-macbook-air-m4-24-gb-512-gb-ssd-macos-sequoia-mc6c4hn-a/p/itm80c9934341eec?pid=COMH9ZWQDEGH4FZZ&lid=LSTCOMH9ZWQDEGH4FZZLLISIR&marketplace=FLIPKART&q=macbook+air+m4+pro+max&store=6bo%2Fb5g&srno=s_1_4&otracker=AS_Query_OrganicAutoSuggest_3_12_na_na_na&otracker1=AS_Query_OrganicAutoSuggest_3_12_na_na_na&fm=search-autosuggest&iid=4fbb99eb-6da5-4466-a8a0-c4f51652305f.COMH9ZWQDEGH4FZZ.SEARCH&ppt=sp&ppn=sp&ssid=6hifrfor1c0000001755499864175&qH=4b94aa8766bf9d81'

loader = WebBaseLoader(url)

docs = loader.load()

chain = prompt | model | parser 

result = chain.invoke({'question':'What is Specifications of the product ?','text':docs[0].page_content})

print(result)