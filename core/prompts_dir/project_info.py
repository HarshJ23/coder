import os
import platform
from pathlib import Path

def get_project_info() -> str:
    os_name = f"{platform.system()} {platform.release()}"
    shell = os.getenv("SHELL") or os.getenv("COMSPEC") or "Unknown Shell"
    home_dir = str(Path.home())


    working_dir = os.getcwd()

    workspace_title = "Current Working Directory"
    workspace_info = working_dir

    project_info = f"""
PROJECT INFORMATION

Operating System: {os_name}
Default Shell: {shell}
Home Directory: {home_dir}
{workspace_title}: {workspace_info}
"""

    return project_info

# print(get_project_info())