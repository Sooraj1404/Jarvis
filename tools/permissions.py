from enum import Enum


class ToolPermission(Enum):
    READ = "read"
    MODIFY = "modify"
    DESTRUCTIVE = "destructive"


TOOL_PERMISSIONS = {
    "system_info": ToolPermission.READ,
    "list_files": ToolPermission.READ,
    "read_file": ToolPermission.READ,
    "search_files": ToolPermission.READ,
    "get_file_info": ToolPermission.READ,

    "open_app": ToolPermission.MODIFY,
    "close_app": ToolPermission.MODIFY,
    "create_file": ToolPermission.MODIFY,
    "write_file": ToolPermission.MODIFY,
    "create_directory": ToolPermission.MODIFY,
    "rename_file": ToolPermission.MODIFY,
    "move_file": ToolPermission.MODIFY,

    "delete_file": ToolPermission.DESTRUCTIVE,
    "delete_directory": ToolPermission.DESTRUCTIVE,
}


def get_tool_permission(tool_name: str) -> ToolPermission | None:
    return TOOL_PERMISSIONS.get(tool_name)