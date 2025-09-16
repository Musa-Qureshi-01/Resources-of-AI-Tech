# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv


# load_dotenv()
# model = ChatGoogleGenerativeAI(model="gemini-1.5-flash") 

# chat_history = []

# while True:
#     user_query = input("You: ")
#     chat_history.append(user_query)
#     if user_query.lower() == "exit":
#         break
#     result = model.invoke(user_query)
#     chat_history.append(result.content)
#     print("AI Chatbot: ", result.content,"\n")

# print(chat_history) 


# ------------------  For Saving Chat History ------------------

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

chat_history = [
    SystemMessage(content="You are a helpful assistant."),
    # HumanMessage(content="Tell me about langchain.")
]

while True:
    user_query = input("You: ")
    if user_query.lower() == "exit":
        break

    chat_history.append(HumanMessage(content=user_query))
    result = model.invoke(chat_history)
    chat_history.append(AIMessage(content=result.content))

    print("AI Chatbot:", result.content, "\n")

print("\nFull Chat History:")
for msg in chat_history:
    role = "You" if isinstance(msg, HumanMessage) else "AI"
    print(f"{role}: {msg.content}")

# print(chat_history) 