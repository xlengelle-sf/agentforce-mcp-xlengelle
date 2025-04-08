from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class SessionManager:
    """Manages Agentforce sessions and sequence IDs"""
    
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        
    def store_auth_info(self, client_email: str, token_info: Dict[str, str]) -> None:
        """Store authentication information for a client"""
        self.sessions[client_email] = {
            'access_token': token_info.get('access_token'),
            'instance_url': token_info.get('instance_url'),
            'session_id': None,
            'last_sequence_id': 0
        }
        
    def store_session_id(self, client_email: str, session_id: str) -> None:
        """Store session ID for a client"""
        if client_email in self.sessions:
            self.sessions[client_email]['session_id'] = session_id
            self.sessions[client_email]['last_sequence_id'] = 0
        else:
            logger.error(f"❌ Client email {client_email} not found in sessions")
            
    def update_sequence_id(self, client_email: str, sequence_id: int) -> None:
        """Update sequence ID for a client"""
        if client_email in self.sessions:
            self.sessions[client_email]['last_sequence_id'] = sequence_id
        else:
            logger.error(f"❌ Client email {client_email} not found in sessions")
            
    def get_next_sequence_id(self, client_email: str) -> int:
        """Get next sequence ID for a client"""
        if client_email in self.sessions:
            return self.sessions[client_email]['last_sequence_id'] + 1
        else:
            logger.error(f"❌ Client email {client_email} not found in sessions")
            return 1  # Default to 1 if not found
            
    def get_access_token(self, client_email: str) -> Optional[str]:
        """Get access token for a client"""
        if client_email in self.sessions:
            return self.sessions[client_email].get('access_token')
        else:
            logger.error(f"❌ Client email {client_email} not found in sessions")
            return None
            
    def get_instance_url(self, client_email: str) -> Optional[str]:
        """Get instance URL for a client"""
        if client_email in self.sessions:
            return self.sessions[client_email].get('instance_url')
        else:
            logger.error(f"❌ Client email {client_email} not found in sessions")
            return None
            
    def get_session_id(self, client_email: str) -> Optional[str]:
        """Get session ID for a client"""
        if client_email in self.sessions:
            return self.sessions[client_email].get('session_id')
        else:
            logger.error(f"❌ Client email {client_email} not found in sessions")
            return None
            
    def get_session_status(self, client_email: str) -> str:
        """Get session status for a client"""
        if client_email not in self.sessions:
            return "No active session. You need to authenticate first."
        
        session_info = self.sessions[client_email]
        
        status = f"Client Email: {client_email}\n"
        status += f"Authenticated: {'Yes' if session_info.get('access_token') else 'No'}\n"
        status += f"Session ID: {session_info.get('session_id') or 'Not created'}\n"
        status += f"Last Sequence ID: {session_info.get('last_sequence_id', 0)}\n"
        
        return status
            
    def is_authenticated(self, client_email: str) -> bool:
        """Check if a client is authenticated"""
        return client_email in self.sessions and self.sessions[client_email].get('access_token') is not None
        
    def has_session(self, client_email: str) -> bool:
        """Check if a client has a session"""
        return client_email in self.sessions and self.sessions[client_email].get('session_id') is not None
