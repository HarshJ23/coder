import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
import msvcrt
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

def select_files():
    import os
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
    current_index = 0
    selected_indices = set()
    
    while True:
        console.clear()
        console.print("[bold blue]File Selector[/bold blue]")
        console.print("Use ↑↓ to navigate, SPACE to select/deselect, ENTER to confirm, ESC to cancel")
        console.print()
        
        for i, option in enumerate(options):
            marker = "→" if i == current_index else " "
            check = "[✓]" if i in selected_indices else "[ ]"
            style = "bold cyan" if i == current_index else ""
            console.print(f"{marker} {check} {option}", style=style)
        
        console.print()
        console.print(f"Selected: {len(selected_indices)} files")
        
        # Wait for key press
        key = msvcrt.getch()
        
        if key == b'\xe0':  # Special key prefix
            key = msvcrt.getch()
            if key == b'H':  # Up arrow
                current_index = (current_index - 1) % len(options)
            elif key == b'P':  # Down arrow
                current_index = (current_index + 1) % len(options)
        elif key == b' ':  # Space
            if current_index in selected_indices:
                selected_indices.remove(current_index)
            else:
                selected_indices.add(current_index)
        elif key == b'\r':  # Enter
            return [options[i] for i in selected_indices]
        elif key == b'\x1b':  # Escape
            return []

def initialize_agent(project_path=".", model="groq/moonshotai/kimi-k2-instruct-0905"):
    # Basic project scan (expand as needed)
    abs_path = os.path.abspath(project_path)
    project_info = f"Project Path: {abs_path}, OS: {os.name}"
    
    # system_prompt = f"You are CODER, an AI coding assistant. {project_info}"
    system_prompt  = AGENT_SYSTEM_PROMPT + f"project info : {project_info}"
    
    return Coder(name="Coder", system_prompt=system_prompt, model=model, agent_tools=tools)

def main():
    console.print(HEADER, style="bold blue")
    
    # Get project path
    project_path = Prompt.ask("Enter project path", default=".")
    model = Prompt.ask("Enter model (or press Enter for default)", default="groq/moonshotai/kimi-k2-instruct-0905")
    
    agent = initialize_agent(project_path, model)
    
    console.print("\n[green]Agent initialized. Type your queries below. Type 'exit' to quit.[/green]\n")
    
    while True:
        query = Prompt.ask("You")
        if query.lower() in ['exit', 'quit']:
            console.print("[red]Goodbye![/red]")
            break

        if query.strip() == "#":
            selected_paths = select_files()
            if selected_paths:
                console.print(f"Selected files: {', '.join(selected_paths)}")
                default_query = f"Analyze these files: {', '.join(selected_paths)}"
                query = Prompt.ask("Enter your query with the selected files", default=default_query)
            else:
                continue
        
        with console.status("[bold green]CODER is thinking...[/bold green]", spinner="dots"):
            try:
                response_text = ""
                for event in agent.run(query):
                    if event['type'] == 'llm_response':
                        response_text += event['data']['content']
                    elif event['type'] == 'tool_call':
                        tool_name = event['data']['tool_name']
                        console.print(f"[dim]Using {tool_name}[/dim]")
                    elif event['type'] == 'tool_response':
                        tool_name = event['data']['tool_name']
                        content = event['data']['content']
                        if content:
                            content = content[:100] + "..." if len(content) > 100 else content
                        else:
                            content = "No output"
                        console.print(f"[dim]{tool_name}: {content}[/dim]")
                    elif event['type'] == 'final_content':
                        response_text += event['data']['content']
                        break
                    elif event['type'] == 'error':
                        console.print(f"[red]Error:[/red] {event['data']['message']}")
                    elif event['type'] == 'usage':
                        pass  # Skip token display for cleaner UI

                if response_text:
                    console.print(f"[blue]CODER:[/blue] {response_text.strip()}")
            except Exception as e:
                console.print(f"[red]Error running agent: {str(e)}[/red]")
        
        console.print()  # New line

if __name__ == "__main__":
    main()
