from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv 
from langchain.schema.runnable import RunnableParallel, RunnableSequence, RunnablePassthrough 


load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash") 

parser = StrOutputParser()


prompt1 = PromptTemplate(
    template = 'Write a joke on {topic}.',
    input_varibles = ['topic']
)

prompt2 = PromptTemplate(
    template = 'Explain your joke - {text}.',
    input_varibles = ['text']
)

joke_chain = RunnableSequence(prompt1, model, parser)

para_chain = RunnableParallel({
    'joke': RunnablePassthrough(),
    'explanation': RunnableSequence(prompt2, model, parser)
})

final = RunnableSequence(joke_chain,  para_chain)

result = final.invoke({'topic':'AI'})

print(result)