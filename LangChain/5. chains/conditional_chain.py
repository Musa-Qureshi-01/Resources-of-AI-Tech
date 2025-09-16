from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.runnable import RunnableBranch, RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field 
from typing import Literal



load_dotenv() 

model1 = ChatGoogleGenerativeAI(model="gemini-1.5-flash") 
llm = HuggingFaceEndpoint(
    repo_id = "google/gemma-2-2b-it",
    task = "text_generation",
)

model2 = ChatHuggingFace(llm=llm) 

parser = StrOutputParser()
class Feedback(BaseModel):
    sentiment: Literal['positive', 'negative'] = Field(description='Give the sentiment of feedback.')

parser2 = PydanticOutputParser(pydantic_object=Feedback)
prompt1 = PromptTemplate(
    template="""
Classify the sentiment of the following feedback text into "positive" or "negative".
Return only a valid JSON object that strictly follows this format: {instruction_format} , Feedback: {feedback}
""",
    input_variables=['feedback'],
    partial_variables={'instruction_format': parser2.get_format_instructions()}
)

classifier_chain = prompt1 | model2 | parser2


prompt2 = PromptTemplate(
    template = 'Write an appropriate response to positive feedback \n {feedback}.',

    input_variables = ['feedback']
)
prompt3 = PromptTemplate(
    template = 'Write an appropriate response to negative feedback \n {feedback}.',
    input_variables = ['feedback']
)



branch_chain = RunnableBranch(
    (lambda x:x.sentiment == 'positive', prompt2 | model2 | parser),
    (lambda x:x.sentiment == 'negative', prompt3 | model2 | parser),
    RunnableLambda(lambda x: "Could not find sentiment.")
)

# result = classifier_chain.invoke({'feedback':"This lpatop is terrible."}).sentiment

# print(result)

chain = classifier_chain | branch_chain 

result = chain.invoke({'feedback':'This mobile phone is wonderful - iphone16 pro'})

print(result)

chain.get_graph().print_ascii()