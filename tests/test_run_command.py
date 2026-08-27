from tools.run_command import RunCommandTool


def main():
    tool = RunCommandTool()

    result = tool.execute(
        command="git",
        arguments=["status"],
    )

    assert result.success is True
    assert result.data["return_code"] == 0

    result = tool.execute(
        command="python",
        arguments=["--version"],
    )

    assert result.success is True
    assert result.data["return_code"] == 0

    result = tool.execute(
        command="del",
        arguments=["important.txt"],
    )

    assert result.success is False
    assert "not approved" in result.message

    result = tool.execute(
        command="git",
        arguments=["status", "--porcelain", "&&", "del"],
    )

    assert result.success is False
    assert "not approved" in result.message

    result = tool.execute(
        command="",
        arguments=[],
    )

    assert result.success is False
    assert "No command was specified" in result.message

    print("Run command verification passed.")


if __name__ == "__main__":
    main()