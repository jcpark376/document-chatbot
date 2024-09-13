import streamlit as st
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from prompt_hub.example_lab_notebook import example_lab_notebook

# load env files and initialize openai
load_dotenv()
openai_api_key = os.environ['OPENAI_API_KEY']

# set up the OpenAI API Key
st.set_page_config(page_title="OpenAI Chatbot", page_icon=":robot:")

# title of the application
st.title('Jay\'s Document-Based Chatbot :page_facing_up:')
st.subheader('WARNING: DO NOT ENTER SENSITVE INFORMATION')

current_system_instructions = '''
You are a helpful assistant responsible for writing the Materials and Methods section of a biomedical journal article. Your writing should be:

- Factual, concise, and technically accurate.
- Structured to reflect typical conventions in scientific writing (e.g., describing materials, equipment, experimental procedures, and analysis methods in logical order).
- Based only on the information provided in the source document, without making any assumptions, adding external information, or interpreting data beyond the details in the document.
- Avoiding personal opinions, speculative statements, or inferred details not explicitly stated in the document.

If any key information is missing, note it without attempting to fill gaps.

Document: {document}
'''

# build the prompt, llm, output_parser. Chain them.
prompt = ChatPromptTemplate.from_messages([
    ("system", current_system_instructions),
    ("user", "{user_instructions}")
])
llm = ChatOpenAI(temperature=0, api_key=openai_api_key)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# display current system instructions
st.subheader("Current System Instructions")
st.markdown(current_system_instructions)

# streamlit box
with st.form("my_form"):
    document = st.text_area("document", value=example_lab_notebook)
    user_instructions = st.text_area("user_instructions", value="Write the materials and methods section.")
    submitted = st.form_submit_button("Submit")
    if submitted:
        response = chain.invoke({
            "document": document,
            "user_instructions": user_instructions
            })
        st.info(response)
        