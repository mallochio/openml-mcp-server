# OpenML MCP Server

[![PyPI](https://img.shields.io/pypi/v/openml-mcp-server.svg)](https://pypi.org/project/openml-mcp-server/) <!-- Replace openml-mcp-server with your actual PyPI name -->
[![Python Versions](https://img.shields.io/pypi/pyversions/openml-mcp-server.svg)](https://pypi.org/project/openml-mcp-server/) <!-- Replace openml-mcp-server -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An MCP (Model Context Protocol) Server that allows AI models and agents (like Claude Desktop) to interact with the public [OpenML API](https://www.openml.org/apis).

This server exposes various OpenML API endpoints as MCP tools, enabling queries for datasets, tasks, flows, runs, and more directly from within an MCP-compatible client.

## Features

*   Provides MCP tools corresponding to major OpenML GET endpoints.
*   Query datasets, tasks, flows, runs, evaluations, setups, studies.
*   List entities with filtering capabilities (where supported by the API).
*   Built using the `mcp` Python SDK (`FastMCP`).

## Installation and Usage (for End Users)

These instructions explain how to use this server with an MCP client like Claude Desktop.

**Prerequisites:**

1.  **Claude Desktop:** Ensure you have the latest version installed ([Download here](https://claude.ai/download)).
2.  **`uv` (Python Package Installer):** This server is run using `uv`. Install it once if you don't have it:
    *   **macOS / Linux:**
        ```bash
        curl -LsSf https://astral.sh/uv/install.sh | sh
        ```
        *(Restart your terminal after installation)*
    *   **Windows (PowerShell):**
        ```powershell
        powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
        ```
        *(Restart your PowerShell terminal after installation)*

**Configuration:**

1.  **Edit Claude Desktop Config:**
    *   Open Claude Desktop -> Menu -> Settings... -> Developer -> Edit Config.
    *   This opens `claude_desktop_config.json`.

2.  **Add Server Configuration:**
    *   Add the following block inside the `mcpServers` object (create `mcpServers` if it doesn't exist):

        ```json
        {
          "mcpServers": {
            "openml-explorer": {
              "command": "uv",
              "args": [
                "run",
                // Make sure this matches the package name on PyPI
                "openml-mcp-server"
              ],
              "env": {
                // OPTIONAL: Add your OpenML API Key if needed for private access
                // Get your key from your OpenML profile page (https://www.openml.org/u)
                // "OPENML_API_KEY": "YOUR_ACTUAL_OPENML_API_KEY"
              }
            }
            // Add other servers here if you have them...
          }
        }
        ```
    *   **Replace** `"openml-mcp-server"` if you published under a different name.
    *   **Uncomment and replace** `"YOUR_ACTUAL_OPENML_API_KEY"` if needed. Most read operations are public and don't strictly require a key.

3.  **Save and Restart:**
    *   Save `claude_desktop_config.json`.
    *   **Completely quit and restart** Claude Desktop.

4.  **Verify:**
    *   Look for the hammer icon <img src="https://mintlify.s3.us-west-1.amazonaws.com/mcp/images/claude-desktop-mcp-hammer-icon.svg" style="display: inline; margin: 0; height: 1.3em;" /> in the Claude chat input.
    *   Click it to see the available "OpenML Explorer" tools (e.g., `get_dataset_description`, `list_tasks`).

**Example Usage in Claude:**

*   "Show the description for OpenML dataset ID 61."
*   "List features for dataset 31."
*   "Find the first 3 classification tasks on OpenML."
*   "Get the run description for run ID 100."

## Development

See the [Testing Instructions](#testing-instructions-for-developers) below.

## License

This project is licensed under the MIT License. See the LICENSE file for details.