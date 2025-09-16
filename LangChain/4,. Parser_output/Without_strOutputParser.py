from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser   
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash") 

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

prompt1 =  template1.invoke({'topic': 'Black holes'})

result1 = model.invoke(prompt1)
print("Detailed Report:\n", result1)

prompt2 = template2.invoke({'text': result1.content})
result2 = model.invoke(prompt2)
print("Summary Report:\n", result2)