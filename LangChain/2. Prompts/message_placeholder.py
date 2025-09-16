from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage

# ------ Chta Template -------
chat_template = ChatPromptTemplate([
    ('system', "You are a helpful customer support agent."),
    MessagesPlaceholder(variable_name="chat_history"),
    ('human', '{query}')
])

chat_history = []


# ------ Load Chat History -------

with open("./Prompts/chat_history.txt") as f:
    chat_history.extend(f.readlines())

print(chat_history)

# ------ Create Prompt -------

prompt = chat_template.invoke({
    'chat_history': chat_history,
    'query': HumanMessage(content="Where is my refund.")
})

print(prompt)