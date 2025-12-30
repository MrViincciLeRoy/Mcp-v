import os
from fastmcp import FastMCP

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
    print(f"Query received: {prompt}")  # Log for debugging
    return "viincci_rag"

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    """Health check endpoint for monitoring"""
    from starlette.responses import JSONResponse
    return JSONResponse({"status": "healthy", "service": "viincci_rag_server"})

@mcp.custom_route("/", methods=["GET"])
async def root(request):
    """Root endpoint with basic info"""
    from starlette.responses import JSONResponse
    return JSONResponse({
        "service": "viincci_rag_server",
        "status": "running",
        "mcp_endpoints": {
            "sse": "/sse (GET to establish connection, then send JSON-RPC via the stream)",
            "messages": "/messages (POST for direct JSON-RPC calls)"
        },
        "other_endpoints": {
            "health": "/health",
            "root": "/"
        },
        "version": "1.0.0",
        "note": "This is an MCP server. Use an MCP client or the /messages endpoint for JSON-RPC calls."
    })

# Add a custom endpoint for easier testing with POST
@mcp.custom_route("/messages", methods=["POST"])
async def messages_endpoint(request):
    """
    Direct JSON-RPC endpoint (non-streaming)
    This makes testing easier without needing SSE
    """
    from starlette.responses import JSONResponse
    import json
    
    try:
        data = await request.json()
        method = data.get("method")
        params = data.get("params", {})
        request_id = data.get("id", 1)
        
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
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": 1,
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        }, status_code=500)

if __name__ == "__main__":
    # Get port from environment variable (for Render) or default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    # Use SSE transport (Server-Sent Events) which is standard for MCP over HTTP
    # The endpoint will be available at /sse (GET to connect)
    # But we also have /messages (POST) for easier testing
    mcp.run(transport="sse", host="0.0.0.0", port=port)
