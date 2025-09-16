from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(r'C:\Users\musaq\OneDrive\Desktop\LangChain\7. RAG - Concepts\Text_Splitter\Research On How to build Tech Blog.pdf')

docs = loader.load()

splitter = CharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap = 0,
    separator = ''
)

result = splitter.split_documents(docs)

print(result[0])
print(len(result[0].page_content))
print(result[0].page_content)
print(result[0].metadata)