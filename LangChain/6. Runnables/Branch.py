from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv 
from langchain.schema.runnable import RunnableBranch,  RunnableParallel, RunnableSequence, RunnablePassthrough 


load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash") 

parser = StrOutputParser()

prompt1 = PromptTemplate(
    template = 'Write a detailed report on {topic}.',
    input_varibles = ['topic']
)
prompt2 = PromptTemplate(
    template = 'Summarise the following {text}.',
    input_varibles = ['text']
)

report_chain = RunnableSequence(prompt1, model, parser)


branch_chain = RunnableBranch(
    (lambda x: len(x.split())>200, RunnableSequence(prompt2, model,parser)),
    RunnablePassthrough()
)

final = RunnableSequence(report_chain, report_chain)

result = final.invoke({'topic':'Russia vs Ukrain'})

print(result)