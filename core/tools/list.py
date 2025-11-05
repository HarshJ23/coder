import os
import fnmatch
from pathlib import Path
from ..models.tool_models import ToolResponse

IGNORE_PATTERNS = [
    "node_modules", "__pycache__", ".git", "dist", "build", "target",
    "vendor", "bin", "obj", ".idea", ".vscode", ".zig-cache", "zig-out",
    ".coverage", "coverage", "tmp", "temp", ".cache", "cache", "logs",
    ".venv", "venv", "env" , ".next"
]

LIMIT = 100


def list_tool(path: str = ".", ignore: list[str] = None):
    """
    Lists directories and files in a tree-like structure,
    while ignoring common large or temporary folders.

    Args:
        path (str): Path to list.
        ignore (list[str]): Additional ignore patterns.

    Returns:
        dict: {
            "title": relative path,
            "metadata": {"count": int, "truncated": bool},
            "output": str
        }
    """
    ignore = ignore or []
    search_path = Path(path).resolve()

    files = []
    all_dirs = set()
    count = 0

    for root, dirs, filenames in os.walk(search_path):
        rel_root = os.path.relpath(root, search_path).replace("\\", "/")
        if rel_root == ".":
            rel_root = ""

        dirs[:] = [
            d for d in dirs
            if not any(p in d or fnmatch.fnmatch(d, f"*{p}*") for p in IGNORE_PATTERNS + ignore)
        ]

        all_dirs.add(rel_root or ".")
        for d in dirs:
            d_path = f"{rel_root}/{d}" if rel_root else d
            all_dirs.add(d_path)

        for file in filenames:
            if any(p in file or fnmatch.fnmatch(file, f"*{p}*") for p in IGNORE_PATTERNS + ignore):
                continue

            rel_path = f"{rel_root}/{file}" if rel_root else file
            files.append(rel_path)
            count += 1
            if count >= LIMIT:
                break
        if count >= LIMIT:
            break

    # Build directory -> files mapping
    files_by_dir = {}
    for f in files:
        dir_path = os.path.dirname(f).replace("\\", "/") or "."
        files_by_dir.setdefault(dir_path, []).append(os.path.basename(f))

    def render_dir(dir_path: str, depth: int) -> str:
        indent = "  " * depth
        output = ""

        if depth > 0 and dir_path != ".":
            output += f"{indent}{os.path.basename(dir_path)}/\n"

        # Get subdirectories
        children = sorted([
            d for d in all_dirs
            if ("/" in d and os.path.dirname(d) == dir_path)
            or (dir_path == "." and "/" not in d and d != ".")
        ])

        for child in children:
            output += render_dir(child, depth + 1)

        child_indent = "  " * (depth + 1)
        for f in sorted(files_by_dir.get(dir_path, [])):
            output += f"{child_indent}{f}\n"

        return output

    output = f"{search_path}/\n" + render_dir(".", 0)

    # return {
    #     "title": os.path.basename(search_path),
    #     "metadata": {"count": len(files), "truncated": len(files) >= LIMIT},
    #     "output": output
    # }

    return ToolResponse(
        status="success",
        data= f"{os.path.basename(search_path) : {output}}",
        tool_name="list_tool"
    )


# Example usage
# if __name__ == "__main__":
#     result = list_tool("engineering-project-manager")
#     print("Title:", result["title"])
#     print("Metadata:", result["metadata"])
#     print("Output:\n", result["output"])
