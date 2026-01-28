"""Configuration management for OpenManus."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field


class Settings(BaseModel):
    """Application settings."""

    # API Configuration
    api_key: Optional[str] = Field(default=None, description="LLM API key")
    api_base: Optional[str] = Field(default=None, description="LLM API base URL")
    model: str = Field(default="deepseek/deepseek-chat", description="LLM model to use")

    # Workspace Configuration
    workspace_root: Path = Field(
        default_factory=lambda: Path.cwd(),
        description="Root directory for all file operations"
    )

    # Execution Configuration
    runs_dir: Path = Field(
        default_factory=lambda: Path.cwd() / "runs",
        description="Directory to store execution runs"
    )

    # Tool Configuration
    shell_whitelist: list[str] = Field(
        default_factory=lambda: ["ls", "cat", "grep", "wc", "head", "tail", "python3", "mkdir"],
        description="Allowed shell commands"
    )

    shell_blacklist: list[str] = Field(
        default_factory=lambda: ["rm", "mv", "sudo", "curl", "wget", "ssh", "chmod", "chown"],
        description="Forbidden shell commands"
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def load(cls) -> "Settings":
        """Load settings from environment variables."""
        load_dotenv()

        return cls(
            api_key=os.getenv("OPENMANUS_API_KEY") or os.getenv("DEEPSEEK_API_KEY"),
            api_base=os.getenv("OPENMANUS_API_BASE") or os.getenv("DEEPSEEK_API_BASE"),
            model=os.getenv("OPENMANUS_MODEL", "deepseek/deepseek-chat"),
        )


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings.load()
    return _settings


def reset_settings() -> None:
    """Reset global settings (useful for testing)."""
    global _settings
    _settings = None
