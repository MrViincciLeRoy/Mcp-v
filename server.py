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

if __name__ == "__main__":
    # Run the server using HTTP transport for web deployment
    mcp.run(transport="http", host="0.0.0.0", port=8000)
