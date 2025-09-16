from typing import TypedDict, Annotated, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash")

# schema

class Review(TypedDict):
    title: Annotated[str, "title of the review"]
    # summary: str
    summary: Annotated[Optional[str], "summary of the review"]
    sentiment: Annotated[str, "sentiment of the review, e.g., positive, negative, neutral"]

structured_model = model.with_structured_output(
    Review
)

result = structured_model.invoke(
    '''
As a developer, I see LangChain as a powerful framework that simplifies building LLM-powered applications by providing tools for chaining prompts, managing memory, and integrating with APIs.
Its modular design makes it easy to connect different AI models and data sources without reinventing the wheel.
While it can feel complex at first, especially with its many abstractions, it greatly speeds up development for chatbots, agents, and AI workflows.
For production apps, its flexibility and wide ecosystem support make it a strong choice for scaling AI solutions.
'''
)

print(result)
print(result['title'])
print(result['summary']) 
print(result['sentiment'])  