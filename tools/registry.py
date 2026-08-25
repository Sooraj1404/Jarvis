from typing import Dict

from tools.base import Tool
from tools.result import ToolResult


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(
                f"Tool '{tool.name}' is already registered."
            )

        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())

    def execute(self, name: str, **kwargs) -> ToolResult:
        tool = self.get(name)

        if tool is None:
            return ToolResult.error(
                f"Unknown tool: '{name}'."
            )

        try:
            return tool.execute(**kwargs)

        except Exception as exc:
            return ToolResult.error(
                f"Tool '{name}' failed: {exc}"
            )