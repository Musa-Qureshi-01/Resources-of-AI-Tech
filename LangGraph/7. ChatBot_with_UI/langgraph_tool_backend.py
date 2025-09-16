from langgraph.graph import StateGraph , START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
import requests

load_dotenv()
model = ChatGoogleGenerativeAI(model='gemini-1.5-flash')

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):
    '''LLM mode thay may answeror request a tool call.'''
    messages = state['messages']
    response = model_with_tools.invoke(messages)
    return {'messages':[response]}



# ====================================== Tools ==========================================

search_tool = DuckDuckGoSearchRun()


# result = search_tool.run("latest Tesla stock price")
# print(result)

@tool
def calculator_tool(expression: str) -> str:
    """
    A simple calculator that evaluates mathematical expressions.
    Supports +, -, *, /, **, and parentheses.
    
    Example:
    - "2 + 3 * 4"
    - "(10 / 2) + 5"
    """
    try:
        result = eval(expression, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"
    
@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g., 'AAPL' for Apple, 'TSLA' for Tesla)
    using Alpha Vantage API.
    """
    api_key = "PA7BXR2RRQDXDTXC"  # ideally, load from .env
    url = (
        f"https://www.alphavantage.co/query"
        f"?function=TIME_SERIES_INTRADAY"
        f"&symbol={symbol}"
        f"&interval=5min"
        f"&apikey={api_key}"
    )
    r = requests.get(url)
    return r.json()


tools = [search_tool, get_stock_price, calculator_tool]
model_with_tools = model.bind_tools(tools)
# ================================= DataBase - SQLITE =====================================

conn = sqlite3.connect(database='chatbot.db', check_same_thread = False)

checkpointer = SqliteSaver(conn=conn)

# ======================= Graph ============================
tool_node = ToolNode(tools)

graph = StateGraph(ChatState)
graph.add_node('chat_node',chat_node)
graph.add_node('tools', tool_node)
graph.add_edge(START, 'chat_node')
graph.add_conditional_edges('chat_node', tools_condition)
graph.add_edge('tools', 'chat_node')
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

# ----------------------- DATABASE Testing ------------------------------------

# CONFIG = {'configurable':{'thread_id':'thread-2'}}

# response = chatbot.invoke(
#     {'messages': [HumanMessage(content='What is my name.')]},
#     config=CONFIG
# )
# print(response)

def retrieve_all_threads():
    all_threads = set()
    for check in checkpointer.list(None):
        all_threads.add(check.config['configurable']['thread_id'])

    return list(all_threads)

# for message_chunk, metadata in chatbot.stream(
#     ChatState(messages=[HumanMessage(content="What is the stock price of AAPL?")]),
#     config={"configurable": {"thread_id": "test-thread"}},
#     stream_mode="messages"
# ):
#     if message_chunk.content:
#         print(message_chunk.content, end=" ", flush=True)