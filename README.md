# Agentforce MCP Server

This MCP server provides tools to interact with the Salesforce Agentforce API. It allows authentication, session creation, and message exchange with Agentforce agents.

Repository: [https://github.com/xlengelle-sf/agentforce-mcp-server-xlengelle](https://github.com/xlengelle-sf/agentforce-mcp-server-xlengelle)

## Setup

1. Ensure you have Python 3.10 or higher installed.

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Make the server script executable:
   ```bash
   chmod +x agentforce_mcp_server.py
   ```

## Configuration

The server uses environment variables for configuration. These are loaded from the `.env` file. Make sure the following variables are set:

- `SALESFORCE_SERVER_URL`: The Salesforce instance URL
- `SALESFORCE_CLIENT_ID`: The client ID from the Salesforce connected app
- `SALESFORCE_CLIENT_SECRET`: The client secret from the Salesforce connected app
- `SALESFORCE_AGENT_ID`: The ID of the Agentforce agent

## Running the Server

Run the server using:

```bash
python agentforce_mcp_server.py
```

## Available Tools

The MCP server exposes the following tools:

### 1. `authenticate`

Authenticates with the Agentforce API using a client email.

Parameters:
- `client_email`: Email of the client for authentication

### 2. `create_agent_session`

Creates a session with the configured Agentforce agent.

Parameters:
- `client_email`: Email of the authenticated client

### 3. `send_message_to_agent`

Sends a message to the Agentforce agent and returns the response.

Parameters:
- `client_email`: Email of the authenticated client
- `message`: Message to send to the agent

### 4. `get_session_status`

Gets the status of the current session, including authentication status, session ID, and sequence ID.

Parameters:
- `client_email`: Email of the authenticated client

### 5. `complete_agentforce_conversation`

Convenience method that handles the complete flow - authentication, session creation, and message sending.

Parameters:
- `client_email`: Email of the client for authentication
- `user_query`: Message to send to the agent

## Using with Claude for Desktop

To use this server with Claude for Desktop, update your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "agentforce": {
      "command": "python",
      "args": [
        "/Users/xlengelle/Code/Claude-MCP/XL_MCP2/agentforce_mcp_server.py"
      ]
    }
  }
}
```

Replace the path with the absolute path to the server script on your machine.

## Notes

- The server automatically manages sequence IDs for message exchanges
- Authentication and session state are maintained for each client email
- All API interactions are logged for debugging purposes
