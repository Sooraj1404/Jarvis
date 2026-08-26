from tools.command import ToolCommand
from tools.executor import ToolExecutor


def test_none_command():
    executor = ToolExecutor()

    result = executor.execute(None)

    assert result.success is False
    assert "No tool command was provided" in result.message


def test_empty_tool_name():
    executor = ToolExecutor()

    command = ToolCommand(tool="")

    result = executor.execute(command)

    assert result.success is False
    assert "does not specify a tool" in result.message


def test_unknown_tool():
    executor = ToolExecutor()

    command = ToolCommand(
        tool="does_not_exist",
    )

    result = executor.execute(command)

    assert result.success is False
    assert "Unknown tool" in result.message


def test_system_info():
    executor = ToolExecutor()

    command = ToolCommand(
        tool="system_info",
    )

    result = executor.execute(command)

    assert result.success is True
    assert isinstance(result.data, dict)


def test_list_files():
    executor = ToolExecutor()

    command = ToolCommand(
        tool="list_files",
        arguments={
            "path": ".",
        },
    )

    result = executor.execute(command)

    assert result.success is True
    assert isinstance(result.data, dict)
    assert "entries" in result.data


def test_read_file():
    executor = ToolExecutor()

    command = ToolCommand(
        tool="read_file",
        arguments={
            "path": "README.md",
        },
    )

    result = executor.execute(command)

    assert result.success is True
    assert isinstance(result.data, dict)
    assert "content" in result.data


def main():
    tests = [
        test_none_command,
        test_empty_tool_name,
        test_unknown_tool,
        test_system_info,
        test_list_files,
        test_read_file,
    ]

    for test in tests:
        test()

    print("Tool executor verification passed.")


if __name__ == "__main__":
    main()