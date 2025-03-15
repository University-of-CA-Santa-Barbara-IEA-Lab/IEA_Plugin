from typing import List, Any
from typing_extensions import TypedDict, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages

# Define the input state for the workflow
class InputState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
# Define the output state for the workflow
class OutputState(TypedDict):
    answer: str
# Define the overall state containing all relevant information
class OverallState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    user_query: str
    complete_user_query: str
    thought: str
    workflow: List[str]
    output_message: str
    answer: str