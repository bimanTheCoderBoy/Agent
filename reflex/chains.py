from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
load_dotenv()


key=os.getenv("KEY")
if key is None:
    raise ValueError("API key not found. Please set the KEY environment variable.")
else:
    print("API key found and loaded successfully." + key)
llm = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=key,
    model_name="google/gemma-3-1b-it:free"
    
)
    
    
generation_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a Social media specialist who can generate posts for various platforms. and if critic ask for some improvement then you make a revised vertion of the previous one as per user request"),
        MessagesPlaceholder(variable_name="chat_history")
    ]
)

critic_prompt = ChatPromptTemplate.from_messages( 
    [
        ("system", "You are a Social media specialist who can critisize post and tell them some ways to improve it better in 3 points"),
        MessagesPlaceholder(variable_name="chat_history")
    ]
)


generation_chain= generation_prompt | llm

critic_chain = critic_prompt | llm