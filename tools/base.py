from abc import ABC, abstractmethod
from typing import Any

from tools.result import ToolResult


class Tool(ABC):
    name: str
    description: str

    @abstractmethod
    def execute(self, **kwargs: Any) -> ToolResult:
        """Execute the tool."""
        raise NotImplementedError