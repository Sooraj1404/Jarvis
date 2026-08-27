import subprocess

from tools.base import Tool
from tools.result import ToolResult


class RunCommandTool(Tool):
    name = "run_command"
    description = "Run a restricted allowlisted system command."

    ALLOWED_COMMANDS = {
        ("git", "status"),
        ("git", "branch"),
        ("git", "log"),
        ("python", "--version"),
    }

    def execute(
        self,
        command: str = "",
        arguments: list[str] | None = None,
        **kwargs,
    ) -> ToolResult:
        command = command.strip()

        if not command:
            return ToolResult.error(
                "No command was specified."
            )

        arguments = arguments or []

        if not isinstance(arguments, list):
            return ToolResult.error(
                "Command arguments must be a list."
            )

        if not all(
            isinstance(argument, str)
            for argument in arguments
        ):
            return ToolResult.error(
                "Command arguments must be strings."
            )

        command_key = (
            command.lower(),
            *[argument.lower() for argument in arguments],
        )

        if command_key not in self.ALLOWED_COMMANDS:
            return ToolResult.error(
                f"Command is not approved: "
                f"'{command} {' '.join(arguments)}'."
            )

        try:
            result = subprocess.run(
                [command, *arguments],
                capture_output=True,
                text=True,
                timeout=10,
                shell=False,
                check=False,
            )

        except (OSError, subprocess.SubprocessError) as exc:
            return ToolResult.error(
                f"Unable to execute command: {exc}"
            )

        output = result.stdout.strip()
        error = result.stderr.strip()

        if result.returncode != 0:
            return ToolResult.error(
                f"Command failed with exit code "
                f"{result.returncode}.",
                {
                    "command": command,
                    "arguments": arguments,
                    "stdout": output,
                    "stderr": error,
                    "return_code": result.returncode,
                },
            )

        return ToolResult.ok(
            f"Command executed successfully: "
            f"'{command} {' '.join(arguments)}'.",
            {
                "command": command,
                "arguments": arguments,
                "stdout": output,
                "stderr": error,
                "return_code": result.returncode,
            },
        )