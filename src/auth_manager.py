"""
Token management for WHOOP MCP Server
"""
import json
import os
import time
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import httpx
import logging

from config import (
    TOKEN_STORAGE_PATH,
    ENCRYPTION_KEY_FILE,
    OAUTH_TOKEN_URL,
    OAUTH_REFRESH_URL,
    REQUEST_TIMEOUT
)

logger = logging.getLogger(__name__)

class TokenManager:
    """Manages WHOOP OAuth tokens with encryption"""
    
    def __init__(self):
        self.storage_path = TOKEN_STORAGE_PATH
        self.key_file = ENCRYPTION_KEY_FILE
        self.encryption_key = self._get_or_create_key()
        self.fernet = Fernet(self.encryption_key)
        self.cipher_suite = self.fernet  # Alias for compatibility
        
        # Ensure storage directory exists
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        
    def _get_or_create_key(self) -> bytes:
        """Get or create encryption key"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            # Create new key
            key = Fernet.generate_key()
            os.makedirs(os.path.dirname(self.key_file), exist_ok=True)
            with open(self.key_file, 'wb') as f:
                f.write(key)
            os.chmod(self.key_file, 0o600)  # Restrict permissions
            return key
    
    def _encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        return self.fernet.encrypt(data.encode()).decode()
    
    def _decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        return self.fernet.decrypt(encrypted_data.encode()).decode()
    
    def save_tokens(self, tokens: Dict[str, Any]) -> None:
        """Save tokens to encrypted storage"""
        try:
            # Calculate expiration time
            expires_in = tokens.get('expires_in', 3600)  # Default 1 hour
            expires_at = datetime.now() + timedelta(seconds=expires_in)
            
            # Prepare data for storage
            token_data = {
                'access_token': self._encrypt_data(tokens['access_token']),
                'refresh_token': self._encrypt_data(tokens.get('refresh_token', '')),
                'token_type': tokens.get('token_type', 'Bearer'),
                'expires_at': expires_at.isoformat(),
                'created_at': datetime.now().isoformat()
            }
            
            # Save to file
            with open(self.storage_path, 'w') as f:
                json.dump(token_data, f, indent=2)
            
            # Restrict file permissions
            os.chmod(self.storage_path, 0o600)
            
            logger.info("Tokens saved successfully")
            
        except Exception as e:
            logger.error(f"Failed to save tokens: {e}")
            raise
    
    def load_tokens(self) -> Optional[Dict[str, Any]]:
        """Load and decrypt tokens from storage"""
        if not os.path.exists(self.storage_path):
            logger.warning("No tokens found")
            return None
        
        try:
            # Check if file is binary (new format) or text (old format)
            with open(self.storage_path, 'rb') as f:
                file_content = f.read()
            
            if file_content.startswith(b'gAAAAA'):  # Fernet encrypted format
                # New binary format
                decrypted_data = self.cipher_suite.decrypt(file_content)
                tokens = json.loads(decrypted_data.decode())
                return tokens
            else:
                # Old JSON format
                with open(self.storage_path, 'r') as f:
                    encrypted_data = json.load(f)
                
                # Decrypt tokens
                tokens = {
                    'access_token': self._decrypt_data(encrypted_data['access_token']),
                    'refresh_token': self._decrypt_data(encrypted_data['refresh_token']),
                    'token_type': encrypted_data.get('token_type', 'Bearer'),
                    'expires_at': encrypted_data['expires_at'],
                    'created_at': encrypted_data['created_at']
                }
                
                return tokens
            
        except Exception as e:
            logger.error(f"Failed to load tokens: {e}")
            return None
    
    def is_token_expired(self, tokens: Dict[str, Any]) -> bool:
        """Check if access token is expired"""
        try:
            expires_at = datetime.fromisoformat(tokens['expires_at'])
            # Consider token expired 5 minutes before actual expiration
            buffer_time = timedelta(minutes=5)
            return datetime.now() + buffer_time >= expires_at
        except Exception:
            return True
    
    def get_valid_access_token(self) -> Optional[str]:
        """Get valid access token, refreshing if necessary"""
        tokens = self.load_tokens()
        if not tokens:
            logger.warning("No tokens available")
            return None
        
        # Check if token is expired
        if not self.is_token_expired(tokens):
            return tokens['access_token']
        
        # Try to refresh token
        logger.info("Access token expired, attempting refresh")
        refreshed_tokens = self.refresh_tokens(tokens['refresh_token'])
        
        if refreshed_tokens:
            return refreshed_tokens['access_token']
        
        logger.error("Failed to refresh token")
        return None
    
    def refresh_tokens(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Refresh access token using refresh token"""
        try:
            import requests
            
            response = requests.post(
                OAUTH_REFRESH_URL,
                json={'refresh_token': refresh_token},
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                token_data = response.json()
                if token_data.get('success'):
                    # Save new tokens
                    self.save_tokens(token_data)
                    return token_data
                else:
                    logger.error(f"Token refresh failed: {token_data.get('error')}")
                    return None
            else:
                logger.error(f"Token refresh failed with status {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error refreshing tokens: {e}")
            return None
    
    def clear_tokens(self) -> None:
        """Clear stored tokens"""
        try:
            if os.path.exists(self.storage_path):
                os.remove(self.storage_path)
            logger.info("Tokens cleared")
        except Exception as e:
            logger.error(f"Failed to clear tokens: {e}")
    
    def get_token_info(self) -> Dict[str, Any]:
        """Get token information without sensitive data"""
        tokens = self.load_tokens()
        if not tokens:
            return {'status': 'no_tokens'}
        
        # Handle different token formats
        if 'expires_at' in tokens:
            expires_at = datetime.fromisoformat(tokens['expires_at'])
        elif 'timestamp' in tokens and 'expires_in' in tokens:
            # New format with timestamp and expires_in
            created_at = datetime.fromtimestamp(tokens['timestamp'])
            expires_at = created_at + timedelta(seconds=tokens['expires_in'])
        else:
            # Default to 1 hour from now if no expiry info
            expires_at = datetime.now() + timedelta(hours=1)
        
        is_expired = datetime.now() > expires_at
        
        return {
            'status': 'expired' if is_expired else 'valid',
            'expires_at': expires_at.isoformat(),
            'created_at': tokens.get('created_at', datetime.now().isoformat()),
            'token_type': tokens.get('token_type', 'Bearer'),
            'has_refresh_token': bool(tokens.get('refresh_token'))
        }