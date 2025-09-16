from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv 
from langchain.schema.runnable import RunnableSequence


load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash") 


prompt1 = PromptTemplate(
    template = 'Write a joke on {topic}.',
    input_varibles = ['topic']
)

prompt2 = PromptTemplate(
    template = 'Explain your joke - {text}.',
    input_varibles = ['text']
)

parser = StrOutputParser()

chain = RunnableSequence(prompt1, model, parser, prompt2, model, parser)

print(chain.invoke({'topic':"AI"}))