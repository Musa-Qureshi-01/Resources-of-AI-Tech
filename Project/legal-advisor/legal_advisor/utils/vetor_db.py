from langchain.vectorstores import chroma 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.docstore.document import Document
from dotenv import load_dotenv 
import os 
load_dotenv()

class Embed :
    def __init__(self , docs: list, api: str =  None ):
        self.docs = docs 
        self.google_api_key  = api or os.getenv("GOOGLE_API_KEY")

    def embedding(self) -> str :
        model = GoogleGenerativeAIEmbeddings(
            model= "gemini-embedding-001" , 
            google_api_key= self.google_api_key
            
        )
        
