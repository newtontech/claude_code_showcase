"""File tool for reading and writing files."""

import fnmatch
from pathlib import Path

from openmanus.config import get_settings
from openmanus.tools.base import Tool, ToolError, ToolOutput


class FileTool(Tool):
    """Tool for file operations within a workspace.

    This tool provides safe file operations that are restricted
    to the workspace root directory.
    """

    def __init__(self, workspace_root: str | None = None) -> None:
        """Initialize the file tool.

        Args:
            workspace_root: The root directory for file operations.
                If None, uses the current working directory.
        """
        settings = get_settings()
        self.workspace_root = Path(workspace_root or settings.workspace_root).resolve()

    @property
    def name(self) -> str:
        """Return the name of this tool."""
        return "file"

    def execute(self, inputs: dict) -> ToolOutput:
        """Execute a file operation.

        Args:
            inputs: Must contain 'action' key and action-specific inputs

        Returns:
            ToolOutput with the result

        Raises:
            ToolError: If the operation fails
        """
        action = inputs.get("action")

        if action == "read_text":
            return self._read_text(inputs)
        elif action == "write_text":
            return self._write_text(inputs)
        elif action == "list_dir":
            return self._list_dir(inputs)
        else:
            return ToolOutput(
                success=False,
                data=None,
                error=f"Unknown action: {action}. Valid actions: read_text, write_text, list_dir",
            )

    def _resolve_path(self, path: str) -> Path:
        """Resolve a path relative to workspace and ensure it's within bounds.

        Args:
            path: The path to resolve

        Returns:
            The resolved absolute path

        Raises:
            ToolError: If the path is outside the workspace
        """
        resolved = (self.workspace_root / path).resolve()

        # Ensure the resolved path is within workspace
        try:
            resolved.relative_to(self.workspace_root)
        except ValueError:
            raise ToolError(
                f"Path '{path}' is outside workspace root '{self.workspace_root}'"
            )

        return resolved

    def _read_text(self, inputs: dict) -> ToolOutput:
        """Read a text file.

        Args:
            inputs: Must contain 'path' key

        Returns:
            ToolOutput with file content
        """
        if "path" not in inputs:
            return ToolOutput(success=False, data=None, error="Missing 'path' in inputs")

        try:
            path = self._resolve_path(inputs["path"])
            content = path.read_text(encoding="utf-8")
            return ToolOutput(success=True, data={"content": content, "path": str(path)})
        except ToolError as e:
            return ToolOutput(success=False, data=None, error=str(e))
        except FileNotFoundError:
            return ToolOutput(success=False, data=None, error=f"File not found: {inputs['path']}")
        except IsADirectoryError:
            return ToolOutput(
                success=False,
                data=None,
                error=f"Path is a directory, not a file: {inputs['path']}",
            )
        except PermissionError:
            return ToolOutput(success=False, data=None, error=f"Permission denied: {inputs['path']}")
        except Exception as e:
            return ToolOutput(success=False, data=None, error=f"Error reading file: {e}")

    def _write_text(
        self,
        inputs: dict,
    ) -> ToolOutput:
        """Write text to a file.

        Args:
            inputs: Must contain 'path' and 'content' keys.
                Optional 'mode' key ('overwrite' or 'append', defaults to 'overwrite')

        Returns:
            ToolOutput with write confirmation
        """
        if "path" not in inputs:
            return ToolOutput(success=False, data=None, error="Missing 'path' in inputs")
        if "content" not in inputs:
            return ToolOutput(success=False, data=None, error="Missing 'content' in inputs")

        mode = inputs.get("mode", "overwrite")
        if mode not in ("overwrite", "append"):
            return ToolOutput(
                success=False,
                data=None,
                error=f"Invalid mode: {mode}. Must be 'overwrite' or 'append'",
            )

        try:
            path = self._resolve_path(inputs["path"])
            content = inputs["content"]

            # Create parent directories if they don't exist
            path.parent.mkdir(parents=True, exist_ok=True)

            # Write the file
            if mode == "append":
                with path.open("a", encoding="utf-8") as f:
                    f.write(content)
            else:
                path.write_text(content, encoding="utf-8")

            return ToolOutput(
                success=True,
                data={"path": str(path), "bytes_written": len(content.encode("utf-8"))},
            )
        except ToolError as e:
            return ToolOutput(success=False, data=None, error=str(e))
        except Exception as e:
            return ToolOutput(success=False, data=None, error=f"Error writing file: {e}")

    def _list_dir(self, inputs: dict) -> ToolOutput:
        """List directory contents.

        Args:
            inputs: Must contain 'path' key. Optional 'pattern' key for glob filtering

        Returns:
            ToolOutput with directory listing
        """
        if "path" not in inputs:
            return ToolOutput(success=False, data=None, error="Missing 'path' in inputs")

        try:
            path = self._resolve_path(inputs["path"])

            if not path.is_dir():
                return ToolOutput(
                    success=False,
                    data=None,
                    error=f"Path is not a directory: {inputs['path']}",
                )

            pattern = inputs.get("pattern", "*")

            # Get all entries matching the pattern
            entries = []
            for entry in path.iterdir():
                if fnmatch.fnmatch(entry.name, pattern):
                    entries.append(
                        {
                            "name": entry.name,
                            "path": str(entry.relative_to(self.workspace_root)),
                            "is_dir": entry.is_dir(),
                            "is_file": entry.is_file(),
                            "size": entry.stat().st_size if entry.is_file() else None,
                        }
                    )

            return ToolOutput(
                success=True,
                data={"path": str(path), "entries": entries, "count": len(entries)},
            )
        except ToolError as e:
            return ToolOutput(success=False, data=None, error=str(e))
        except FileNotFoundError:
            return ToolOutput(success=False, data=None, error=f"Directory not found: {inputs['path']}")
        except PermissionError:
            return ToolOutput(success=False, data=None, error=f"Permission denied: {inputs['path']}")
        except Exception as e:
            return ToolOutput(success=False, data=None, error=f"Error listing directory: {e}")
