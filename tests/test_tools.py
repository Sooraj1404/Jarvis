from tools import (
    CloseAppTool,
    OpenAppTool,
    SystemInfoTool,
    Tool,
    ToolManager,
    ToolRegistry,
    ToolResult,
    ListFilesTool,
    ReadFileTool,
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

    # Verify registration
    tools = registry.list_tools()

    assert "test_tool" in tools
    assert "system_info" in tools
    assert "open_app" in tools
    assert "close_app" in tools
    assert "list_files" in registry.list_tools()
    assert "read_file" in registry.list_tools()


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


    # Verify missing path
    result = registry.execute("list_files")

    assert result.success is False
    assert "No directory path was specified" in result.message

    # Verify nonexistent path
    result = registry.execute(
        "list_files",
        path="C:\\this_directory_should_not_exist_jarvis_test",
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

    # Verify missing path
    result = registry.execute("read_file")

    assert result.success is False
    assert "No file path was specified" in result.message

    # Verify nonexistent file
    result = registry.execute(
        "read_file",
        path="C:\\this_file_should_not_exist_jarvis_test.txt",
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