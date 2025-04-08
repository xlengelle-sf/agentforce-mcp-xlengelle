import httpx
import json
import logging
import uuid
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentforceClient:
    """Client for interacting with the Salesforce Agentforce API"""
    
    def __init__(self, server_url: str, client_id: str, client_secret: str, agent_id: str):
        self.server_url = server_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.agent_id = agent_id
        self.token_url = f"https://{server_url}/services/oauth2/token"
        self.api_url = "https://api.salesforce.com"
        
    async def get_access_token(self, client_email: str) -> Optional[Dict[str, str]]:
        """Get an access token for the Agentforce API"""
        try:
            payload = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'client_email': client_email
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(self.token_url, data=payload, headers=headers)
                response.raise_for_status()
                
                token_data = response.json()
                logger.info(f"✅ Token retrieved for {client_email}")
                
                return {
                    'client_email': client_email,
                    'access_token': token_data.get('access_token'),
                    'instance_url': token_data.get('instance_url')
                }
                
        except Exception as e:
            logger.error(f"❌ Error retrieving token: {str(e)}")
            return None
    
    async def create_session(self, token: str, instance_url: str) -> Optional[str]:
        """Create a session with the Agentforce API"""
        try:
            session_url = f"{self.api_url}/einstein/ai-agent/v1/agents/{self.agent_id}/sessions"
            
            random_uuid = str(uuid.uuid4())
            
            payload = {
                'externalSessionKey': random_uuid,
                'instanceConfig': {
                    'endpoint': instance_url
                },
                'streamingCapabilities': {
                    'chunkTypes': ['Text']
                },
                'bypassUser': True
            }
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(session_url, json=payload, headers=headers)
                response.raise_for_status()
                
                session_data = response.json()
                session_id = session_data.get('sessionId')
                
                if session_id:
                    logger.info(f"✅ Session Created, ID: {session_id}")
                    return session_id
                else:
                    logger.error("❌ No session ID in response")
                    return None
                    
        except Exception as e:
            logger.error(f"❌ Error creating session: {str(e)}")
            return None
    
    async def send_message(self, session_id: str, token: str, message: str, sequence_id: int = 1) -> Dict[str, Any]:
        """Send a message to the Agentforce API"""
        try:
            message_url = f"{self.api_url}/einstein/ai-agent/v1/sessions/{session_id}/messages"
            
            payload = {
                'message': {
                    'sequenceId': sequence_id,
                    'type': 'Text',
                    'text': message
                }
            }
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            logger.info(f"📤 Sending request with body: {json.dumps(payload)}")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(message_url, json=payload, headers=headers, timeout=120.0)
                response.raise_for_status()
                
                response_data = response.json()
                
                result = {
                    'session_id': session_id,
                    'sequence_id': sequence_id + 1,  # Increment sequence ID for next message
                    'agent_response': None
                }
                
                if 'messages' in response_data and response_data['messages']:
                    result['agent_response'] = response_data['messages'][0].get('message')
                else:
                    result['agent_response'] = 'No response message received'
                    
                return result
                
        except Exception as e:
            logger.error(f"❌ Error sending message: {str(e)}")
            return {
                'session_id': session_id,
                'sequence_id': sequence_id,
                'agent_response': f"Error sending message: {str(e)}"
            }
