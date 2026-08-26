from tools import (
    CloseAppTool,
    CreateFileTool,
    DeleteFileTool,
    ListFilesTool,
    OpenAppTool,
    ReadFileTool,
    SystemInfoTool,
    Tool,
    ToolManager,
    ToolRegistry,
    ToolResult,
    WriteFileTool,
    RenameFileTool,
)


class TestTool(Tool):
    name = "test_tool"
    description = "A simple tool used to test the tool system."

    def execute(self, **kwargs):
        return ToolResult.ok("Test tool executed successfully.")


def main():
    registry = ToolRegistry()

    # Register tools
    registry.register(TestTool())
    registry.register(SystemInfoTool())
    registry.register(OpenAppTool())
    registry.register(CloseAppTool())
    registry.register(ListFilesTool())
    registry.register(ReadFileTool())
    registry.register(CreateFileTool())
    registry.register(WriteFileTool())
    registry.register(DeleteFileTool())
    registry.register(RenameFileTool())

    # Verify registration
    tools = registry.list_tools()

    assert "test_tool" in tools
    assert "system_info" in tools
    assert "open_app" in tools
    assert "close_app" in tools
    assert "list_files" in tools
    assert "read_file" in tools
    assert "create_file" in tools
    assert "write_file" in tools
    assert "delete_file" in tools
    assert "rename_file" in registry.list_tools()


    # Verify test tool execution
    result = registry.execute("test_tool")

    assert result.success is True
    assert result.message == "Test tool executed successfully."

    # Verify system information tool
    system_result = registry.execute("system_info")

    assert system_result.success is True
    assert isinstance(system_result.data, dict)

    required_fields = [
        "operating_system",
        "os_version",
        "computer_name",
        "architecture",
        "processor",
        "python_version",
    ]

    for field in required_fields:
        assert field in system_result.data

    # Verify open_app validation
    result = registry.execute("open_app")

    assert result.success is False
    assert "No application was specified" in result.message

    result = registry.execute(
        "open_app",
        app="unknown_application",
    )

    assert result.success is False
    assert "not approved" in result.message

    # Verify close_app validation
    result = registry.execute("close_app")

    assert result.success is False
    assert "No application was specified" in result.message

    result = registry.execute(
        "close_app",
        app="unknown_application",
    )

    assert result.success is False
    assert "not approved" in result.message

    # Verify list_files validation
    result = registry.execute("list_files")

    assert result.success is False
    assert "No directory path was specified" in result.message

    # Verify nonexistent directory
    result = registry.execute(
        "list_files",
        path="this_directory_should_not_exist_jarvis_test",
    )

    assert result.success is False
    assert "does not exist" in result.message

    # Verify file path rejection
    result = registry.execute(
        "list_files",
        path="tools\\list_files.py",
    )

    assert result.success is False
    assert "not a directory" in result.message

    # Verify read_file validation
    result = registry.execute("read_file")

    assert result.success is False
    assert "No file path was specified" in result.message

    # Verify nonexistent file
    result = registry.execute(
        "read_file",
        path="this_file_should_not_exist_jarvis_test.txt",
    )

    assert result.success is False
    assert "does not exist" in result.message

    # Verify directory rejection
    result = registry.execute(
        "read_file",
        path="tools",
    )

    assert result.success is False
    assert "not a file" in result.message

    # Verify protected path rejection
    result = registry.execute(
        "read_file",
        path=".venv",
    )

    assert result.success is False
    assert "protected path" in result.message

    # Verify create_file validation
    result = registry.execute("create_file")

    assert result.success is False
    assert "No file path was specified" in result.message

    # Verify protected parent directory
    result = registry.execute(
        "create_file",
        path=".venv\\jarvis_test.txt",
        content="test",
    )

    assert result.success is False
    assert "protected path" in result.message

    # Verify nonexistent parent directory
    result = registry.execute(
        "create_file",
        path="this_directory_should_not_exist_jarvis_test\\file.txt",
        content="test",
    )

    assert result.success is False
    assert "Parent directory does not exist" in result.message

    # Verify write_file validation
    result = registry.execute("write_file")

    assert result.success is False
    assert "No file path was specified" in result.message

    # Verify nonexistent file
    result = registry.execute(
        "write_file",
        path="this_file_should_not_exist_jarvis_test.txt",
        content="test",
    )

    assert result.success is False
    assert "File does not exist" in result.message

    # Verify directory rejection
    result = registry.execute(
        "write_file",
        path="tools",
        content="test",
    )

    assert result.success is False
    assert "not a file" in result.message

    # Verify protected path rejection
    result = registry.execute(
        "write_file",
        path=".venv\\test.txt",
        content="test",
    )

    assert result.success is False
    assert "protected path" in result.message

    # Verify delete_file validation
    result = registry.execute("delete_file")

    assert result.success is False
    assert "No file path was specified" in result.message

    # Verify nonexistent file
    result = registry.execute(
        "delete_file",
        path="this_file_should_not_exist_jarvis_test.txt",
    )

    assert result.success is False
    assert "File does not exist" in result.message

    # Verify directory rejection
    result = registry.execute(
        "delete_file",
        path="tools",
    )

    assert result.success is False
    assert "not a file" in result.message

    # Verify protected path rejection
    result = registry.execute(
        "delete_file",
        path=".venv\\test.txt",
    )

    assert result.success is False
    assert "protected path" in result.message

    # Verify filesystem boundary protection
    result = registry.execute(
        "read_file",
        path="..\\README.md",
    )

    assert result.success is False
    assert "outside the approved directory" in result.message

    # Verify protected directory
    result = registry.execute(
        "read_file",
        path=".git\\config",
    )

    assert result.success is False
    assert "protected path" in result.message

    # Verify absolute path outside approved root
    result = registry.execute(
        "read_file",
        path="C:\\Windows\\System32\\drivers\\etc\\hosts",
    )

    assert result.success is False
    assert "outside the approved directory" in result.message

    # Verify missing source path
    result = registry.execute("rename_file")

    assert result.success is False
    assert "No file path was specified" in result.message

    # Verify missing new name
    result = registry.execute(
        "rename_file",
        path="tools\\list_files.py",
    )

    assert result.success is False
    assert "No new file name was specified" in result.message

    # Verify nonexistent source
    result = registry.execute(
        "rename_file",
        path="this_file_should_not_exist_jarvis_test.txt",
        new_name="renamed.txt",
    )

    assert result.success is False
    assert "File does not exist" in result.message

    # Verify directory rejection
    result = registry.execute(
        "rename_file",
        path="tools",
        new_name="renamed",
    )

    assert result.success is False
    assert "not a file" in result.message

    # Verify protected source
    result = registry.execute(
        "rename_file",
        path=".venv\\test.txt",
        new_name="renamed.txt",
    )

    assert result.success is False
    assert "protected path" in result.message

        # Verify destination path rejection
    result = registry.execute(
        "rename_file",
        path="tools\\list_files.py",
        new_name="..\\renamed.py",
    )

    assert result.success is False
    assert "New file name must be a file name, not a path." in result.message

    # Verify protected destination
    result = registry.execute(
        "rename_file",
        path="tools\\list_files.py",
        new_name=".git\\renamed.py",
    )

    assert result.success is False
    assert "New file name must be a file name, not a path." in result.message

    # Verify unknown tool handling
    result = registry.execute("does_not_exist")

    assert result.success is False
    assert "Unknown tool" in result.message

    # Verify centralized ToolManager
    manager = ToolManager()

    manager_tools = manager.list_tools()

    assert "system_info" in manager_tools
    assert "open_app" in manager_tools
    assert "close_app" in manager_tools
    assert "list_files" in manager_tools
    assert "read_file" in manager_tools
    assert "create_file" in manager_tools
    assert "write_file" in manager_tools
    assert "delete_file" in manager_tools
    assert "rename_file" in manager_tools

    # Verify manager execution
    result = manager.execute("system_info")

    assert result.success is True
    assert isinstance(result.data, dict)

    # Verify manager error handling
    result = manager.execute("does_not_exist")

    assert result.success is False
    assert "Unknown tool" in result.message

    print("Tool system verification passed.")
    print()
    print("System information:")
    print(system_result.message)


if __name__ == "__main__":
    main()