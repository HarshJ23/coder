import os
import sys
import msvcrt
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.markup import escape  # ✅ Correct way to escape Rich markup
from core.agent import Coder
from core.tools.tool_directory import tools
from core.prompts import AGENT_SYSTEM_PROMPT

console = Console()

HEADER = """
 ██████╗ ██████╗ ██████╗ ███████╗██████╗ 
██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗
██║     ██║   ██║██║  ██║█████╗  ██████╔╝
██║     ██║   ██║██║  ██║██╔══╝  ██╔══██╗
╚██████╗╚██████╔╝██████╔╝███████╗██║  ██║
 ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
Welcome to CODER !
"""

# ----------------------------
# File Selection Utilities
# ----------------------------

def select_files():
    """Interactive file selector for multi-file operations."""
    files = []
    for root, dirs, filenames in os.walk("."):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    
    if not files:
        console.print("No files found.")
        return []
    
    # Interactive multi-select menu
    selected = interactive_menu(files)
    return selected


def interactive_menu(options):
    """Simple keyboard-based file selector."""
    current_index = 0
    selected_indices = set()
    
    while True:
        console.clear()
        console.print("[bold blue]File Selector[/bold blue]")
        console.print("Use ↑↓ to navigate, SPACE to select/deselect, ENTER to confirm, ESC to cancel\n")
        
        for i, option in enumerate(options):
            marker = "→" if i == current_index else " "
            check = "[✓]" if i in selected_indices else "[ ]"
            style = "bold cyan" if i == current_index else ""
            console.print(f"{marker} {check} {option}", style=style)
        
        console.print(f"\nSelected: {len(selected_indices)} files")
        
        # Wait for key press
        key = msvcrt.getch()
        
        if key == b'\xe0':  # Arrow key prefix
            key = msvcrt.getch()
            if key == b'H':  # Up arrow
                current_index = (current_index - 1) % len(options)
            elif key == b'P':  # Down arrow
                current_index = (current_index + 1) % len(options)
        elif key == b' ':  # Space bar toggles selection
            if current_index in selected_indices:
                selected_indices.remove(current_index)
            else:
                selected_indices.add(current_index)
        elif key == b'\r':  # Enter key
            return [options[i] for i in selected_indices]
        elif key == b'\x1b':  # Escape key
            return []


# ----------------------------
# Agent Initialization
# ----------------------------

def initialize_agent(project_path=".", model="groq/moonshotai/kimi-k2-instruct-0905"):
    """Initialize the main Coder agent."""
    abs_path = os.path.abspath(project_path)
    project_info = f"Project Path: {abs_path}, OS: {os.name}"
    system_prompt = AGENT_SYSTEM_PROMPT + f"project info : {project_info}"
    
    return Coder(name="Coder", system_prompt=system_prompt, model=model, agent_tools=tools)


# ----------------------------
# Main CLI Loop
# ----------------------------

def main():
    console.print(HEADER, style="bold blue")
    
    # Get basic info
    project_path = Prompt.ask("Enter project path", default=".")
    model = Prompt.ask("Enter model (or press Enter for default)", default="groq/moonshotai/kimi-k2-instruct-0905")
    
    # Initialize agent
    agent = initialize_agent(project_path, model)
    console.print("\n[green]Agent initialized. Type your queries below. Type 'exit' to quit.[/green]\n")
    
    while True:
        query = Prompt.ask("You")
        if query.lower() in ["exit", "quit"]:
            console.print("[red]Goodbye![/red]")
            break

        # File selector shortcut
        if query.strip() == "#":
            selected_paths = select_files()
            if selected_paths:
                console.print(f"Selected files: {', '.join(selected_paths)}")
                default_query = f"Analyze these files: {', '.join(selected_paths)}"
                query = Prompt.ask("Enter your query with the selected files", default=default_query)
            else:
                continue
        
        # Run the agent
        try:
            with console.status("[bold green]CODER is thinking...[/bold green]", spinner="dots") as status:
                response_started = False
                
                for event in agent.run(query):
                    if event["type"] == "llm_response":
                        if not response_started:
                            response_started = True
                            status.stop()
                            console.print("[bold blue]CODER:[/bold blue] ", end="")
                        
                        content = event["data"]["content"]
                        console.print(content, end="")
                        sys.stdout.flush()
                    
                    elif event["type"] == "tool_call":
                        if not response_started:
                            response_started = True
                            status.stop()
                            console.print("[bold blue]CODER:[/bold blue] ", end="")
                        console.print(f"\n[dim]Using {event['data']['tool_name']}[/dim]")
                    
                    elif event["type"] == "tool_response":
                        if not response_started:
                            response_started = True
                            status.stop()
                            console.print("[bold blue]CODER:[/bold blue] ", end="")
                        tool_name = event["data"]["tool_name"]
                        content = event["data"]["content"] or "No output"
                        if len(content) > 100:
                            content = content[:100] + "..."
                        console.print(f"[dim]{tool_name}: {content}[/dim]")
                    
                    elif event["type"] == "final_content":
                        break  # already shown
                    
                    elif event["type"] == "error":
                        if not response_started:
                            response_started = True
                            status.stop()
                            console.print("[bold blue]CODER:[/bold blue] ", end="")
                        console.print(f"\n[red]Error:[/red] {escape(event['data']['message'])}")
                    
                    elif event["type"] == "usage":
                        pass  # hide token usage
                
                # Newline after output
                if response_started:
                    console.print()
        
        except Exception as e:
            console.print(f"[red]Error running agent:[/red] {escape(str(e))}")
        
        console.print()  # extra line between queries


if __name__ == "__main__":
    main()
