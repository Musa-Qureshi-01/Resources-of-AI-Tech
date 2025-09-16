from langchain_huggingface import HuggingFaceEmbeddings  

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

text = "The capital of France is Paris."

# For a single query
# vector = embedding.embed_query(text)

docs = [
    "Paris is the capital of France.",
    "Berlin is the capital of Germany.",   
    "Madrid is the capital of Spain.",
    "Rome is the capital of Italy.",
    "London is the capital of the United Kingdom.",
    "Lisbon is the capital of Portugal.",
]

vector = embedding.embed_documents(docs)

print(str(vector))