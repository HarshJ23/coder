import os
from typing import Dict, List, Any
from models.tool_models import ToolResponse


def edit_file_tool(file_path: str, old_str: str, new_str: str, replace_all: bool = False) -> ToolResponse:
    """
    Edits an existing file by replacing old_str with new_str.
    If replace_all is True, replaces all occurrences; otherwise, only the first.
    Supports multi-line strings.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} does not exist.")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if old_str not in content:
            return ToolResponse(
                status="error",
                data=f"'{old_str}' not found in {file_path}.",
                tool_name="edit_file_tool",
                error=f"'{old_str}' not found in {file_path}."
            )

        if replace_all:
            new_content = content.replace(old_str, new_str)
        else:
            new_content = content.replace(old_str, new_str, 1)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return ToolResponse(
            status="success",
            data=f"Replaced '{old_str}' with '{new_str}' in {file_path}.",
            tool_name="edit_file_tool"
        )
    except Exception as e:
        return ToolResponse(
            status="error",
            data=f"Error editing file: {str(e)}",
            tool_name="edit_file_tool",
            error=str(e)
        )
