import streamlit as st
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Load env files and initialize openai
load_dotenv()
openai_api_key = os.environ['OPENAI_API_KEY']

# Set up the OpenAI API Key
st.set_page_config(page_title="OpenAI Chatbot", page_icon=":robot:")

# Title of the application
st.title('Jay\'s Document-Based Chatbot :page_facing_up:')
st.subheader('WARNING: DO NOT ENTER SENSITVE INFORMATION')

# build the prompt, llm, output_parser. Chain them.
prompt = ChatPromptTemplate.from_messages([
    ("system", "{system_instructions}"),
    ("user", "{user_instructions}")
])
llm = ChatOpenAI(temperature=0, api_key=openai_api_key)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# streamlit box
with st.form("my_form"):
    system_instructions = st.text_area("Enter System instructions:", value='Hello!')
    user_instructions = st.text_area("Enter User Instructions", value="hello!")
    submitted = st.form_submit_button("Submit")
    if submitted:
        response = chain.invoke({
            "system_instructions": system_instructions,
            "user_instructions": user_instructions
            })
        st.info(response)
        