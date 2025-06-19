from schema import AgentState
from tools import react_runnble, tools


#reason node
def reason_node(state:AgentState):
    agent_action = react_runnble.invoke(state)
    return {"agent_outcome": agent_action}


#action node 
def action_node(state:AgentState):
    
    agent_action = state["agent_outcome"]
    tool_name = agent_action.tool
    tool_input = agent_action.tool_input
    
    tool_function=None
    for tool in tools:
        if tool.name == tool_name:
            tool_function = tool
            break   
        
    output=""
    if tool_function is None:
        output="Tool not found"
    else:
        if isinstance(tool_function, dict):
            output = tool_function.invoke(**tool_input)
        else:
            output = tool_function.invoke(tool_input)

    return {"intermediate_steps": [(agent_action, output)]}
    
    
    