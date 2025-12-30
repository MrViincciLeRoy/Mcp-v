# Viincci RAG MCP Server

A basic MCP (Model Context Protocol) server that responds with 'viincci_rag' to any prompt.

## Features

- Simple tool that responds with 'viincci_rag' to any input
- HTTP transport for web deployment
- Ready for deployment on Render

## Local Development

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd viincci-rag-mcp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running Locally

Run the server with:
```bash
python server.py
```

The server will start on `http://localhost:8000` and the MCP endpoint will be available at `http://localhost:8000/mcp`.

You can also use the FastMCP CLI:
```bash
fastmcp run server.py
```

Or with HTTP transport:
```bash
fastmcp run server.py --transport http
```

## Deployment on Render

### Step 1: Push to GitHub

1. Create a new GitHub repository
2. Push this code to your repository:
```bash
git init
git add .
git commit -m "Initial commit: viincci_rag MCP server"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: viincci-rag-mcp (or your preferred name)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server.py`
   - **Port**: 8000 (Render will set the PORT environment variable automatically)

5. Click "Create Web Service"

### Environment Variables (Optional)

If you need to use Render's dynamic port, update the server.py to use:
```python
import os
port = int(os.environ.get("PORT", 8000))
mcp.run(transport="http", host="0.0.0.0", port=port)
```

But the current configuration should work fine as is.

### Access Your Server

Once deployed, your MCP server will be available at:
```
https://your-service-name.onrender.com/mcp
```

## Testing the Server

You can test the server by connecting an MCP client to the endpoint, or use curl:

```bash
# Health check
curl https://your-service-name.onrender.com/health

# Test the MCP endpoint (requires MCP client)
# Your MCP client should connect to: https://your-service-name.onrender.com/mcp
```

## Server Details

- **Tool Name**: `query`
- **Input**: `prompt` (string) - any text input
- **Output**: Always returns the string `"viincci_rag"`

## Usage in Claude Desktop or MCP Client

Add this configuration to your MCP client:

```json
{
  "mcpServers": {
    "viincci_rag": {
      "url": "https://your-service-name.onrender.com/mcp",
      "transport": "http"
    }
  }
}
```

## License

MIT
