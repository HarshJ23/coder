from typing import Optional , Dict , Any
import os
import subprocess
import sys
from ..models.tool_models import ToolResponse


def execute_shell_tool(
    command: str,
    directory: Optional[str] = None,
    timeout: int = 30_000,
    stream: bool = False,
) -> ToolResponse:
    """
    Execute a shell command cross-platform.
    - stream=False (default): captures stdout/stderr (non-interactive).
    - stream=True: attaches directly to terminal (interactive).
    Works on Windows (cmd.exe / PowerShell) and Linux/macOS (bash/zsh).
    """
    try:
        cwd = os.path.abspath(directory) if directory else None

        if stream:
            process = subprocess.Popen(
                command,
                cwd=cwd,
                shell=True,  
                stdin=sys.stdin,
                stdout=sys.stdout,
                stderr=sys.stderr,
                text=True,
            )
            exit_code = process.wait()
            if exit_code == 0:
                return ToolResponse(
                    status="success",
                    data=f"Command executed successfully with exit code {exit_code}",
                    tool_name="execute_shell_tool"
                )
            else:
                return ToolResponse(
                    status="error",
                    data=None,
                    tool_name="execute_shell_tool",
                    error=f"Command exited with code {exit_code}"
                )

        else:
            # Capture-only mode
            completed = subprocess.run(
                command,
                cwd=cwd,
                shell=True,   # system shell handles cmd/bash automatically
                capture_output=True,
                text=True,
                timeout=timeout / 1000,
            )
            if completed.returncode == 0:
                return ToolResponse(
                    status="success",
                    data={
                        "stdout": completed.stdout,
                        "stderr": completed.stderr,
                        "exit_code": completed.returncode
                    },
                    tool_name="execute_shell_tool"
                )
            else:
                return ToolResponse(
                    status="error",
                    data={
                        "stdout": completed.stdout,
                        "stderr": completed.stderr,
                        "exit_code": completed.returncode
                    },
                    tool_name="execute_shell_tool",
                    error=f"Command exited with code {completed.returncode}"
                )

    except subprocess.TimeoutExpired:
        return ToolResponse(
            status="error",
            data=f"Command timed out after {timeout}ms",
            tool_name="execute_shell_tool",
            error=f"Command timed out after {timeout}ms"
        )
    except Exception as e:
        return ToolResponse(
            status="error",
            data=f"Exception occurred while executing command: {str(e)}",
            tool_name="execute_shell_tool",
            error=str(e)
        )
