import os
from fastmcp import FastMCP
from starlette.responses import JSONResponse

# Initialize the MCP server
mcp = FastMCP(name="viincci_rag_server")

@mcp.tool()
def query(prompt: str) -> str:
    """
    Responds to any prompt with 'viincci_rag'.
    
    Args:
        prompt: Any text input or question
        
    Returns:
        Always returns 'viincci_rag'
    """
    print(f"Query received: {prompt}")
    return "viincci_rag"

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    """Health check endpoint for monitoring"""
    return JSONResponse({"status": "healthy", "service": "viincci_rag_server"})

@mcp.custom_route("/", methods=["GET"])
async def root(request):
    """Root endpoint with basic info"""
    return JSONResponse({
        "service": "viincci_rag_server",
        "status": "running",
        "transport": "http",
        "endpoints": {
            "mcp": "/mcp (POST - JSON-RPC)",
            "health": "/health (GET)",
            "root": "/ (GET)"
        },
        "version": "1.0.0",
        "note": "Send JSON-RPC requests to /mcp endpoint"
    })

# Manual MCP endpoint that handles all JSON-RPC calls
@mcp.custom_route("/mcp", methods=["POST"])
async def mcp_endpoint(request):
    """
    Main MCP endpoint that handles all JSON-RPC methods
    """
    try:
        data = await request.json()
        method = data.get("method")
        params = data.get("params", {})
        request_id = data.get("id", 1)
        
        print(f"Received request - Method: {method}, ID: {request_id}")
        
        # Handle initialize
        if method == "initialize":
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "viincci_rag_server",
                        "version": "1.0.0"
                    }
                }
            })
        
        # Handle tools/list
        elif method == "tools/list":
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": "query",
                            "description": "Responds to any prompt with 'viincci_rag'.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "prompt": {
                                        "type": "string",
                                        "description": "Any text input or question"
                                    }
                                },
                                "required": ["prompt"]
                            }
                        }
                    ]
                }
            })
        
        # Handle tools/call
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            print(f"Tool call - Name: {tool_name}, Arguments: {arguments}")
            
            if tool_name == "query":
                prompt = arguments.get("prompt", "")
                result = query(prompt)
                
                return JSONResponse({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": result
                            }
                        ]
                    }
                })
            else:
                return JSONResponse({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Tool not found: {tool_name}"
                    }
                }, status_code=404)
        
        # Handle notifications/initialized (optional but good to support)
        elif method == "notifications/initialized":
            # This is a notification, no response needed
            return JSONResponse({"jsonrpc": "2.0"})
        
        else:
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }, status_code=404)
            
    except Exception as e:
        print(f"Error processing request: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": data.get("id", 1) if 'data' in locals() else 1,
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        }, status_code=500)

if __name__ == "__main__":
    # Get port from environment variable (for Render) or default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    # Use HTTP transport
    print(f"Starting viincci_rag MCP server on port {port}")
    print(f"MCP endpoint: /mcp (POST)")
    print(f"Health endpoint: /health (GET)")
    
    mcp.run(transport="http", host="0.0.0.0", port=port)
