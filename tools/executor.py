from tools.command import ToolCommand
from tools.manager import ToolManager
from tools.result import ToolResult


class ToolExecutor:
    """Executes structured ToolCommand objects through ToolManager."""

    def __init__(self, manager: ToolManager | None = None):
        self.manager = manager or ToolManager()

    def execute(self, command: ToolCommand | None) -> ToolResult:
        if command is None:
            return ToolResult.error(
                "No tool command was provided."
            )

        if not command.tool.strip():
            return ToolResult.error(
                "Tool command does not specify a tool."
            )

        return self.manager.execute(
            command.tool,
            **command.arguments,
        )