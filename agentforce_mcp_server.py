#!/usr/bin/env python3
from mcp.server.fastmcp import FastMCP
from typing import Dict, Optional, List, Any
import os
import logging
from dotenv import load_dotenv
from agentforce_client import AgentforceClient
from session_manager import SessionManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("agentforce-mcp-server")

# Initialize the Agentforce client
agentforce_client = AgentforceClient(
    server_url=os.getenv("SALESFORCE_SERVER_URL"),
    client_id=os.getenv("SALESFORCE_CLIENT_ID"),
    client_secret=os.getenv("SALESFORCE_CLIENT_SECRET"),
    agent_id=os.getenv("SALESFORCE_AGENT_ID")
)

# Initialize the session manager
session_manager = SessionManager()

@mcp.tool()
async def authenticate(client_email: str) -> str:
    """Authenticate with the Agentforce API and store the token.
    
    Args:
        client_email: Email of the client for authentication
    """
    token_response = await agentforce_client.get_access_token(client_email)
    
    if not token_response or not token_response.get('access_token'):
        return "Failed to authenticate. Please check the client email and try again."
    
    # Store token information
    session_manager.store_auth_info(client_email, token_response)
    
    return f"Successfully authenticated as {client_email}"

@mcp.tool()
async def create_agent_session(client_email: str) -> str:
    """Create a session with an Agentforce agent.
    
    Args:
        client_email: Email of the authenticated client
    """
    if not session_manager.is_authenticated(client_email):
        return "You need to authenticate first using the authenticate tool."
    
    token = session_manager.get_access_token(client_email)
    instance_url = session_manager.get_instance_url(client_email)
    
    session_id = await agentforce_client.create_session(token, instance_url)
    
    if not session_id:
        return "Failed to create session. Please try again."
    
    # Store session ID
    session_manager.store_session_id(client_email, session_id)
    
    return f"Successfully created session with agent. Session ID: {session_id}"

@mcp.tool()
async def send_message_to_agent(client_email: str, message: str) -> str:
    """Send a message to the Agentforce agent and get the response.
    
    Args:
        client_email: Email of the authenticated client
        message: Message to send to the agent
    """
    if not session_manager.is_authenticated(client_email):
        return "You need to authenticate first using the authenticate tool."
    
    if not session_manager.has_session(client_email):
        return "You need to create a session first using the create_agent_session tool."
    
    token = session_manager.get_access_token(client_email)
    session_id = session_manager.get_session_id(client_email)
    next_sequence_id = session_manager.get_next_sequence_id(client_email)
    
    response = await agentforce_client.send_message(
        session_id=session_id,
        token=token,
        message=message,
        sequence_id=next_sequence_id
    )
    
    # Update last sequence ID
    session_manager.update_sequence_id(client_email, response['sequence_id'])
    
    return response['agent_response']

@mcp.tool()
async def get_session_status(client_email: str) -> str:
    """Get the status of the current session.
    
    Args:
        client_email: Email of the authenticated client
    """
    return session_manager.get_session_status(client_email)

@mcp.tool()
async def complete_agentforce_conversation(client_email: str, user_query: str) -> str:
    """Complete full conversation flow with Agentforce - authenticate, create session, and send message.
    
    Args:
        client_email: Email of the client for authentication
        user_query: Message to send to the agent
    """
    # Step 1: Authenticate
    if not session_manager.is_authenticated(client_email):
        auth_result = await authenticate(client_email)
        if not "Successfully" in auth_result:
            return f"Authentication failed: {auth_result}"
        logger.info(f"Authentication successful for {client_email}")
    
    # Step 2: Create session
    if not session_manager.has_session(client_email):
        session_result = await create_agent_session(client_email)
        if not "Successfully" in session_result:
            return f"Session creation failed: {session_result}"
        logger.info("Session created successfully")
    
    # Step 3: Send message
    response = await send_message_to_agent(client_email, user_query)
    return response

if __name__ == "__main__":
    logger.info("Starting Agentforce MCP Server...")
    logger.info(f"Using Agent ID: {os.getenv('SALESFORCE_AGENT_ID')}")
    
    # Initialize and run the server
    mcp.run(transport='stdio')
