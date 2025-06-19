from langgraph.graph import StateGraph,END
from nodes import reason_node, action_node
from langchain_core.agents import AgentFinish, AgentAction
from schema import AgentState
import os
from dotenv import load_dotenv
load_dotenv()

# Define the state graph
graph = StateGraph(AgentState)

#should continue after reason to [action or finish]
def continue_after_reason(state: AgentState):
    agent_outcome = state["agent_outcome"]
    if isinstance(agent_outcome, AgentAction) and len(state["intermediate_steps"]) < 6:
        return ACTION
    else:
        return END
    
    
# Define the nodes in the graph
REASON="reason"
ACTION="action"
graph.add_node(REASON, reason_node)
graph.add_node(ACTION, action_node)


# Define the edges in the graph
graph.add_edge(ACTION,REASON)
graph.add_conditional_edges(REASON, continue_after_reason)

graph.set_entry_point(REASON)

init_state={
    "input": "Hi tell me when Sri ram was born and also tell me it is how many years back from now?",
    "agent_outcome": None,
    "intermediate_steps": []
}

app=graph.compile()

response=app.invoke(init_state)


print(response["agent_outcome"].return_values["output"], "final result")