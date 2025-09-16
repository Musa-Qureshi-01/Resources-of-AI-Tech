from langgraph.graph import StateGraph , START, END
from typing import TypedDict, Annotated, Optional
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3
from langchain.chains import LLMChain
from duckduckgo_search import DDGS
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_experimental.tools import PythonREPLTool
from langchain_community.tools import GoogleSearchRun
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
import requests
from langchain_google_community import GoogleSearchAPIWrapper, GoogleSearchRun
import os
os.environ["USER_AGENT"] = "my-rag-bot/1.0"

load_dotenv()
model = ChatGoogleGenerativeAI(model='gemini-2.5-pro')

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    chat_name: Optional[str]


def chat_node(state: ChatState):
    messages = state['messages']

    if not state.get('chat_name') and messages and isinstance(messages[0], HumanMessage):
        first_message_content = messages[0].content
        chat_name = first_message_content[:25].strip()
        state['chat_name'] = chat_name

    response = model_with_tools.invoke(messages)
    return {'messages':[response]}



# ====================================== Tools ==========================================

search_tool = DuckDuckGoSearchRun()

python_repl_tool = PythonREPLTool()


search_wrapper = GoogleSearchAPIWrapper()
google_search_tool = GoogleSearchRun(api_wrapper=search_wrapper)

@tool
def web_loader_tool(url: str) -> str:
    """
    Loads the content of a webpage from a given URL.
    Use this tool to get specific information from a known webpage,
    like a syllabus or a news article.
    """
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()

        # Return a summary or a part of the document to avoid hitting context limits
        return docs[0].page_content[:2000] 
    except Exception as e:
        return f"An error occurred while loading the webpage: {str(e)}"

@tool
def career_guidance_tool(query: str, field_of_study: str) -> str:
    """
    Offers career advice and information on job opportunities, required skills,
    and higher education paths related to a specific field of study.

    The knowledge base for this tool is specific to industries and
    opportunities in and around Jammu and Kashmir.

    Args:
        query: The student's question about their career.
        field_of_study: The student's major (e.g., "Computer Science", "Medicine").
    """
    try:
        search_query = f"{query} for {field_of_study} in Jammu and Kashmir"
        results = DDGS().text(keywords=search_query, region='in-en', max_results=5)
        
        if not results:
            return "No relevant information found for your query. Please try rephrasing."

        search_results_text = ""
        for i, result in enumerate(results):
            search_results_text += f"Result {i+1}: {result['title']}\n"
            search_results_text += f"Source: {result['href']}\n"
            search_results_text += f"Summary: {result['body']}\n\n"

        prompt = PromptTemplate(
            input_variables=["student_query", "search_results"],
            template="""You are a helpful career counselor for students in Jammu and Kashmir. 
            A student has asked the following question: "{student_query}".

            You have gathered the following information from various online sources:
            {search_results}

            Based on this information, provide a concise and helpful career guidance response. 
            Focus on job opportunities, required skills, or higher education options in J&K.
            If the information is not sufficient, state that you need more details.
            """
        )

        model = ChatGoogleGenerativeAI(model='gemini-1.5-flash', temperature=0.1)
        llm_chain = LLMChain(llm=model, prompt=prompt)
        guidance_response = llm_chain.run(student_query=query, search_results=search_results_text)
        
        return guidance_response

    except Exception as e:
        return f"An error occurred while providing career guidance: {str(e)}"


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


tools = [search_tool, get_stock_price, calculator_tool, python_repl_tool, web_loader_tool, google_search_tool, career_guidance_tool]
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





def retrieve_all_threads():
    all_threads = set()
    for check in checkpointer.list(None):
        all_threads.add(check.config['configurable']['thread_id'])
        

    return list(all_threads)

