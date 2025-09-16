from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.output_parsers import JsonOutputParser  
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id = "google/gemma-2-2b-it",
    task = "text_generation",
)

model = ChatHuggingFace(llm=llm)


parser = JsonOutputParser()

template = PromptTemplate(
    template = " Give the name , age and city of the the fictional person \n {format_instructions}",
    input_variables = ["format_instructions"],
    partial_variables = {"format_instructions": parser.get_format_instructions()}
)

# prompt = template.format()
# result = model.invoke(prompt)

# final_result = parser.parse(result.content)
chain = template | model | parser 

result = chain.invoke({})

print(result)