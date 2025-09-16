from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain.output_parsers import PydanticOutputParser
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from pydantic import BaseModel , Field

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id = "google/gemma-2-2b-it",
    task = "text_generation",
)

model = ChatHuggingFace(llm=llm)

class Person(BaseModel):
    name : str = Field(description='Name of the person')
    age : str = Field(gt=18 ,description='Age of the person')
    city : str = Field(description='City of the person')


parser = PydanticOutputParser(pydantic_object = Person)

template =PromptTemplate(
    template = " Generate the name , age and city of the the fictional {place} person \n {format_instructions}",
    input_variables = ['place'],
    partial_variables={'format_instructions': parser.get_format_instructions()}
)

# prompt = template.invoke({'place': 'Italian'})

# print(prompt)

# result = model.invoke(prompt)

# final_re = parser.parse(result)

# print(final_re)

chain = template | model | parser 

result = chain.invoke ({'place': 'Italian'})

print(result)