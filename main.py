import json
import sys
import os
from markitdown import MarkItDown

def handle_request(data):
    method = data.get("jsonrpc")
    if method != "2.0":
        return {"error": {"code": -32700, "message": "Parse error"}}
    
    req_method = data.get("method")
    params = data.get("params", {})
    
    if req_method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "result": {
                "tools": [{
                    "name": "convert_to_markdown",
                    "description": "Convert files to Markdown",
                    "inputSchema": {"type": "object", "properties": {"file_path": {"type": "string"}}, "required": ["file_path"]}
                }]
            }
        }
    
    elif req_method == "tools/call":
        try:
            md = MarkItDown()
            result = md.convert(params.get("file_path"))
            return {"jsonrpc": "2.0", "result": {"content": [{"type": "text", "text": result.text_content[:5000]}]}}
        except Exception as e:
            return {"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}
    
    return {"error": {"code": -32601, "message": "Method not found"}}

if __name__ == "__main__":
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            data = json.loads(line)
            response = handle_request(data)
            print(json.dumps(response))
            sys.stdout.flush()
        except:
            pass
