
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from reflex.chains import critic_chain, generation_chain
from langgraph.graph import MessageGraph,END
from dotenv import load_dotenv
import os
load_dotenv()


key=os.getenv("KEY")
if key is None:
    raise ValueError("API key not found. Please set the KEY environment variable.")


graph=MessageGraph()

GENERATE="generate"
CRITIC="critic"

def generation_node(state):
    return generation_chain.invoke(
        {
            "chat_history": state
        }
    )
    
def critic_node(messages):
    response= critic_chain.invoke(
        {
            "chat_history": messages
        }
    )
    return HumanMessage(content=response.content)


graph.add_node(GENERATE,generation_node)
graph.add_node(CRITIC,critic_node)

graph.set_entry_point(GENERATE)

def switch_node(state):
    if len(state) > 4:
        return "end"
    return "critic"


graph.add_conditional_edges(GENERATE,switch_node,{
    "end":END,
    "critic":CRITIC
})

graph.add_edge(CRITIC,GENERATE)


app=graph.compile()

app.get_graph().print_ascii()

response=app.invoke(HumanMessage(content="Write a linkedIn Post on AI Agent Advancement"));
print(response)