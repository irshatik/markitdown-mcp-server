from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import sys

PORT = int(os.environ.get('PORT', 8000))

class MCPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            request = json.loads(body)
            
            if request.get("method") == "list_tools":
                response = {
                    "tools": [{
                        "name": "convert_to_markdown",
                        "description": "Convert files to Markdown",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "file_path": {
                                    "type": "string",
                                    "description": "File path or URL"
                                }
                            },
                            "required": ["file_path"]
                        }
                    }]
                }
            
            elif request.get("method") == "call_tool":
                try:
                    from markitdown import MarkItDown
                    md = MarkItDown()
                    result = md.convert(request["params"]["file_path"])
                    response = {
                        "success": True,
                        "content": result.text_content[:5000]
                    }
                except Exception as e:
                    response = {"success": False, "error": str(e)}
            
            else:
                response = {"error": "Unknown method"}
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'MCP Server running')

    def log_message(self, *args):
        pass

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', PORT), MCPHandler)
    print(f"Server running on port {PORT}")
    sys.stdout.flush()
    server.serve_forever()
