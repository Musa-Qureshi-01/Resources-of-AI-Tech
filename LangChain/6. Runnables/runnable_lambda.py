from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv 
from langchain.schema.runnable import RunnableLambda,  RunnableParallel, RunnableSequence, RunnablePassthrough 


load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash") 

parser = StrOutputParser()

prompt = PromptTemplate(
    template = 'Write a joke on {topic}.',
    input_varibles = ['topic']
)

def word_count(text):
    return len(text.split())

joke_chain = RunnableSequence(prompt, model, parser)

para_chain = RunnableParallel({
    'joke': RunnablePassthrough(),
    'word_count': RunnableLambda(word_count)
})

final = RunnableSequence(joke_chain,  para_chain)
result = final.invoke({'topic':'Habits'})

print(result)