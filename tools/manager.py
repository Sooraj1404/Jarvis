from tools.close_app import CloseAppTool
from tools.open_app import OpenAppTool
from tools.list_files import ListFilesTool
from tools.registry import ToolRegistry
from tools.result import ToolResult
from tools.system_info import SystemInfoTool
from tools.read_file import ReadFileTool
from tools.create_file import CreateFileTool
from tools.write_file import WriteFileTool
from tools.delete_file import DeleteFileTool
from tools.rename_file import RenameFileTool
from tools.move_file import MoveFileTool
from tools.search_files import SearchFilesTool
from tools.create_directory import CreateDirectoryTool
from tools.delete_directory import DeleteDirectoryTool
from tools.get_file_info import GetFileInfoTool
from tools.run_command import RunCommandTool

class ToolManager:
    def __init__(self):
        self.registry = ToolRegistry()
        self._register_tools()

    def _register_tools(self) -> None:
        self.registry.register(SystemInfoTool())
        self.registry.register(OpenAppTool())
        self.registry.register(CloseAppTool())
        self.registry.register(ListFilesTool())
        self.registry.register(ReadFileTool())
        self.registry.register(CreateFileTool())
        self.registry.register(WriteFileTool())
        self.registry.register(DeleteFileTool())
        self.registry.register(RenameFileTool())
        self.registry.register(MoveFileTool())
        self.registry.register(SearchFilesTool())
        self.registry.register(CreateDirectoryTool())
        self.registry.register(DeleteDirectoryTool())
        self.registry.register(GetFileInfoTool())
        self.registry.register(RunCommandTool())

    def execute(self, tool_name: str, **kwargs) -> ToolResult:
        return self.registry.execute(tool_name, **kwargs)

    def list_tools(self) -> list[str]:
        return self.registry.list_tools()