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

prompt = PromptTemplate(
    template = ' Generate 5 interesting facts about {topic}.',
    input_varibles = ['topic']
)

parser = StrOutputParser()

chain = prompt | model | parser 

result = chain.invoke({'topic':"Philosphy"})

print(result)

chain.get_graph().print_ascii()