from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small", chunk_size=1, dimension=64)

# For a single query
# result = embeddings.embed_query("What is the capital of France?")

docs = [
    "Paris is the capital of France.",
    "Berlin is the capital of Germany.",   
    "Madrid is the capital of Spain.",
    "Rome is the capital of Italy.",
    "London is the capital of the United Kingdom.",
    "Lisbon is the capital of Portugal.",
]

result = embeddings.embed_documents(docs)

print(str(result))