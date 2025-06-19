from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.agents import create_react_agent, tool
from langchain_tavily import TavilySearch
from langchain import hub
import datetime
import os

load_dotenv()
key = os.getenv("KEY")
if not key:
    raise ValueError("API key not found. Please set the KEY environment variable.") 

llm = ChatOpenAI(
   openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=key,
    model_name="mistralai/devstral-small:free"
)

search_tool = TavilySearch(max_results=5, max_depth="basic")


@tool
def get_system_time() -> str:
    """Get the current system time."""
    return datetime.datetime.now().isoformat()

prompt = hub.pull("hwchase17/react")

react_runnble = create_react_agent(
    llm=llm,    
    tools=[search_tool, get_system_time],
    prompt=prompt
    )

tools=[get_system_time, search_tool]

