from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(r'C:\Users\musaq\OneDrive\Desktop\LangChain\7. RAG - Concepts\Text_Splitter\Research On How to build Tech Blog.pdf')

docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 700,
    chunk_overlap = 0,
    # separator = ''
)

result = splitter.split_documents(docs)

print(result[0])
print(len(result[0].page_content))
print(result[0].page_content)
print(result[0].metadata)