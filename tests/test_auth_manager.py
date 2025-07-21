"""
Tests for WHOOP MCP Server authentication management
"""
import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import tempfile
import os
from datetime import datetime, timedelta

# Add src to path for imports
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from auth_manager import TokenManager


class TestTokenManager(unittest.TestCase):
    """Test cases for TokenManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.token_path = os.path.join(self.temp_dir, 'tokens.json')
        self.key_path = os.path.join(self.temp_dir, '.encryption_key')
        
        # Mock the configuration paths
        self.token_manager_patcher = patch.multiple(
            'auth_manager',
            TOKEN_STORAGE_PATH=self.token_path,
            ENCRYPTION_KEY_FILE=self.key_path
        )
        self.token_manager_patcher.start()
        
    def tearDown(self):
        """Clean up test fixtures"""
        self.token_manager_patcher.stop()
        # Clean up temp files
        try:
            os.unlink(self.token_path)
            os.unlink(self.key_path)
            os.rmdir(self.temp_dir)
        except FileNotFoundError:
            pass
    
    def test_token_manager_initialization(self):
        """Test TokenManager initializes correctly"""
        tm = TokenManager()
        self.assertIsNotNone(tm.encryption_key)
        self.assertIsNotNone(tm.fernet)
    
    def test_encryption_key_creation(self):
        """Test encryption key is created if not exists"""
        self.assertFalse(os.path.exists(self.key_path))
        tm = TokenManager()
        self.assertTrue(os.path.exists(self.key_path))
        
    def test_save_and_load_tokens(self):
        """Test token save and load functionality"""
        tm = TokenManager()
        
        # Test tokens
        test_tokens = {
            'access_token': 'test_access_token_123',
            'refresh_token': 'test_refresh_token_456',
            'token_type': 'Bearer',
            'expires_in': 3600
        }
        
        # Save tokens
        tm.save_tokens(test_tokens)
        self.assertTrue(os.path.exists(self.token_path))
        
        # Load tokens
        loaded_tokens = tm.load_tokens()
        self.assertIsNotNone(loaded_tokens)
        self.assertEqual(loaded_tokens['access_token'], test_tokens['access_token'])
        self.assertEqual(loaded_tokens['refresh_token'], test_tokens['refresh_token'])
        
    def test_token_expiration_check(self):
        """Test token expiration checking"""
        tm = TokenManager()
        
        # Create expired token
        expired_token = {
            'expires_at': (datetime.now() - timedelta(hours=1)).isoformat()
        }
        self.assertTrue(tm.is_token_expired(expired_token))
        
        # Create valid token
        valid_token = {
            'expires_at': (datetime.now() + timedelta(hours=1)).isoformat()
        }
        self.assertFalse(tm.is_token_expired(valid_token))
    
    def test_no_tokens_scenario(self):
        """Test behavior when no tokens exist"""
        tm = TokenManager()
        
        # Should return None when no tokens exist
        tokens = tm.load_tokens()
        self.assertIsNone(tokens)
        
        # Should return None for access token
        access_token = tm.get_valid_access_token()
        self.assertIsNone(access_token)
    
    @patch('auth_manager.httpx.AsyncClient.post')
    def test_token_refresh(self, mock_post):
        """Test token refresh functionality"""
        # Mock successful refresh response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'success': True,
            'access_token': 'new_access_token',
            'refresh_token': 'new_refresh_token',
            'expires_in': 3600,
            'token_type': 'Bearer'
        }
        mock_post.return_value = mock_response
        
        tm = TokenManager()
        
        # Test refresh
        result = tm.refresh_tokens('old_refresh_token')
        
        self.assertIsNotNone(result)
        self.assertEqual(result['access_token'], 'new_access_token')
        
    def test_clear_tokens(self):
        """Test token clearing functionality"""
        tm = TokenManager()
        
        # Save some tokens first
        test_tokens = {
            'access_token': 'test_token',
            'refresh_token': 'test_refresh',
            'token_type': 'Bearer',
            'expires_in': 3600
        }
        tm.save_tokens(test_tokens)
        
        # Verify tokens exist
        self.assertTrue(os.path.exists(self.token_path))
        
        # Clear tokens
        tm.clear_tokens()
        
        # Verify tokens are cleared
        self.assertFalse(os.path.exists(self.token_path))
    
    def test_get_token_info(self):
        """Test token info retrieval"""
        tm = TokenManager()
        
        # Test with no tokens
        info = tm.get_token_info()
        self.assertEqual(info['status'], 'no_tokens')
        
        # Test with valid tokens
        test_tokens = {
            'access_token': 'test_token',
            'refresh_token': 'test_refresh',
            'token_type': 'Bearer',
            'expires_in': 3600
        }
        tm.save_tokens(test_tokens)
        
        info = tm.get_token_info()
        self.assertIn(info['status'], ['valid', 'expired'])
        self.assertEqual(info['token_type'], 'Bearer')


if __name__ == '__main__':
    unittest.main()