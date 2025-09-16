from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv()

# Use the embedding model, not the chat model
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

docs = [
    "Paris is the capital of France, known for the Eiffel Tower and its vibrant art scene.",
    "Berlin is the capital of Germany, famous for its history and the Brandenburg Gate.",
    "Madrid is the capital of Spain, renowned for its lively plazas and the Prado Museum.",
    "Rome is the capital of Italy, home to ancient landmarks like the Colosseum and the Vatican.",
    "London is the capital of the United Kingdom, known for Big Ben, Buckingham Palace, and diverse culture.",
    "Lisbon is the capital of Portugal, celebrated for its historic trams and pastel-colored buildings."
]
# query = "Tell me about Lisbon."
query = input("Enter your City you want to know about : ")

# Get embeddings
docs_embeddings = embeddings.embed_documents(docs)
query_embedding = embeddings.embed_query(query)


# Compute cosine similarity
scores = cosine_similarity([query_embedding], docs_embeddings)[0]

# print("Cosine Similarities:", cosine_similarities)
# print("Most similar doc:", docs[np.argmax(cosine_similarities)])

index, score = (sorted(list(enumerate(scores)),key = lambda x: x[1])[-1])


print(query)
print(docs[index])
print("Cosine similarity score:", score)
