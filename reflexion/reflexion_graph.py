from langgraph.graph import MessageGraph,END
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from reflexion.chains import responder_chain, revisor_chain
from reflexion.execute_tools import execute_tools

graph=MessageGraph()

RESPONDER="responder"
REVISOR="revisor"
SEARCHCALL="search_call"

def responder_node(state):
    pydantic_output= responder_chain.invoke(
        {
            "messages":state
        }
    )
    return AIMessage(
        content=pydantic_output.json()
    )
    


def revisor_node(state):
    print(state)
    pydantic_output=revisor_chain.invoke(
        {
            "messages":state
        }
    )
    return AIMessage(
        content=pydantic_output.json(),
    
    )

graph.add_node(RESPONDER,responder_node)
graph.add_node(REVISOR,revisor_node)
graph.add_node(SEARCHCALL,execute_tools)

graph.set_entry_point(RESPONDER)
graph.add_edge(RESPONDER,SEARCHCALL)
graph.add_edge(SEARCHCALL,REVISOR )

def switch_call(state):
    """Switch the call to the search tool."""
    count_tool_call=len(state)
    if count_tool_call>5:
        return END
    return SEARCHCALL


graph.add_conditional_edges(REVISOR,switch_call)

app=graph.compile()

response = app.invoke(
    "Write about how small business can leverage AI to grow"
)

print(response[-1])