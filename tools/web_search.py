from urllib.parse import urlparse

from ddgs import DDGS
from ddgs.exceptions import DDGSException, TimeoutException

from tools.base import Tool
from tools.result import ToolResult


class WebSearchTool(Tool):
    name = "web_search"
    description = "Search the web for information."

    MAX_RESULTS = 5
    TIMEOUT = 10

    def execute(
        self,
        query: str = "",
        max_results: int = MAX_RESULTS,
        **kwargs,
    ) -> ToolResult:
        query = query.strip()

        if not query:
            return ToolResult.error(
                "No web search query was specified."
            )

        if not isinstance(max_results, int):
            return ToolResult.error(
                "max_results must be an integer."
            )

        max_results = max(
            1,
            min(max_results, self.MAX_RESULTS),
        )

        try:
            results = DDGS(
                timeout=self.TIMEOUT
            ).text(
                query,
                region="in-en",
                safesearch="moderate",
                max_results=max_results,
                backend="auto",
            )

        except TimeoutException:
            return ToolResult.error(
                "The web search timed out."
            )

        except DDGSException as exc:
            return ToolResult.error(
                f"Web search failed: {exc}"
            )

        except Exception as exc:
            return ToolResult.error(
                f"Unable to perform web search: {exc}"
            )

        if not results:
            return ToolResult.ok(
                f"No web results were found for '{query}'.",
                {
                    "query": query,
                    "results": [],
                },
            )

        normalized_results = []

        for result in results:
            url = (
                result.get("href")
                or result.get("url")
                or ""
            )

            title = str(
                result.get("title") or ""
            ).strip()

            snippet = str(
                result.get("body") or ""
            ).strip()

            if not self._is_http_url(url):
                continue

            normalized_results.append(
                {
                    "title": title,
                    "url": url,
                    "snippet": snippet,
                    "source": urlparse(url).netloc,
                }
            )

        if not normalized_results:
            return ToolResult.ok(
                f"No usable web results were found "
                f"for '{query}'.",
                {
                    "query": query,
                    "results": [],
                },
            )

        return ToolResult.ok(
            f"Found {len(normalized_results)} "
            f"web result(s) for '{query}'.",
            {
                "query": query,
                "results": normalized_results,
            },
        )

    @staticmethod
    def _is_http_url(url: str) -> bool:
        try:
            parsed = urlparse(url)
        except ValueError:
            return False

        return (
            parsed.scheme in {"http", "https"}
            and bool(parsed.netloc)
        )