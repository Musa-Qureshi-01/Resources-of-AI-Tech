from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from langchain_community.document_loaders import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

from dotenv import load_dotenv

load_dotenv()

# Google Gemini model
model = ChatGoogleGenerativeAI(model='gemini-1.5-flash')

# HuggingFace embeddings
instructor_embeddings = HuggingFaceEmbeddings(model_name="hkunlp/instructor-base")

vectordb_file_path = "faiss_index"


def vector_db():
    loader = CSVLoader(file_path="codebasics_faqs.csv", source_column='prompt')
    data = loader.load()
    vectordb = FAISS.from_documents(documents=data, embedding=instructor_embeddings)
    vectordb.save_local(vectordb_file_path)  # ✅ correct save method


def get_chain():
    # ✅ FIX: allow_dangerous_deserialization=True required in latest langchain
    vectordb = FAISS.load_local(
        vectordb_file_path,
        instructor_embeddings,
        allow_dangerous_deserialization=True
    )

    # Use retriever with a score threshold
    retriever = vectordb.as_retriever(search_kwargs={"score_threshold": 0.7})

    prompt_template = """Given the following context and a question, generate an answer based on this context only.
    In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
    If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

    CONTEXT: {context}

    QUESTION: {question}"""

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=['context', 'question']
    )

    chain = RetrievalQA.from_chain_type(
        llm=model,
        chain_type="stuff",
        retriever=retriever,
        input_key="query",
        return_source_documents=True,
        chain_type_kwargs={'prompt': prompt}
    )

    return chain


if __name__ == '__main__':
    chain = get_chain()
    result = chain.invoke("Do you provide internship? Do you have EMI options?")
    print(result)
