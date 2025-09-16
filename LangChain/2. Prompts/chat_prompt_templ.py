from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


# -------Sometime LangChain does not work from any of these so use instead in both-------
chat_template = ChatPromptTemplate([
    SystemMessage(content="You are a helpful {domain} expert."),
    HumanMessage(content="Explain in simpler terms, what is {topic}."),
])

# chat_template = ChatPromptTemplate.from_messages([
#     (system_message := 'You are a helpful {domain} expert.'),
#     (human_message := 'Explain in simpler terms, what is {topic}.'),
# ])

prompt = chat_template.invoke({
    'domain': 'LangChain Developer',
    'topic': 'Most important concepts of LangChain'
})
print(prompt)