from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv 
from langchain.schema.runnable import RunnableParallel, RunnableSequence 


load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash") 

parser = StrOutputParser()

prompt1 = PromptTemplate(
    template = "Generate a tweet (X post) about {subject} (in points).",
    input_variables = ['subject']
)
prompt2 = PromptTemplate(
    template = "Generate a LinkedIn post about {subject} (in points).",
    input_variables = ['subject']
)

parallel_chain = RunnableParallel({
    'tweet': RunnableSequence(prompt1, model, parser),
    'LinkedIn': RunnableSequence(prompt2, model, parser)
})

result = parallel_chain.invoke({'subject':'LangChain is heart for GenAI'})

print(result)