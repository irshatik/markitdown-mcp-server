import asyncio
import sys
from markitdown import MarkItDown
from mcp.server import Server

server = Server("markitdown-mcp-server")

@server.list_tools()
async def list_tools():
    return [
        {
            "name": "convert_to_markdown",
            "description": "Convert files to Markdown using MarkItDown",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to file or URL"
                    }
                },
                "required": ["file_path"]
            }
        }
    ]

@server.call_tool()
async def call_tool(name, arguments):
    if name == "convert_to_markdown":
        try:
            md = MarkItDown()
            result = md.convert(arguments["file_path"])
            return [{"type": "text", "text": result.text_content}]
        except Exception as e:
            return [{"type": "text", "text": f"Error: {str(e)}"}]
    return [{"type": "text", "text": "Unknown tool"}]

async def main():
    async with server:
        await server.wait_for_shutdown()

if __name__ == "__main__":
    asyncio.run(main())
