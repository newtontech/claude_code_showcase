"""Unit tests for Tools module."""

import tempfile
from pathlib import Path

import pytest

from openmanus.config import reset_settings
from openmanus.tools.base import ToolError, ToolOutput, ToolRegistry
from openmanus.tools.file_tool import FileTool
from openmanus.tools.shell_tool import ShellTool


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def reset_config():
    """Reset config before each test."""
    reset_settings()
    yield


class TestToolRegistry:
    """Tests for ToolRegistry."""

    def test_register_and_get_tool(self) -> None:
        """Test registering and retrieving a tool."""
        registry = ToolRegistry()
        tool = FileTool()

        registry.register(tool)
        assert registry.has("file")
        assert registry.get("file") is tool

    def test_register_duplicate_raises_error(self) -> None:
        """Test that registering a duplicate tool raises an error."""
        registry = ToolRegistry()
        tool1 = FileTool()
        tool2 = FileTool()

        registry.register(tool1)
        with pytest.raises(ToolError):
            registry.register(tool2)

    def test_list_tools(self) -> None:
        """Test listing registered tools."""
        registry = ToolRegistry()
        registry.register(FileTool())
        registry.register(ShellTool())

        tools = registry.list_tools()
        assert set(tools) == {"file", "shell"}

    def test_get_nonexistent_tool(self) -> None:
        """Test getting a tool that doesn't exist."""
        registry = ToolRegistry()
        assert registry.get("nonexistent") is None

    def test_global_registry(self) -> None:
        """Test the global tool registry."""
        from openmanus.tools.base import get_global_registry, reset_global_registry

        reset_global_registry()
        registry = get_global_registry()

        tool = FileTool()
        registry.register(tool)

        # Should get the same registry
        registry2 = get_global_registry()
        assert registry2.get("file") is tool


class TestFileTool:
    """Tests for FileTool."""

    def test_read_text_success(self, temp_workspace: str, reset_config) -> None:
        """Test successfully reading a text file."""
        # Create a test file
        test_file = Path(temp_workspace) / "test.txt"
        test_file.write_text("Hello, world!")

        tool = FileTool(workspace_root=temp_workspace)
        result = tool.execute({"action": "read_text", "path": "test.txt"})

        assert result.success is True
        assert result.data["content"] == "Hello, world!"

    def test_read_text_file_not_found(self, temp_workspace: str, reset_config) -> None:
        """Test reading a non-existent file."""
        tool = FileTool(workspace_root=temp_workspace)
        result = tool.execute({"action": "read_text", "path": "nonexistent.txt"})

        assert result.success is False
        assert "not found" in result.error.lower()

    def test_read_text_outside_workspace(self, temp_workspace: str, reset_config) -> None:
        """Test that reading outside workspace is blocked."""
        tool = FileTool(workspace_root=temp_workspace)
        result = tool.execute({"action": "read_text", "path": "/etc/passwd"})

        assert result.success is False
        assert "outside workspace" in result.error.lower()

    def test_write_text_overwrite(self, temp_workspace: str, reset_config) -> None:
        """Test writing/overwriting a text file."""
        tool = FileTool(workspace_root=temp_workspace)

        result = tool.execute(
            {
                "action": "write_text",
                "path": "out/test.txt",
                "content": "New content",
                "mode": "overwrite",
            }
        )

        assert result.success is True
        written_file = Path(temp_workspace) / "out" / "test.txt"
        assert written_file.read_text() == "New content"

    def test_write_text_append(self, temp_workspace: str, reset_config) -> None:
        """Test appending to a text file."""
        tool = FileTool(workspace_root=temp_workspace)

        # Write initial content
        tool.execute(
            {
                "action": "write_text",
                "path": "test.txt",
                "content": "Hello",
                "mode": "overwrite",
            }
        )

        # Append more content
        result = tool.execute(
            {
                "action": "write_text",
                "path": "test.txt",
                "content": " World",
                "mode": "append",
            }
        )

        assert result.success is True
        assert (Path(temp_workspace) / "test.txt").read_text() == "Hello World"

    def test_write_text_creates_directories(self, temp_workspace: str, reset_config) -> None:
        """Test that write_text creates parent directories."""
        tool = FileTool(workspace_root=temp_workspace)

        result = tool.execute(
            {
                "action": "write_text",
                "path": "deep/nested/path/test.txt",
                "content": "Content",
            }
        )

        assert result.success is True
        assert (Path(temp_workspace) / "deep" / "nested" / "path" / "test.txt").exists()

    def test_write_text_invalid_mode(self, temp_workspace: str, reset_config) -> None:
        """Test write_text with invalid mode."""
        tool = FileTool(workspace_root=temp_workspace)

        result = tool.execute(
            {
                "action": "write_text",
                "path": "test.txt",
                "content": "Content",
                "mode": "invalid",
            }
        )

        assert result.success is False
        assert "invalid mode" in result.error.lower()

    def test_list_dir(self, temp_workspace: str, reset_config) -> None:
        """Test listing directory contents."""
        # Create some test files
        (Path(temp_workspace) / "file1.txt").write_text("content1")
        (Path(temp_workspace) / "file2.txt").write_text("content2")
        (Path(temp_workspace) / "subdir").mkdir()

        tool = FileTool(workspace_root=temp_workspace)
        result = tool.execute({"action": "list_dir", "path": "."})

        assert result.success is True
        entries = result.data["entries"]
        assert len(entries) == 3

    def test_list_dir_with_pattern(self, temp_workspace: str, reset_config) -> None:
        """Test listing directory with pattern filter."""
        (Path(temp_workspace) / "test1.txt").write_text("content1")
        (Path(temp_workspace) / "test2.md").write_text("content2")
        (Path(temp_workspace) / "other.txt").write_text("content3")

        tool = FileTool(workspace_root=temp_workspace)
        result = tool.execute({"action": "list_dir", "path": ".", "pattern": "test*.txt"})

        assert result.success is True
        entries = result.data["entries"]
        assert len(entries) == 1
        assert entries[0]["name"] == "test1.txt"

    def test_list_dir_not_a_directory(self, temp_workspace: str, reset_config) -> None:
        """Test listing a file instead of directory."""
        (Path(temp_workspace) / "file.txt").write_text("content")

        tool = FileTool(workspace_root=temp_workspace)
        result = tool.execute({"action": "list_dir", "path": "file.txt"})

        assert result.success is False
        assert "not a directory" in result.error.lower()

    def test_unknown_action(self, temp_workspace: str, reset_config) -> None:
        """Test unknown action returns error."""
        tool = FileTool(workspace_root=temp_workspace)
        result = tool.execute({"action": "unknown"})

        assert result.success is False
        assert "unknown action" in result.error.lower()


