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
        "transport": "http",
        "mcp_endpoint": "/mcp/v1",
        "health_endpoint": "/health",
        "version": "1.0.0",
        "note": "Using HTTP transport for MCP JSON-RPC calls"
    })

if __name__ == "__main__":
    # Get port from environment variable (for Render) or default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    # Use HTTP transport instead of SSE
    # This creates a standard HTTP endpoint for JSON-RPC
    print(f"Starting server on port {port} with HTTP transport")
    mcp.run(transport="http", host="0.0.0.0", port=port)
