"""Base tool interface and registry."""

from abc import ABC, abstractmethod

from pydantic import BaseModel


class ToolInput(BaseModel):
    """Base model for tool inputs."""

    pass


class ToolOutput(BaseModel):
    """Base model for tool outputs."""

    success: bool
    data: dict | str | None
    error: str | None = None


class Tool(ABC):
    """Abstract base class for tools.

    A tool represents a unit of work that can be executed,
    such as reading a file or running a shell command.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this tool."""
        raise NotImplementedError

    @abstractmethod
    def execute(self, inputs: dict) -> ToolOutput:
        """Execute the tool with the given inputs.

        Args:
            inputs: A dictionary of input parameters

        Returns:
            A ToolOutput containing the result

        Raises:
            ToolError: If execution fails
        """
        raise NotImplementedError

    def validate_inputs(self, inputs: dict) -> None:
        """Validate inputs before execution.

        Args:
            inputs: The inputs to validate

        Raises:
            ValueError: If inputs are invalid
        """
        pass


class ToolError(Exception):
    """Exception raised when a tool fails."""

    pass


class ToolRegistry:
    """Registry for managing available tools.

    Tools can be registered and retrieved by name.
    """

    def __init__(self) -> None:
        """Initialize an empty tool registry."""
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """Register a tool.

        Args:
            tool: The tool to register

        Raises:
            ToolError: If a tool with the same name is already registered
        """
        name = tool.name
        if name in self._tools:
            raise ToolError(f"Tool '{name}' is already registered")
        self._tools[name] = tool

    def get(self, name: str) -> Tool | None:
        """Get a tool by name.

        Args:
            name: The name of the tool

        Returns:
            The tool if found, None otherwise
        """
        return self._tools.get(name)

    def list_tools(self) -> list[str]:
        """List all registered tool names.

        Returns:
            A list of tool names
        """
        return list(self._tools.keys())

    def has(self, name: str) -> bool:
        """Check if a tool is registered.

        Args:
            name: The name of the tool

        Returns:
            True if the tool is registered, False otherwise
        """
        return name in self._tools


# Global tool registry
_global_registry: ToolRegistry | None = None


def get_global_registry() -> ToolRegistry:
    """Get or create the global tool registry."""
    global _global_registry
    if _global_registry is None:
        _global_registry = ToolRegistry()
    return _global_registry


def reset_global_registry() -> None:
    """Reset the global tool registry (useful for testing)."""
    global _global_registry
    _global_registry = None
