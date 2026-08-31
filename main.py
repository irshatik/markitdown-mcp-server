import os
from mcp.server.fastmcp import FastMCP
from markitdown import MarkItDown

mcp = FastMCP("markitdown-mcp-server", stateless_http=True)

@mcp.tool()
def convert_to_markdown(file_path: str) -> str:
    """Convert a file (by local path or URL) to Markdown text.

    Args:
        file_path: Path to a local file or a URL of the file to convert.
    """
    md = MarkItDown()
    result = md.convert(file_path)
    return result.text_content[:10000]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = port
    mcp.run(transport="streamable-http")
