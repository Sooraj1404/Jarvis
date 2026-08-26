from tools.command import ToolCommand
from tools.intent import ToolIntentDetector


detector = ToolIntentDetector()


def test_open_app():
    command = detector.detect("Open Notepad")

    assert command == ToolCommand(
        tool="open_app",
        arguments={
            "app": "Notepad",
        },
    )


def test_close_app():
    command = detector.detect("Close Calculator")

    assert command == ToolCommand(
        tool="close_app",
        arguments={
            "app": "Calculator",
        },
    )


def test_case_insensitive():
    command = detector.detect("OPEN Notepad")

    assert command == ToolCommand(
        tool="open_app",
        arguments={
            "app": "Notepad",
        },
    )


def test_list_files():
    command = detector.detect("List files")

    assert command == ToolCommand(
        tool="list_files",
        arguments={
            "path": ".",
        },
    )


def test_show_files():
    command = detector.detect("Show files")

    assert command == ToolCommand(
        tool="list_files",
        arguments={
            "path": ".",
        },
    )


def test_read_file():
    command = detector.detect("Read README.md.")

    assert command == ToolCommand(
        tool="read_file",
        arguments={
            "path": "README.md",
        },
    )


def test_create_file():
    command = detector.detect("Create file test.txt")

    assert command == ToolCommand(
        tool="create_file",
        arguments={
            "path": "test.txt",
            "content": "",
        },
    )


def test_write_file():
    command = detector.detect(
        "Write to test.txt with Hello JARVIS"
    )

    assert command == ToolCommand(
        tool="write_file",
        arguments={
            "path": "test.txt",
            "content": "Hello JARVIS",
        },
    )


def test_delete_file():
    command = detector.detect("Delete file test.txt")

    assert command == ToolCommand(
        tool="delete_file",
        arguments={
            "path": "test.txt",
        },
    )


def test_rename_file():
    command = detector.detect(
        "Rename test.txt to renamed.txt"
    )

    assert command == ToolCommand(
        tool="rename_file",
        arguments={
            "path": "test.txt",
            "new_name": "renamed.txt",
        },
    )


def test_move_file():
    command = detector.detect(
        "Move test.txt to docs/test.txt"
    )

    assert command == ToolCommand(
        tool="move_file",
        arguments={
            "path": "test.txt",
            "destination": "docs/test.txt",
        },
    )


def test_find_files():
    command = detector.detect(
        "Find Python files"
    )

    assert command == ToolCommand(
        tool="search_files",
        arguments={
            "query": "Python files",
            "path": ".",
        },
    )


def test_search_files():
    command = detector.detect(
        "Search for README"
    )

    assert command == ToolCommand(
        tool="search_files",
        arguments={
            "query": "README",
            "path": ".",
        },
    )


def test_create_directory():
    command = detector.detect(
        "Create directory Projects"
    )

    assert command == ToolCommand(
        tool="create_directory",
        arguments={
            "path": "Projects",
        },
    )


def test_create_folder():
    command = detector.detect(
        "Create folder Projects"
    )

    assert command == ToolCommand(
        tool="create_directory",
        arguments={
            "path": "Projects",
        },
    )


def test_delete_directory():
    command = detector.detect(
        "Delete directory Projects"
    )

    assert command == ToolCommand(
        tool="delete_directory",
        arguments={
            "path": "Projects",
        },
    )


def test_delete_folder():
    command = detector.detect(
        "Delete folder Projects"
    )

    assert command == ToolCommand(
        tool="delete_directory",
        arguments={
            "path": "Projects",
        },
    )


def test_get_file_info():
    command = detector.detect(
        "Get information about README.md"
    )

    assert command == ToolCommand(
        tool="get_file_info",
        arguments={
            "path": "README.md",
        },
    )

def test_write_file_preserves_punctuation():
    command = detector.detect(
        "Write to test.txt with Hello JARVIS."
    )

    assert command.arguments["content"] == "Hello JARVIS."

def test_get_file_info_short_form():
    command = detector.detect(
        "Get info about README.md"
    )

    assert command == ToolCommand(
        tool="get_file_info",
        arguments={
            "path": "README.md",
        },
    )


def test_empty_input():
    assert detector.detect("") is None


def test_whitespace_input():
    assert detector.detect("   ") is None


def test_non_tool_request():
    assert detector.detect(
        "What is the weather today?"
    ) is None


def test_normal_conversation():
    assert detector.detect(
        "That sounds interesting."
    ) is None


def main():
    tests = [
        test_open_app,
        test_close_app,
        test_case_insensitive,
        test_list_files,
        test_show_files,
        test_read_file,
        test_create_file,
        test_write_file,
        test_delete_file,
        test_rename_file,
        test_move_file,
        test_find_files,
        test_search_files,
        test_create_directory,
        test_create_folder,
        test_delete_directory,
        test_delete_folder,
        test_get_file_info,
        test_get_file_info_short_form,
        test_empty_input,
        test_whitespace_input,
        test_non_tool_request,
        test_normal_conversation,
    ]

    for test in tests:
        test()

    print("Tool intent verification passed.")


if __name__ == "__main__":
    main()