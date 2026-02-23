from langgraph.graph import StateGraph, START, END
from state import HRState
from nodes import handle_leave, intent_classifier_node, handle_policy, handle_greet, handle_leave, handle_claim, handle_feedback
from typing import Literal
from config import llm
from langgraph.checkpoint.memory import MemorySaver

# 1. Initialize the memory
memory = MemorySaver()
def router(state: HRState) -> Literal["leave", "policy", "greet","feedback","claim","other"]:
    cat = state["category"]
    if cat in ["leave", "policy", "greet","feedback","claim"]:
        return cat
    return "other"

builder = StateGraph(HRState)

builder.add_node("intent_classifier", intent_classifier_node)
builder.add_node("leave", handle_leave)
builder.add_node("policy", handle_policy)
builder.add_node("greet", handle_greet)
builder.add_node("claim", handle_claim)
builder.add_node("feedback", handle_feedback)


builder.add_node("other", lambda x: {"response": "I'm not sure how to help with that yet."})

# Define the Flow
builder.add_edge(START, "intent_classifier")

# The Decision Point
builder.add_conditional_edges(
    "intent_classifier",
    router,
    {
        "leave": "leave",
        "policy": "policy",
        "greet": "greet",
        "claim": "claim",
        "feedback": "feedback",
        "other": "other"


    }
)


builder.add_edge("leave", END)
builder.add_edge("policy", END)
builder.add_edge("claim", END)
builder.add_edge("feedback", END)
builder.add_edge("greet", END)
builder.add_edge("other", END)

graph = builder.compile(checkpointer=memory)

from IPython.display import Image,display

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    pass
