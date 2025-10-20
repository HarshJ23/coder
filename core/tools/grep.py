import os
import re
from typing import Dict, Any, List
from models.tool_models import ToolResponse


IGNORE_DIRS = [
    "node_modules", ".git", "__pycache__", "dist", "build", "target",
    "venv", ".venv", "env", "logs", ".idea", ".vscode" ,".next"
]


def grep_tool(pattern: str, path: str) -> ToolResponse:
    """
    Search for a regex pattern in a file or recursively in all files under a directory.

    Args:
        pattern (str): Regex pattern to search for.
        path (str): File or directory path.

    Returns:
        ToolResponse: Contains list of matches with file path, line number, match text, and groups.
    """
    if not path:
        return ToolResponse(
            status="error",
            data="Path must not be None",
            tool_name="grep_tool",
            error="Path must not be None"
        )

    if not os.path.exists(path):
        return ToolResponse(
            status="error",
            data=f"Path '{path}' does not exist.",
            tool_name="grep_tool",
            error=f"Path '{path}' does not exist."
        )

    search_pattern = re.compile(pattern, re.DOTALL)
    results: List[Dict[str, Any]] = []

    def search_in_file(file_path: str):
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            for m in search_pattern.finditer(content):
                start_line = content[:m.start()].count("\n") + 1
                results.append({
                    "file_path": file_path,
                    "start_line_no": start_line,
                    "match_text": m.group(0),
                    "groups": m.groups(),
                })
        except (UnicodeDecodeError, PermissionError):
            # Skip binary/unreadable files
            pass

    if os.path.isfile(path):
        search_in_file(path)
    else:
        for root, dirs, files in os.walk(path):
            # Skip ignored directories
            dirs[:] = [
                d for d in dirs
                if not any(ignored in d for ignored in IGNORE_DIRS)
            ]

            for file in files:
                file_path = os.path.join(root, file)
                search_in_file(file_path)

    return ToolResponse(
        status="success",
        data=results,
        tool_name="grep_tool"
    )
