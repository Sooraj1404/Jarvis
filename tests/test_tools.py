from tools import (
    CloseAppTool,
    OpenAppTool,
    SystemInfoTool,
    Tool,
    ToolManager,
    ToolRegistry,
    ToolResult,
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

    # Verify registration
    tools = registry.list_tools()

    assert "test_tool" in tools
    assert "system_info" in tools
    assert "open_app" in tools
    assert "close_app" in tools

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