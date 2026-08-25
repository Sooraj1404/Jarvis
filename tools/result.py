from dataclasses import dataclass
from typing import Any


@dataclass
class ToolResult:
    success: bool
    message: str
    data: Any = None

    @classmethod
    def ok(cls, message: str, data: Any = None):
        return cls(
            success=True,
            message=message,
            data=data,
        )

    @classmethod
    def error(cls, message: str, data: Any = None):
        return cls(
            success=False,
            message=message,
            data=data,
        )