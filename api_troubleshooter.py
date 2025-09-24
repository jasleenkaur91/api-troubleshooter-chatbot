import os
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

# Load API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Define prompt
template = """
You are an expert API troubleshooter. A developer has encountered this error:

Error Message:
{error_message}

Explain:
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
llm = ChatOpenAI(model_name="gpt-4", temperature=0, openai_api_key=openai_api_key)

# Create chain
troubleshoot_chain = LLMChain(llm=llm, prompt=prompt)

# CLI Loop
print("🔧 API Troubleshooting Assistant")
print("Type 'exit' to quit.\n")

while True:
    error_input = input("Paste API error: ")
    if error_input.lower() in ["exit", "quit"]:
        print("Goodbye 👋")
        break

    response = troubleshoot_chain.run(error_message=error_input)
    print("\n💡 Suggestion:\n")
    print(response)
    print("-" * 50)

