import streamlit as st
import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
#from langchain.embeddings import OpenAIEmbeddings

# Set up page
st.set_page_config(page_title="API Troubleshooter", page_icon="🔧")
st.title("🔧 API Troubleshooting Assistant")
st.write("Paste API error messages and get step-by-step troubleshooting help.")

# Load API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.warning("⚠️ Please set your OpenAI API key in the environment or Streamlit secrets.")

# Define troubleshooting prompt
template = """
You are an expert API troubleshooter. A developer has encountered this error:

Error Message:
{error_message}

Explain clearly:
1. What the error usually means
2. The most likely root causes
3. Step-by-step troubleshooting actions
4. Example fix if possible
"""

prompt = PromptTemplate(
    input_variables=["error_message"],
    template=template
)

# Initialize LLM
llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0,
    openai_api_key=openai_api_key
)
troubleshoot_chain = LLMChain(llm=llm, prompt=prompt)

# Store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
user_input = st.chat_input("Paste your API error here...")
if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Run chain
    response = troubleshoot_chain.run(error_message=user_input)

    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Save to history
    st.session_state.chat_history.append((user_input, response))

# Display past conversation
for user_msg, bot_msg in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(bot_msg)

