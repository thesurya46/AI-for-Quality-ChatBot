import os
import gradio as gr
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

# Set environment for OpenRouter (pretending to be OpenAI)
os.environ["OPENAI_API_KEY"] = "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"
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"  # Not always supported

MODEL_NAME = "mistralai/mistral-7b-instruct:free"

# Template
template = """
"Hello! 👋 I’m your AI Assistant for Quality Management — developed by a group of passionate university students.
I'm here to help you explore, improve, and solve quality-related challenges in your organization. How can I assist you today?"
{chat_history}
User: {user_message}
Chatbot:
"""

prompt = PromptTemplate(
    input_variables=["chat_history", "user_message"],
    template=template
)

memory = ConversationBufferMemory(memory_key="chat_history")

# This might not work depending on whether LangChain's OpenAI wrapper supports OpenRouter (experimental)
llm_chain = LLMChain(
    llm=ChatOpenAI(
        temperature=0.5,
        model_name=MODEL_NAME,
        openai_api_base=os.environ["OPENAI_BASE_URL"],  # Try this
        openai_api_key=os.environ["OPENAI_API_KEY"],
    ),
    prompt=prompt,
    verbose=True,
    memory=memory,
)

# Response function
def get_text_response(user_message, history):
    try:
        return llm_chain.predict(user_message=user_message)
    except Exception as e:
        return f"Error: {str(e)}"

# Gradio UI
demo = gr.ChatInterface(get_text_response)
demo.launch(share=True)