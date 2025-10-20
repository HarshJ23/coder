import os
from typing import Dict , List , Any
from models.tool_models import ToolResponse

def create_file_tool(file_path: str, content: str = "") -> ToolResponse:
    """
    Creates a new file at the given path.
    If parent directories don't exist, they are created automatically.
    """
    try:
        # parent directory verification
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # file write
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        # return f"File created successfully at {file_path}"
        return ToolResponse(
            status = "success",
            data = f"file created at {file_path}",
            tool_name= "create_file_tool"
        )
    except Exception as e:
        return ToolResponse(
            status = "error",
            data = f"Error creating file: {str(e)}",
            tool_name= "create_file_tool",
            error= str(e)
        )


def write_file_tool(file_path: str, content: str) -> ToolResponse:
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            # return {"success" : True , "message" : f"write complete for {file_path}"}
            return ToolResponse(
                status = "success",
                data = f"Code written at {file_path}",
                tool_name= "write_file_tool"
            )
    except FileNotFoundError as e:
        return ToolResponse(
            status = "error",
            data = f"File not found: {str(e)}",
            tool_name= "write_file_tool",
            error = str(e)
        )
    except Exception as e:
        # return {"success" : False , "error" : str(e)}
        return ToolResponse(
            status = "error",
            data = f"Error writing file: {str(e)}",
            tool_name= "write_file_tool",
            error  =  str(e)
        )

def read_file_tool(file_path: str) -> ToolResponse:
    """
    Read  a file and return its content (by default , can read only 2000 loc).

    Args:
        file_path (str): file path.
    Returns:
        dict :  {"status" : 'complete' | 'error' ,
                 "content" :  <file_content> .. </file_content>}
    """
    if not file_path:
        return ToolResponse(
            status="error",
            data=f"{file_path} is invalid. Please try again with a valid file_path",
            tool_name="read_file_tool",
            error=f"{file_path} is invalid. Please try again with a valid file_path"
        )
    if not os.path.exists(file_path):
        return ToolResponse(
            status="error",
            data=f"{file_path} does not exist. Try again.",
            tool_name="read_file_tool",
            error=f"{file_path} does not exist. Try again."
        )
    results = []
    max_lines = 2000
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            for line_no, line in enumerate(file, start=1):
                if line_no > max_lines:
                    break
                results.append(f"{line_no:04d} : {line.rstrip()}")
        format_content = "<file_content>\n" + "\n".join(results) + "\n</file_content>"
        # return {"status" : "complete"  , "data" : format_content}
        return ToolResponse(
            status="success",
            data=format_content,
            tool_name="read_file_tool"
        )
    except Exception as e:
        # return {"status":"error" , "data" : str(e)}
        return ToolResponse(
            status="error",
            data=f"Error reading file: {str(e)}",
            tool_name="read_file_tool",
            error=str(e)
        )

def create_directory(directory_path : str) -> ToolResponse:
    """
    Creates a directory(nested directories).
    Does nothing if the directory already exists.
    """
    # exist_ok=True --> doesn't return error if directory already exist.
    try:
        os.makedirs(directory_path , exist_ok = True)
        return ToolResponse(
            status = "success",
            data = f"{directory_path} directory created",
            tool_name =  "create_directory",
        )
    except Exception as e:
        return ToolResponse(
            status = "error",
            data = f"Error creating directory: {str(e)}",
            tool_name =  "create_directory",
            error = str(e)
        )


# testing
# res = read_file_tool("tools/grep.py")

# if res.status == "success":
#     tool_response = res.data

# print(f"tool_response : {tool_response}")
# print(f"complete response : {res}")
