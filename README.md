⛑️ Work in Progress!

# OpenML MCP Server

[![PyPI](https://img.shields.io/pypi/v/openml-mcp-server.svg)](https://pypi.org/project/openml-mcp-server/)
[![Python Versions](https://img.shields.io/pypi/pyversions/openml-mcp-server.svg)](https://pypi.org/project/openml-mcp-server/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An MCP (Model Context Protocol) server that allows clients (like Claude Desktop) to interact with the public [OpenML API](https://www.openml.org/apis).

This server exposes various OpenML API endpoints as MCP tools, enabling queries for datasets, tasks, flows, runs, and more directly from within an MCP-compatible client.

## Table of Contents

- [Features](#features)
- [Installation and Usage](#installation-and-usage)
  - [For End Users](#for-end-users)
  - [For Developers](#for-developers)
- [Configuration](#configuration)
- [Examples](#examples)
- [Development](#development)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

## Features

* Provides MCP tools corresponding to major OpenML GET endpoints.
* Query datasets, tasks, flows, runs, evaluations, setups, studies.
* List entities with filtering capabilities (where supported by the API).
* Built using the `mcp` Python SDK (`FastMCP`).

## Installation and Usage

### For End Users

These instructions explain how to use this server with an MCP client like Claude Desktop.

**Prerequisites:**

1. **Claude Desktop:** Ensure you have the latest version installed ([Download here](https://claude.ai/download)).
2. **`uv` (Python Package Installer):** This server is run using `uv`. Install it once if you don't have it:
    - **macOS / Linux:**
        ```bash
        curl -LsSf https://astral.sh/uv/install.sh | sh
        ```
        *(Restart your terminal after installation)*
    - **Windows (PowerShell):**
        ```powershell
        powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
        ```
        *(Restart your PowerShell terminal after installation)*

### For Developers

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/your-repo/openml-mcp-server.git
    cd openml-mcp-server
    ```
2. **Install Dependencies:**
    ```bash
    uv sync
    ```

## Configuration

1. **Edit Claude Desktop Config:**
    - Open Claude Desktop -> Menu -> Settings... -> Developer -> Edit Config.
    - This opens `claude_desktop_config.json`.

2. **Add Server Configuration:**
    - Add the following block inside the `mcpServers` object (create `mcpServers` if it doesn't exist):

        ```json
        {
          "mcpServers": {
            "openml-explorer": {
              "command": "uv",
              "args": [
                "run",
                "openml-mcp-server"
              ],
              "env": {
                "OPENML_API_KEY": "YOUR_ACTUAL_OPENML_API_KEY"
              }
            }
          }
        }
        ```

3. **Save and Restart:**
    - Save `claude_desktop_config.json`.
    - **Completely quit and restart** Claude Desktop.

4. **Verify:**
    - Look for the hammer icon <img src="https://mintlify.s3.us-west-1.amazonaws.com/mcp/images/claude-desktop-mcp-hammer-icon.svg" style="display: inline; margin: 0; height: 1.3em;" /> in the Claude chat input.
    - Click it to see the available "OpenML Explorer" tools (e.g., `get_dataset_description`, `list_tasks`).

## Examples

- "Show the description for OpenML dataset ID 61."
- "List features for dataset 31."
- "Find the first 3 classification tasks on OpenML."
- "Get the run description for run ID 100."

## Development

See the [Testing Instructions](#testing-instructions-for-developers) below.

## Running Tests

To run the test suite (requires `pytest` and `pytest-asyncio`):

```bash
uv run pytest
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
