from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolCommand:
    """Represents a structured request to execute a JARVIS tool."""

    tool: str
    arguments: dict[str, Any] = field(default_factory=dict)