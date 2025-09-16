from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain.output_parsers import StructuredOutputParser , ResponseSchema
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id = "google/gemma-2-2b-it",
    task = "text_generation",
)

model = ChatHuggingFace(llm=llm)

schema = [
    ResponseSchema(name="fact-1", description="Fact - 1 about the topic"),
    ResponseSchema(name="fact-2", description="Fact - 2 about the topic"),  
    ResponseSchema(name="fact-3", description="Fact - 3 about the topic"),
]

parser = StructuredOutputParser.from_response_schemas(schema)


template = PromptTemplate(
    template = "Give  three facts about {topic} \n {format_instructions}",
    input_variables = ["topic"],
    partial_variables = {"format_instructions": parser.get_format_instructions()}
)

chain = template | model | parser

result = chain.invoke({'topic':"black holes"})

print(result)

# prompt =  template.format(topic="Black holes")
# result = model.invoke(prompt)   

# final_result = parser.parse(result.content)

# print(final_result)