from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
from transformers import pipeline
from dotenv import load_dotenv
import os

os.environ['HF_HOME'] = 'D:/HuggingFace_cache'

# 1. Create a text-generation pipeline with all your parameters
hf_pipeline = pipeline(
    task="text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    max_new_tokens=250,
    temperature=0.5
)

# 2. Instantiate HuggingFacePipeline with the pipeline object
llm = HuggingFacePipeline(pipeline=hf_pipeline)

model = ChatHuggingFace(llm=llm)

result = model.invoke("What is the capital of France?")

print(result.content)