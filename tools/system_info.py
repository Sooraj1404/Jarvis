import platform
import socket
import sys

from tools.base import Tool
from tools.result import ToolResult


class SystemInfoTool(Tool):
    name = "system_info"
    description = "Get basic information about the current system."

    def execute(self, **kwargs):
        try:
            info = {
                "operating_system": platform.system(),
                "os_version": platform.version(),
                "computer_name": socket.gethostname(),
                "architecture": platform.machine(),
                "processor": platform.processor(),
                "python_version": sys.version.split()[0],
            }

            message = (
                f"Operating system: {info['operating_system']}\n"
                f"OS version: {info['os_version']}\n"
                f"Computer name: {info['computer_name']}\n"
                f"Architecture: {info['architecture']}\n"
                f"Processor: {info['processor']}\n"
                f"Python version: {info['python_version']}"
            )

            return ToolResult.ok(message, info)

        except Exception as exc:
            return ToolResult.error(
                f"Unable to retrieve system information: {exc}"
            )