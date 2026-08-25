from tools.open_app import OpenAppTool
from tools.registry import ToolRegistry
from tools.result import ToolResult
from tools.system_info import SystemInfoTool


class ToolManager:
    def __init__(self):
        self.registry = ToolRegistry()
        self._register_tools()

    def _register_tools(self) -> None:
        self.registry.register(SystemInfoTool())
        self.registry.register(OpenAppTool())

    def execute(self, tool_name: str, **kwargs) -> ToolResult:
        return self.registry.execute(tool_name, **kwargs)

    def list_tools(self) -> list[str]:
        return self.registry.list_tools()