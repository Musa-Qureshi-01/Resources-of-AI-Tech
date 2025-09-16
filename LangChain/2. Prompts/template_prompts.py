from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import PromptTemplate, load_prompt


load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash") 

st.title("Research Assistant")

paper_input = st.selectbox("Select Research Paper Name", ["Attention is All You Need", "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding", "GPT-3: Language Models are Few-Shot Learners", "Diffusion Models Beat GANs on Image Synthesis", "DALL-E 2: A New Era of AI-Generated Images" ])

style_input = st.selectbox("Select Style", ["Formal", "Informal", "Technical", "Conversational", "Descriptive","Mathematical"])

length_input = st.selectbox("Select Length", ["Very Short","Short", "Medium", "Long", "Very Long"])

# # --------------------------- template --------------------------------------- 

# template = PromptTemplate(
#     template = """
# Please summarize the research paper titled "{paper_input}" with the following specifications: 
# Explanation Style: {style_input} 
# Explanation Length: ngth: {length_input} 
# 1. Mathematical Details:
#     - Include relevant mathematical equations if present in the paper.
# Explain the mathematical concepts using simple, intuitive code snippets where applicable.
# 2. Analogies: 
#     - Use relatable analogies to simplify complex ideas. 
# If certain information is not available in the paper, respond with: "Insufficient information available" instead of guessing.
# Ensure the summary is clear, accurate, and aligned with the provided style and length.
# """,
# input_variables=["paper_input", "style_input", "length_input"]
# )


template = load_prompt("template.json")


# #placeholders
# prompt = template.invoke ({
#     "paper_input": paper_input,
#     "style_input": style_input,
#     "length_input": length_input
# })

# if st.button("Summarise"):
#     result = model.invoke(prompt)
#     st.write("Response:", result.content)

#  ------------------ Chaining ---------------------------


if st.button("Summarise"):
    chain = template | model
    result = chain.invoke({
        "paper_input": paper_input,
        "style_input": style_input,
        "length_input": length_input
    })
    st.write(result.content)
