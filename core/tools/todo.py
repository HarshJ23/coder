import json
from ..models.tool_models import ToolResponse

def write_todos(todos: list[dict], tool_call_id=None) -> ToolResponse:
    """Updates the current todo list"""
    # For now just print and return it
    # print(f"Updated todos: {todos}")
    return ToolResponse(
        status="success",
        data={"todos": todos},
        tool_name="write_todos"
    )
