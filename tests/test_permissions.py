from tools.permissions import (
    ToolPermission,
    get_tool_permission,
)


def test_read_tools():
    assert get_tool_permission("read_file") == ToolPermission.READ
    assert get_tool_permission("list_files") == ToolPermission.READ
    assert get_tool_permission("search_files") == ToolPermission.READ
    assert get_tool_permission("get_file_info") == ToolPermission.READ
    assert get_tool_permission("system_info") == ToolPermission.READ


def test_modify_tools():
    assert get_tool_permission("write_file") == ToolPermission.MODIFY
    assert get_tool_permission("create_file") == ToolPermission.MODIFY
    assert get_tool_permission("rename_file") == ToolPermission.MODIFY
    assert get_tool_permission("move_file") == ToolPermission.MODIFY
    assert get_tool_permission("create_directory") == ToolPermission.MODIFY


def test_destructive_tools():
    assert (
        get_tool_permission("delete_file")
        == ToolPermission.DESTRUCTIVE
    )

    assert (
        get_tool_permission("delete_directory")
        == ToolPermission.DESTRUCTIVE
    )


def test_unknown_tool():
    assert get_tool_permission("does_not_exist") is None


def main():
    test_read_tools()
    test_modify_tools()
    test_destructive_tools()
    test_unknown_tool()

    print("Permission verification passed.")


if __name__ == "__main__":
    main()