from unittest.mock import patch

from tools.command import ToolCommand
from tools.intent import ToolIntentDetector
from tools.web_search import WebSearchTool


def test_web_search_intent():
    detector = ToolIntentDetector()

    command = detector.detect(
        "Search the web for Python generators"
    )

    assert command == ToolCommand(
        tool="web_search",
        arguments={
            "query": "Python generators",
        },
    )


def test_web_search_intent_polite():
    detector = ToolIntentDetector()

    command = detector.detect(
        "Could you search online for Python 3.12?"
    )

    assert command == ToolCommand(
        tool="web_search",
        arguments={
            "query": "Python 3.12",
        },
    )


def test_empty_query():
    tool = WebSearchTool()

    result = tool.execute("")

    assert result.success is False
    assert "query" in result.message.lower()


@patch("tools.web_search.DDGS")
def test_web_search_normalizes_results(mock_ddgs):
    mock_ddgs.return_value.text.return_value = [
        {
            "title": "Python",
            "href": "https://www.python.org/",
            "body": "Official Python website.",
        }
    ]

    tool = WebSearchTool()

    result = tool.execute("Python")

    assert result.success is True

    assert result.data["query"] == "Python"

    assert result.data["results"] == [
        {
            "title": "Python",
            "url": "https://www.python.org/",
            "snippet": "Official Python website.",
            "source": "www.python.org",
        }
    ]


@patch("tools.web_search.DDGS")
def test_web_search_rejects_non_http_results(mock_ddgs):
    mock_ddgs.return_value.text.return_value = [
        {
            "title": "Bad result",
            "href": "javascript:alert(1)",
            "body": "Should not be accepted.",
        }
    ]

    tool = WebSearchTool()

    result = tool.execute("test")

    assert result.success is True
    assert result.data["results"] == []