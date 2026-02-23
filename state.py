from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class HRState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    user_query: str
    category: str
    response: str
    # --- New Fields for Leave Logic ---
    leave_dates: str
    leave_reason: str
    pto_available: int # We'll assume this starts at 15