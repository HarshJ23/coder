from typing import List
from ..models.tool_models import ToolResponse


def spawn_subagent(name: str, description: str, task: str, tools_list: List[str]):
    from ..sub_agent import SubCoder
    sub_agent = SubCoder.create_subagent(
        name, description=description, task=task, tools_list=tools_list
    )
    for event in sub_agent.run(task):
        if event["type"] == "final_content":
            return ToolResponse(
                status="success",
                data=event["data"]["content"],
                tool_name="spawn_subagent",
            )
