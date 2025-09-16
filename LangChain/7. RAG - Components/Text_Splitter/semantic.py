from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from dotenv import load_dotenv
load_dotenv()
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


text = '''
Climate change is one of the biggest challenges of the 21st century. Rising global temperatures, melting ice caps, and extreme weather events are threatening ecosystems and human life. Governments and organizations worldwide are working on renewable energy adoption, sustainable agriculture, and eco-friendly urban planning to reduce carbon emissions and protect the planet for future generations.

In the field of technology, Artificial Intelligence (AI) is being increasingly applied to solve environmental problems. Machine learning models can predict weather patterns, optimize energy consumption, and even detect deforestation from satellite images. By combining sustainability practices with AI-powered tools, humanity has a better chance to mitigate the effects of climate change and build a greener future.
'''

text_splitter = SemanticChunker(
    embeddings,
    breakpoint_threshold_type="standard_deviation",
    breakpoint_threshold_amount=1
)


docs = text_splitter.create_documents([text])

print(len(docs))
print(docs)