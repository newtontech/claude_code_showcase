"""Shell tool for executing safe shell commands."""

import shlex
import subprocess
from typing import Literal

from openmanus.config import get_settings
from openmanus.tools.base import Tool, ToolError, ToolOutput


class ShellTool(Tool):
    """Tool for executing safe shell commands.

    This tool only allows whitelisted commands and blocks dangerous operations.
    """

    # Default whitelist of safe commands
    DEFAULT_WHITELIST = ["ls", "cat", "grep", "wc", "head", "tail", "python3", "mkdir"]

    # Default blacklist of dangerous commands
    DEFAULT_BLACKLIST = [
        "rm",
        "mv",
        "sudo",
        "curl",
        "wget",
        "ssh",
        "chmod",
        "chown",
        "kill",
        "killall",
        "pkill",
        "shutdown",
        "reboot",
        "format",
        "fdisk",
        "dd",
    ]

    def __init__(
        self,
        whitelist: list[str] | None = None,
        blacklist: list[str] | None = None,
    ) -> None:
        """Initialize the shell tool.

        Args:
            whitelist: List of allowed commands. If None, uses default whitelist.
            blacklist: List of forbidden commands. If None, uses default blacklist.
        """
        settings = get_settings()
        self.whitelist = set(whitelist or settings.shell_whitelist)
        self.blacklist = set(blacklist or settings.shell_blacklist)

    @property
    def name(self) -> str:
        """Return the name of this tool."""
        return "shell"

    def execute(self, inputs: dict) -> ToolOutput:
        """Execute a shell command.

        Args:
            inputs: Must contain 'cmd' key. Optional 'timeout' key (in seconds, default 30)

        Returns:
            ToolOutput with command output

        Raises:
            ToolError: If the command is not allowed or execution fails
        """
        if "cmd" not in inputs:
            return ToolOutput(success=False, data=None, error="Missing 'cmd' in inputs")

        cmd = inputs["cmd"]
        timeout = inputs.get("timeout", 30)

        # Parse the command to get the base command
        try:
            parts = shlex.split(cmd)
            if not parts:
                return ToolOutput(success=False, data=None, error="Empty command")

            base_cmd = parts[0]

        except ValueError as e:
            return ToolOutput(success=False, data=None, error=f"Invalid command syntax: {e}")

        # Check blacklist first
        if base_cmd in self.blacklist:
            return ToolOutput(
                success=False,
                data=None,
                error=f"Command '{base_cmd}' is not allowed (blacklisted)",
            )

        # Check whitelist
        if base_cmd not in self.whitelist:
            return ToolOutput(
                success=False,
                data=None,
                error=f"Command '{base_cmd}' is not in the allowed list: {sorted(self.whitelist)}",
            )

        # Check for dangerous patterns in the full command
        dangerous_patterns = [
            "rm -rf /",
            "rm -rf /*",
            "> /",
            "dd if=",
            "mkfs",
            ":(){:|:&};:",  # fork bomb
        ]
        cmd_lower = cmd.lower()
        for pattern in dangerous_patterns:
            if pattern in cmd_lower:
                return ToolOutput(
                    success=False,
                    data=None,
                    error=f"Command contains dangerous pattern: {pattern}",
                )

        # Execute the command
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )

            stdout = result.stdout
            stderr = result.stderr
            return_code = result.returncode

            return ToolOutput(
                success=return_code == 0,
                data={
                    "stdout": stdout,
                    "stderr": stderr,
                    "return_code": return_code,
                    "command": cmd,
                },
                error=stderr if return_code != 0 else None,
            )

        except subprocess.TimeoutExpired:
            return ToolOutput(
                success=False,
                data=None,
                error=f"Command timed out after {timeout} seconds",
            )
        except Exception as e:
            return ToolOutput(success=False, data=None, error=f"Error executing command: {e}")
