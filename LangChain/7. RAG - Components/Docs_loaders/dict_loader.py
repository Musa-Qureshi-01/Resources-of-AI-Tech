from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

loader = DirectoryLoader(
    path=r'C:\Users\musaq\OneDrive\Desktop\LangChain\7. RAG\Docs_loaders\Blogs',
    glob="*.pdf",
    loader_cls=PyPDFLoader
)




# ------- Normal load ----------
# docs = loader.load()
# print(len(docs), "documents loaded.")


# print(docs[0].page_content)
# print(docs[0].metadata)


# ---------  Lazy Load ----------

docs = loader.lazy_load()

for doc in docs:
    print(doc.metadata)