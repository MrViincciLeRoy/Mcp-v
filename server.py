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
        "mcp_endpoint": "/sse",
        "health_endpoint": "/health",
        "version": "1.0.0"
    })

if __name__ == "__main__":
    # Get port from environment variable (for Render) or default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    # Use SSE transport (Server-Sent Events) which is standard for MCP over HTTP
    # The endpoint will be available at /sse
    mcp.run(transport="sse", host="0.0.0.0", port=port)
