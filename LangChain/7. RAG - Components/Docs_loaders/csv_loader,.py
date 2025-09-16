from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(file_path=r'C:\Users\musaq\OneDrive\Desktop\LangChain\7. RAG - Concepts\Docs_loaders\train.csv')
docs = loader.load()

print(len(docs))
print(docs[10])

