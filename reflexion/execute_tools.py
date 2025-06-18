from langchain_tavily import TavilySearch
from langchain_core.messages import ToolMessage,HumanMessage
import json
search_tool= TavilySearch(max_results=4)

def execute_tools(state):
    message=state[-1]
    json_str = message.content
    message = json.loads(json_str)
    query_results={}
    for query in message["search_queries"]:
        search_results = search_tool.invoke(query)
        query_results[query]=search_results
        
    return [
        HumanMessage(
            content=json.dumps(query_results),
        )
    ]