import subprocess

from tools.base import Tool
from tools.result import ToolResult


class OpenAppTool(Tool):
    name = "open_app"
    description = "Open an approved application."

    APPLICATIONS = {
        "notepad": ["notepad.exe"],
        "calculator": ["calc.exe"],
        "explorer": ["explorer.exe"],
        "chrome": [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        ],
    }

    def execute(self, app: str = "", **kwargs) -> ToolResult:
        app = app.strip().lower()

        if not app:
            return ToolResult.error(
                "No application was specified."
            )

        command = self.APPLICATIONS.get(app)

        if command is None:
            available = ", ".join(sorted(self.APPLICATIONS))

            return ToolResult.error(
                f"Application '{app}' is not approved. "
                f"Available applications: {available}."
            )

        try:
            subprocess.Popen(
                command,
                shell=False,
            )

            return ToolResult.ok(
                f"Opening {app}.",
                {
                    "application": app,
                },
            )

        except FileNotFoundError:
            return ToolResult.error(
                f"The application '{app}' could not be found."
            )

        except OSError as exc:
            return ToolResult.error(
                f"Unable to open '{app}': {exc}"
            )