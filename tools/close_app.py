import subprocess

from tools.base import Tool
from tools.result import ToolResult


class CloseAppTool(Tool):
    name = "close_app"
    description = "Close an approved application."

    APPLICATIONS = {
        "notepad": "notepad.exe",
        "calculator": "CalculatorApp.exe",
        "explorer": "explorer.exe",
    }

    def execute(self, app: str = "", **kwargs) -> ToolResult:
        app = app.strip().lower()

        if not app:
            return ToolResult.error(
                "No application was specified."
            )

        process_name = self.APPLICATIONS.get(app)

        if process_name is None:
            available = ", ".join(sorted(self.APPLICATIONS))

            return ToolResult.error(
                f"Application '{app}' is not approved. "
                f"Available applications: {available}."
            )

        try:
            result = subprocess.run(
                [
                    "taskkill",
                    "/IM",
                    process_name,
                ],
                capture_output=True,
                text=True,
                shell=False,
            )

            if result.returncode == 0:
                return ToolResult.ok(
                    f"Closed {app}.",
                    {
                        "application": app,
                        "process": process_name,
                    },
                )

            output = result.stdout.strip() or result.stderr.strip()

            if "not found" in output.lower():
                return ToolResult.error(
                    f"{app.capitalize()} is not currently running."
                )

            return ToolResult.error(
                f"Unable to close '{app}'."
            )
        except OSError as exc:
            return ToolResult.error(
                f"Unable to close '{app}': {exc}"
            )