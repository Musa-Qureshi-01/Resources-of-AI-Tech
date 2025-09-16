from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.runnable import RunnableParallel

load_dotenv() 

model1 = ChatGoogleGenerativeAI(model="gemini-1.5-flash") 
llm = HuggingFaceEndpoint(
    repo_id = "google/gemma-2-2b-it",
    task = "text_generation",
)

model2 = ChatHuggingFace(llm=llm) 


prompt1 = PromptTemplate(
    template = 'Generate short and simple notes from the following text \n {text}',
    input_variables = ['text']
)
prompt2 = PromptTemplate(
    template = 'Generate 5 questions and answers (quiz) on the \n {text}',
    input_variables = ['text']
)
prompt3 = PromptTemplate(
    template = 'Merge the notes and quiz into a single document \n notes -> {notes} and quiz -> {quiz}.',
    input_variables = ['notes','quiz']
)

parser = StrOutputParser()

para_chain =  RunnableParallel({
    'notes': prompt1 | model1 | parser,
    'quiz' : prompt2 | model2 | parser
})

merge_chain = prompt3 | model2 | parser 

chain = para_chain | merge_chain

text = """
Purpose – LangChain is an open-source framework for building applications powered by Large Language Models (LLMs) like OpenAI GPT, Google Gemini, Anthropic Claude, Hugging Face models, or local models.

Modularity – Provides building blocks like prompts, chains, agents, tools, and memory to structure complex AI workflows.

Prompt Templates – Create reusable and dynamic instructions with variables instead of hardcoding text.

Chains – Link multiple components (e.g., prompt → LLM → parser) to run in sequence as one pipeline.

Memory – Store conversation history so the model can remember previous interactions.

Agents – Allow the LLM to decide and use different tools dynamically to complete tasks.

Tool Integrations – Supports APIs, databases (SQL, MongoDB), vector stores (Pinecone, FAISS, Chroma, Weaviate), and external services like Wikipedia or SerpAPI.

RAG (Retrieval-Augmented Generation) – Retrieve relevant documents from a vector database and feed them to the LLM for accurate, context-aware answers.

Structured Output – Supports output formatting with JSON or Pydantic models to ensure reliable, machine-readable responses.

Use Cases – Chatbots, document Q&A, research assistants, AI coding helpers, automated content creation, and autonomous agents.

Best Practices – Use explicit instructions in prompts, chunk large documents, cache results to save API calls, add retries for reliability, and test across models.

Flexibility – Easily switch between different LLM providers without rewriting application logic.

Ecosystem – Rapidly growing, with community-driven integrations and continuous feature updates.

Deployment Ready – Supports streaming, API wrapping, and integration into production environments
"""

result = chain.invoke({'text':text})

print(result)

chain.get_graph().print_ascii()