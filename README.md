# Agentforce MCP Server

This MCP server provides tools to interact with the Salesforce Agentforce API. It allows authentication, session creation, and message exchange with Agentforce agents.

## Getting Started After Cloning

If you've just cloned this repository, follow these steps to set up and run the Agentforce MCP Server:

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your environment variables**:
   ```bash
   cp .env.example .env
   ```

3. **Collect your Salesforce credentials**:
   - **SALESFORCE_ORG_ID**: Your 18-character Salesforce Org ID
   - **SALESFORCE_AGENT_ID**: The 18-character Agent ID from your Agentforce agent
   - **SALESFORCE_CLIENT_ID**: The Consumer Key from your Connected App
   - **SALESFORCE_CLIENT_SECRET**: The Consumer Secret from your Connected App
   - **SALESFORCE_SERVER_URL**: Your Salesforce My Domain URL without https:// prefix

4. **Edit your .env file** with the collected credentials:
   ```
   SALESFORCE_ORG_ID="00D5f000000J2PKEA0"
   SALESFORCE_AGENT_ID="0XxHn000000x9F1KAI"
   SALESFORCE_CLIENT_ID="3MVG9OGq41FnYVsFgnaG0AzJDWnoy37Bb18e0R.GgDJu2qB9sqppVl7ehWmJhGvPSLrrA0cBNhDJdsbZXnv52"
   SALESFORCE_CLIENT_SECRET="210117AC36E9E4C8AFCA02FF062B8A677BACBFFB71D2BB1162D60D316382FADE"
   SALESFORCE_SERVER_URL="example.my.salesforce.com"
   ```
   (Note: These are fictional example values. Replace with your actual credentials.)

5. **Make the server script executable**:
   ```bash
   chmod +x agentforce_mcp_server.py
   ```

6. **Run the server**:
   ```bash
   python agentforce_mcp_server.py
   ```

For detailed instructions on finding your Salesforce credentials, see the [Setting Up Salesforce](#setting-up-salesforce) section below.

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

The server uses environment variables for configuration. These are loaded from the `.env` file.

1. Copy the example environment file to create your own:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and fill in your values:
   ```
   SALESFORCE_ORG_ID="your_org_id_here"
   SALESFORCE_AGENT_ID="your_agent_id_here"  # The 18-character Agent ID you found in Salesforce
   SALESFORCE_CLIENT_ID="your_client_id_here"  # The Consumer Key from your Connected App
   SALESFORCE_CLIENT_SECRET="your_client_secret_here"  # The Consumer Secret from your Connected App
   SALESFORCE_SERVER_URL="your_server_url_here"  # Your My Domain URL (e.g., example.my.salesforce.com)
   ```

## Salesforce Configuration

To use the Agentforce API, you need to:

1. Create a Connected App in your Salesforce org
2. Find your Agentforce Agent ID
3. Note your Salesforce My Domain URL

For detailed instructions on these steps, see the [Setting Up Salesforce](#setting-up-salesforce) section below.

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
        "/path/to/your/agentforce_mcp_server.py"
      ]
    }
  }
}
```

Replace the path with the absolute path to the server script on your machine.

### Path Locations by Platform

#### macOS
- Configuration file: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Example path: `/Users/yourusername/Projects/agentforce-mcp-server/agentforce_mcp_server.py`

#### Windows
- Configuration file: `%APPDATA%\Claude\claude_desktop_config.json`
- Example path: `C:\Users\yourusername\Projects\agentforce-mcp-server\agentforce_mcp_server.py`

## Setting Up Salesforce

### Creating a Connected App

To use the Agentforce API, you need to create a Connected App in your Salesforce org:

1. Log in to your Salesforce org as an administrator
2. Go to **Setup**
3. In the Quick Find box, search for "App Manager" and click on it
4. Click the **New Connected App** button
5. Fill in the basic information:
   - **Connected App Name**: Agentforce MCP Integration (or any name you prefer)
   - **API Name**: Agentforce_MCP_Integration (this will be auto-filled)
   - **Contact Email**: Your email address
6. Check **Enable OAuth Settings**
7. Set the **Callback URL** to `https://localhost/oauth/callback` (this is not used but required)
8. Under **Selected OAuth Scopes**, add:
   - Manage user data via APIs (api)
   - Perform requests at any time (refresh_token, offline_access)
9. Click **Save**
10. After saving, you'll be redirected to the Connected App detail page
11. Note the **Consumer Key** (this is your client ID) and click **Click to reveal** next to **Consumer Secret** to get your client secret

### Finding Your Agent ID

To find your Agentforce Agent ID:

1. Log in to your Salesforce org
2. Navigate to **Einstein Agent Builder**
3. Select the agent you want to use
4. Look at the URL in your browser - it will contain the Agent ID in the format: `https://your-salesforce-instance.lightning.force.com/lightning/r/Agent__c/0XxXXXXXXXXXXXXX/view` 
5. The Agent ID is that 18-character ID (`0XxXXXXXXXXXXXXX`) in the URL

### Finding Your Salesforce My Domain URL

To find your Salesforce My Domain URL:

1. Log in to your Salesforce org
2. Go to **Setup**
3. In the Quick Find box, search for "My Domain" and click on it
4. You'll see your domain in the format `DOMAIN-NAME.my.salesforce.com`
5. Use this URL without the "https://" prefix in your .env file

### Finding Your Org ID

To find your Salesforce Org ID:

1. Log in to your Salesforce org
2. Go to **Setup**
3. In the Quick Find box, search for "Company Information" and click on it
4. Look for the "Organization ID" field - this is your Salesforce Org ID
5. It will be a 15 or 18-character alphanumeric string

## Notes

- The server automatically manages sequence IDs for message exchanges
- Authentication and session state are maintained for each client email
- All API interactions are logged for debugging purposes

## Troubleshooting

If you encounter issues:

1. **Authentication failures**: Verify your Connected App settings and ensure the client ID and secret are correct
2. **Session creation errors**: Check your Agent ID and make sure it's the 18-character version
3. **Connection issues**: Verify your Salesforce My Domain URL is correct (without "https://" prefix)
4. **Permission errors**: Make sure your Connected App has the proper OAuth scopes enabled

## Testing the Setup

You can test your setup using the included test script:

```bash
python test_agentforce.py
```

This will attempt to authenticate, create a session, and exchange messages with your Agentforce agent.
