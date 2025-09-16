import streamlit as st
from helper import vector_db, get_chain

st.title("FAQ's Bot 🌱")

st.subheader("📂 Knowledge Base")
btn = st.button("Create KnowledgeBase")
if btn:
    st.success("KnowledgeBase created successfully!")

question = st.text_input("Question: ")

if question:
    chain = get_chain()
    result = chain(question)
    st.subheader("Answer")
    st.write(result['result'])
    st.subheader("Internal Model Work.")
    st.write(result)
    # btn = st.button("Enter")
    # if btn:
    #     st.subheader("Answer")
    #     st.write(result['result'])
    #     st.subheader("Internal Model Work.")
    #     st.write(result)



st.text("Made by ©️ Musa Qureshi. Ⓜ️")