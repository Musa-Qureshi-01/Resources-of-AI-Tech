from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash") 

st.title("Research Assistant")

user_query = st.text_input("Enter your research query:")

if st.button("Summarise"):
    result = model.invoke(user_query)
    st.write("Response:", result.content)