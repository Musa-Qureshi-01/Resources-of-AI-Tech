from langgraph.graph import StateGraph , START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()
model = ChatGoogleGenerativeAI(model='gemini-1.5-flash')

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):

    messages = state['messages']
    response = model.invoke(messages)
    return {'messages':[response]}


checkpointer = InMemorySaver()

graph = StateGraph(ChatState)
graph.add_node('chat_node',chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer = checkpointer)


# ====== This is not required here but I am test =======
# config = {
#     "configurable": {
#         "thread_id": "1"
#     }
# }

# for message_chunk , metadata in chatbot.stream(
#     {'messages':[HumanMessage(content='What is the recipe to make pasta.')]},
#     config=config,
#     stream_mode = 'messages'
# ):

# # print(type(stream))
#     if message_chunk.content:
#         print(message_chunk.content, end=" ", flush=True)

