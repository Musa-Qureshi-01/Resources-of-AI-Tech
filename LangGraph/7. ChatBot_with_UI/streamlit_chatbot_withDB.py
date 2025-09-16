import streamlit as st
from langgraph_database_backend import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid

# ******************************* Utility Functions ********************************

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

# def load_conversation(thread_id):
#     return chatbot.get_state(config={'configurable':{'thread_id':thread_id}}).values['messages']
def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])
    
#     return messages


# ******************************** Session SetUp ************************************

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()
add_thread(st.session_state['thread_id'])

# ********************************** SideBar UI *************************************
st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads']:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role':role, 'content':msg.content})
        st.session_state['message_history'] = temp_messages

# ************************************ Main UI **************************************

# CONFIG = {'configurable':{'thread_id':st.session_state['thread_id']}}

CONFIG = {
    'configurable':{'thread_id':st.session_state['thread_id']},
    "metadat":{
        'thread_id':st.session_state['thread_id']
    },
    "run_name":"chat_turn"
}

user_input = st.chat_input('Type here')

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

if user_input:
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # response = chatbot.invoke({'messages':[HumanMessage(content=user_input)]}, config=CONFIG)
    # ai_message = response['messages'][-1].content
    # st.session_state['message_history'].append({'role':'assistant','content':ai_message})
    # with st.chat_message('assistant'):
    #     st.text(ai_message)
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages':[HumanMessage(content=user_input)]},
                config = CONFIG,
                stream_mode = 'messages'
            )
        )
    st.session_state['message_history'].append({'role':'assistant', 'content':ai_message})