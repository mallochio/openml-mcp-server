import sys
from .server import mcp 

def run_server():
    """Runs the MCP server."""
    print("Starting OpenML MCP Server via package entry point...")
    # Access configuration/API key from environment if needed here
    # Example: OPENML_API_KEY = os.environ.get("OPENML_API_KEY")
    # You might want to add logic here to pass config to your server setup if necessary
    from .tools import data  # Registers dataset tools
    mcp.run() 

if __name__ == "__main__":
    run_server()
