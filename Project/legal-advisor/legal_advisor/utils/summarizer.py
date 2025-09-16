from langchain.chains.summarize import load_summarize_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.docstore.document import Document
from dotenv import load_dotenv
import os

load_dotenv()

class Summary:
    def __init__(self, docs: list, api: str = None):
        self.docs = docs 
        self.google_api_key = api or os.getenv("GOOGLE_API_KEY") 
    
    def summarize(self, chain_type: str = "map_reduce") -> str:
        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=self.google_api_key
        )

        summary_chain = load_summarize_chain(model, chain_type=chain_type)
        summary_docs = [Document(page_content=chunk) for chunk in self.docs]

        try:
            return summary_chain.invoke(summary_docs)
        except Exception as e:
            raise RuntimeError(f"Summarization failed: {str(e)}")
