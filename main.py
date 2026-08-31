import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get('PORT', 8000))

class MCPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            
            response = self.handle_request(data)
            
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

    def handle_request(self, request):
        method = request.get("method")
        
        if method == "initialize":
            return {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "markitdown-mcp-server", "version": "1.0.0"}}
        
        elif method == "tools/list":
            return {"tools": [{"name": "convert_to_markdown", "description": "Convert files to Markdown", "inputSchema": {"type": "object", "properties": {"file_path": {"type": "string"}}, "required": ["file_path"]}}]}
        
        elif method == "tools/call":
            try:
                from markitdown import MarkItDown
                md = MarkItDown()
                result = md.convert(request["params"]["file_path"])
                return {"content": [{"type": "text", "text": result.text_content[:5000]}]}
            except Exception as e:
                return {"error": str(e)}
        
        return {"error": "Unknown method"}

    def log_message(self, *args):
        pass

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', PORT), MCPHandler)
    print(f"Server running on port {PORT}")
    sys.stdout.flush()
    server.serve_forever()
