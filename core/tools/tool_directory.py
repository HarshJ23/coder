from ..prompts import (
    web_search_description,
    WRITE_TODOS_DESCRIPTION,
    READ_FILE_TOOL_DESCRIPTION ,
    CREATE_DIRECTORY_TOOL_DESCRIPTION ,
    SHELL_TOOL_DESC,
    create_file_tool_description,
    grep_tool_description,
    edit_file_tool_description
    )
from .list import list_tool
from .web_search import web_search_tool
from .todo import write_todos
from .file_tools import (
create_file_tool,
write_file_tool,
read_file_tool,
create_directory
)
from .edit import edit_file_tool
from .shell_tool import execute_shell_tool
from .grep import grep_tool
from .spawn_subagent import spawn_subagent




available_functions = {
        "web_search_tool": web_search_tool,
        "write_todos": write_todos,
        "create_file_tool" : create_file_tool,
        "write_file_tool" : write_file_tool,
        "read_file_tool" : read_file_tool,
        "create_directory" : create_directory,
        "edit_file_tool" : edit_file_tool,
        "execute_shell_tool" : execute_shell_tool,
        "list_tool" : list_tool,
        "grep_tool" : grep_tool,
        "spawn_subagent": spawn_subagent
}



tools = [
        {
            "type": "function",
            "function": {
                "name": "web_search_tool",
                "description": web_search_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "search_query": {
                            "type": "string",
                            "description": "The search query for which information needs to be fetched.",
                        }
                    },
                    "required": ["search_query"],
                },
            },
        },

        {
    "type": "function",
    "function": {
        "name": "write_todos",
        "description": WRITE_TODOS_DESCRIPTION,  # from your earlier code
        "parameters": {
            "type": "object",
            "properties": {
                "todos": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "task": {"type": "string", "description": "The description of the task"},
                            "status": {"type": "string", "enum": ["pending", "in_progress", "completed"]}
                        },
                        "required": ["task", "status"]
                    },
                    "description": "List of tasks with their statuses"
                }
            },
            "required": ["todos"]
        }
    }
},
{
            "type": "function",
            "function": {
                "name": "create_file_tool",
                "description": create_file_tool_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Absolute or relative path of the file to create.",
                        }
                    },
                    "required": ["file_path"],
                },
            },
        },
{
    "type": "function",
    "function": {
        "name": "write_file_tool",
        "description": "Writes text content to an existing file. Overwrites the file’s contents entirely. Requires the file to already exist (use create_file_tool first if needed).",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Absolute or relative path of the file to write to."
                },
                "content": {
                    "type": "string",
                    "description": "The text content to write into the file."
                }
            },
            "required": ["file_path", "content"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "read_file_tool",
        "description": READ_FILE_TOOL_DESCRIPTION,
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Absolute or relative path of the file to be read."
                },
            },
            "required": ["file_path"]
        }
    }
},
{
"type": "function",
"function": {
"name": "edit_file_tool",
        "description": edit_file_tool_description,
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Absolute or relative path of the file to edit."
                },
                "old_str": {
                    "type": "string",
                    "description": "The string to replace in the file."
                },
                "new_str": {
                    "type": "string",
                    "description": "The new string to replace old_str with."
                },
                "replace_all": {
                    "type": "boolean",
                    "description": "Whether to replace all occurrences of old_str. Defaults to false.",
                    "default": "false"
                }
            },
            "required": ["file_path", "old_str", "new_str"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "create_directory",
        "description": CREATE_DIRECTORY_TOOL_DESCRIPTION,
        "parameters": {
            "type": "object",
            "properties": {
                "directory_path": {
                    "type": "string",
                    "description": "Absolute or relative path of the directory to be created. Supports nested directories."
                }
            },
            "required": ["directory_path"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "execute_shell_tool",
        "description": SHELL_TOOL_DESC,
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The shell command to be executed. could be used to scaffold a template/project.Always execute the command in a new shell/window command prompt to avoid breaking the flow of agent execution. for example , in windows , ALWAYS use cmd /k <command> by default while using this tool."
                },
                "stream": {
                    "type": "boolean",
                    "description": "Always True"
                }
            },
            "required": ["command" , "stream"]
        }
    }
},
{
  "type": "function",
  "function": {
    "name": "list_tool",
    "description": "Lists files and directories in a given path, producing a tree-like structure. Supports ignoring patterns and limits results to 100 files.",
    "parameters": {
      "type": "object",
      "properties": {
        "path": {
          "type": "string",
          "description": "The absolute or relative path to the directory to list. Defaults to current directory if not provided."
        },
        "ignore": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Optional list of glob-style patterns (e.g., 'dist/', 'logs/*') to ignore while listing files."
        }
      },
      "required": []
    }
  }
},
{
    "type": "function",
    "function": {
        "name": "grep_tool",
        "description": grep_tool_description,
        "parameters": {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "The regex pattern to search in the code file."
                },
                "path": {
                    "type": "string",
                    "description": "The file to search in"
                }
            },
            "required": ["pattern" , "path"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "spawn_subagent",
        "description": """
Use to create subagents for offloading specific and complex tasks , avoiding context overload on the main agent.
-  Only use this tool if the task is complex or might result in high no. of tool call invocations.
-  For creating subagent - based on task requirement choose the appropriate tools from the following list:
   - web_search_tool 
   - write_todos
   - create_file_tool 
   - write_file_tool
   - read_file_tool
   - create_directory
   - edit_file_tool
   - execute_shell_tool
   - list_tool
   - grep_tool
""",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the subagent."
                },
                "description": {
                    "type": "string",
                    "description": "Overview and description of the task to be performed by the subagent."
                },
                "task": {
                    "type": "string",
                    "description": "Exact task to guide the subagent - may contain detailed implementation steps, research pointers based on your codebase understanding etc."
                },
                "tools_list": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Tool names from the list needed for the agent to perform the required task."
                }
            },
            "required": ["name", "description", "task", "tools_list"]
        }
    }
}
]
