from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

message = [ SystemMessage(content="You are a helpful assistant."),
           HumanMessage(content="Tell me about langchain." ),
]
result = model.invoke(message)

message.append(AIMessage(content=result.content))
print(message)