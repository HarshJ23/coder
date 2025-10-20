
from agent import Coder
from tools.tool_directory import tools
from prompts import AGENT_SYSTEM_PROMPT



coder_agent = Coder(
    name="coder" , 
    system_prompt=AGENT_SYSTEM_PROMPT , 
    model="groq/moonshotai/kimi-k2-instruct-0905" ,
    agent_tools= tools
    )


# 16-10-2025
tq9 = """Create a task manager for the projects I'm working on during my internship. Requirements:
- Web UI using plain HTML, CSS, and JavaScript with an enterprise-grade, professional, aesthetic style (clean, minimal, modern).
- Support multiple projects: user can add new projects and select a project from a list to manage its tasks.
- For each project, allow adding tasks, marking tasks complete, and viewing completed tasks in a separate "Completed" tab.
- Implement a very simple file-based storage solution (e.g., JSON files stored in a folder) for storing and querying projects and tasks. Organize files in a project folder.
- Provide an organized folder structure and all necessary files (HTML/CSS/JS and simple backend file handlers for persisting JSON).
- Ensure the UI is polished and usable (professional spacing, typography, colors, and responsive layout) while keeping the code readable and modular.
"""

res = coder_agent.run(tq9)

for event in res:
    if event["type"] == "llm_response":
        print("LLM:", event["data"]["content"])
    elif event["type"] == "tool_call":
        print("TOOL CALL:", event["data"])
    elif event["type"] == "tool_response":
        print("TOOL RESPONSE:", event["data"])
    elif event["type"] == "final_content":
        print("FINAL:", event["data"]["content"])
    elif event["type"] == "usage":
        print("TOKENS:", event["data"])
    elif event["type"] == "error":
        print("ERROR:", event["data"]["message"])