class TestShellTool:
    """Tests for ShellTool."""

    def test_execute_whitelisted_command(self, reset_config) -> None:
        """Test executing a whitelisted command."""
        tool = ShellTool()
        result = tool.execute({"cmd": "ls /"})

        assert result.success is True
        assert len(result.data["stdout"]) > 0

    def test_execute_blacklisted_command(self, reset_config) -> None:
        """Test that blacklisted commands are rejected."""
        tool = ShellTool()
        result = tool.execute({"cmd": "rm -rf /tmp/test"})

        assert result.success is False
        assert "not allowed" in result.error.lower()

    def test_execute_non_whitelisted_command(self, reset_config) -> None:
        """Test that non-whitelisted commands are rejected."""
        tool = ShellTool()
        result = tool.execute({"cmd": "nonexistentcommand"})

        assert result.success is False
        assert "not in the allowed list" in result.error.lower()

    def test_execute_with_timeout(self, reset_config) -> None:
        """Test command execution with timeout."""
        tool = ShellTool()
        result = tool.execute({"cmd": "python3 -c 'import time; time.sleep(0.1)'", "timeout": 5})

        assert result.success is True

    def test_execute_dangerous_pattern(self, reset_config) -> None:
        """Test that dangerous patterns are blocked."""
        tool = ShellTool()
        result = tool.execute({"cmd": "python3 -c 'print(\"test\")' | dd if=/dev/zero of=/dev/null"})

        assert result.success is False
        assert "dangerous pattern" in result.error.lower()

    def test_custom_whitelist(self, reset_config) -> None:
        """Test custom whitelist."""
        tool = ShellTool(whitelist=["ls", "cat"])

        # Whitelisted command should work
        result = tool.execute({"cmd": "ls /"})
        assert result.success is True

        # Non-whitelisted command should fail
        result = tool.execute({"cmd": "wc -l"})
        assert result.success is False

    def test_custom_blacklist(self, reset_config) -> None:
        """Test custom blacklist."""
        tool = ShellTool(blacklist=["ls"])

        result = tool.execute({"cmd": "ls /"})
        assert result.success is False
        assert "not allowed" in result.error.lower()

    def test_missing_cmd(self, reset_config) -> None:
        """Test that missing 'cmd' key returns error."""
        tool = ShellTool()
        result = tool.execute({})

        assert result.success is False
        assert "missing" in result.error.lower()

    def test_python3_command(self, reset_config) -> None:
        """Test running Python inline script."""
        tool = ShellTool()
        result = tool.execute({"cmd": 'python3 -c "print(42)"'})

        assert result.success is True
        assert "42" in result.data["stdout"]

    def test_grep_command(self, reset_config) -> None:
        """Test running grep command."""
        tool = ShellTool()
        # Use printf instead of echo since echo might not be in whitelist
        result = tool.execute({"cmd": "python3 -c 'print(\"hello world\")' | grep world"})

        assert result.success is True
        assert "world" in result.data["stdout"]

    def test_command_failure(self, reset_config) -> None:
        """Test that non-zero return code is handled."""
        tool = ShellTool()
        result = tool.execute({"cmd": "ls /nonexistent_directory_12345"})

        assert result.success is False
        assert result.data["return_code"] != 0
