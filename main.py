import sys
import asyncio
from markitdown import MarkItDown
from mcp.server.models import InitializationOptions
from mcp.server import Server
import mcp.types as types

server = Server("markitdown-mcp-server")

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="convert_to_markdown",
            description="Convert files to Markdown using MarkItDown",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to file or URL"
                    }
                },
                "required": ["file_path"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "convert_to_markdown":
        try:
            md = MarkItDown()
            result = md.convert(arguments["file_path"])
            return [types.TextContent(type="text", text=result.text_content)]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]
    return [types.TextContent(type="text", text="Unknown tool")]

async def main():
    async with server:
        await server.wait_for_shutdown()

if __name__ == "__main__":
    asyncio.run(main())
