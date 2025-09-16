from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser   
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id = "google/gemma-2-2b-it",
    task = "text_generation",
)

model = ChatHuggingFace(llm=llm)
#  1st prompt -> detailed report 

template1 = PromptTemplate(
    template = "Write detailed report on {topic}.",
    input_variables = ["topic"]
)

# 2nd prompt -> summary report

template2 = PromptTemplate(
    template = "Write detailed report on {text}.",
    input_variables = ["text"]
)


parser = StrOutputParser()

chain = template1 | model | parser | template2 | model | parser
result = chain.invoke({'topic': 'Black holes'})

print(result)