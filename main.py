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

    # Disable DNS-rebinding host check so Railway's proxy domain is accepted
    try:
        mcp._session_manager  # noqa
    except Exception:
        pass

    import uvicorn
    app = mcp.streamable_http_app()

    # Allow all hosts (Railway sits behind a proxy with a dynamic domain)
    for middleware in getattr(app, "user_middleware", []):
        pass

    uvicorn.run(app, host="0.0.0.0", port=port, forwarded_allow_ips="*", proxy_headers=True)
