#!/usr/bin/env python3
import httpx
import asyncio
import os
from dotenv import load_dotenv
from agentforce_client import AgentforceClient

async def test_agentforce_api():
    """Test the Agentforce API directly"""
    # Load environment variables
    load_dotenv()
    
    # Create client
    client = AgentforceClient(
        server_url=os.getenv("SALESFORCE_SERVER_URL"),
        client_id=os.getenv("SALESFORCE_CLIENT_ID"),
        client_secret=os.getenv("SALESFORCE_CLIENT_SECRET"),
        agent_id=os.getenv("SALESFORCE_AGENT_ID")
    )
    
    # Test email to use
    test_email = "test@example.com"
    
    print(f"Testing Agentforce API with {test_email}")
    
    # Step 1: Get access token
    print("\n1. Getting access token...")
    token_response = await client.get_access_token(test_email)
    
    if not token_response or not token_response.get('access_token'):
        print("❌ Failed to get access token")
        return
    
    print(f"✅ Got access token: {token_response['access_token'][:10]}...")
    
    # Step 2: Create session
    print("\n2. Creating session...")
    session_id = await client.create_session(
        token=token_response['access_token'],
        instance_url=token_response['instance_url']
    )
    
    if not session_id:
        print("❌ Failed to create session")
        return
    
    print(f"✅ Created session with ID: {session_id}")
    
    # Step 3: Send message
    print("\n3. Sending test message...")
    message_response = await client.send_message(
        session_id=session_id,
        token=token_response['access_token'],
        message="Hello, can you help me find a hotel near CDG airport?",
        sequence_id=1
    )
    
    print(f"✅ Got response: {message_response['agent_response'][:100]}...")
    print(f"Next sequence ID: {message_response['sequence_id']}")
    
    # Step 4: Send follow-up message
    print("\n4. Sending follow-up message...")
    followup_response = await client.send_message(
        session_id=session_id,
        token=token_response['access_token'],
        message="I need a room for 2 people for tonight",
        sequence_id=message_response['sequence_id']
    )
    
    print(f"✅ Got response: {followup_response['agent_response'][:100]}...")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_agentforce_api())
