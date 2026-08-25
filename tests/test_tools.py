from tools import (
    OpenAppTool,
    SystemInfoTool,
    Tool,
    ToolManager,
    ToolRegistry,
    ToolResult,
)

def main():
    registry = ToolRegistry()

    # Register test tool
    registry.register(TestTool())

    # Register system information tool
    registry.register(SystemInfoTool())

    # Register open application tool
    registry.register(OpenAppTool())

    # Verify registration
    tools = registry.list_tools()

    assert "test_tool" in tools
    assert "system_info" in tools
    assert "open_app" in tools

    # ... your existing tests ...

    # Verify unknown tool handling
    result = registry.execute("does_not_exist")

    assert result.success is False
    assert "Unknown tool" in result.message

    # -------------------------------------------------
    # Verify centralized tool manager
    # -------------------------------------------------

    manager = ToolManager()

    manager_tools = manager.list_tools()

    assert "system_info" in manager_tools
    assert "open_app" in manager_tools

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