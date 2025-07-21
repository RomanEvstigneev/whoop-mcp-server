"""
Tests for WHOOP API client
"""
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import json
import asyncio

# Add src to path for imports
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from whoop_client import WhoopClient


class TestWhoopClient(unittest.TestCase):
    """Test cases for WhoopClient class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = None
    
    def tearDown(self):
        """Clean up test fixtures"""
        if self.client:
            # Clear any cached data
            self.client.clear_cache()
    
    @patch('whoop_client.TokenManager')
    def test_client_initialization(self, mock_token_manager):
        """Test WhoopClient initializes correctly"""
        mock_token_manager.return_value = MagicMock()
        
        client = WhoopClient()
        
        self.assertIsNotNone(client.token_manager)
        self.assertIsInstance(client.cache, dict)
        self.assertIsNotNone(client.last_request_time)
    
    @patch('whoop_client.TokenManager')
    def test_get_auth_headers_with_valid_token(self, mock_token_manager):
        """Test auth headers generation with valid token"""
        mock_tm = MagicMock()
        mock_tm.get_valid_access_token.return_value = 'test_access_token'
        mock_token_manager.return_value = mock_tm
        
        client = WhoopClient()
        headers = client._get_auth_headers()
        
        expected = {
            'Authorization': 'Bearer test_access_token',
            'User-Agent': 'WHOOP-MCP-Server/1.0.0'
        }
        self.assertEqual(headers, expected)
    
    @patch('whoop_client.TokenManager')
    def test_get_auth_headers_no_token(self, mock_token_manager):
        """Test auth headers when no token available"""
        mock_tm = MagicMock()
        mock_tm.get_valid_access_token.return_value = None
        mock_token_manager.return_value = mock_tm
        
        client = WhoopClient()
        
        with self.assertRaises(Exception) as context:
            client._get_auth_headers()
        
        self.assertIn("No valid access token", str(context.exception))
    
    @patch('whoop_client.TokenManager')
    def test_cache_key_generation(self, mock_token_manager):
        """Test cache key generation"""
        mock_token_manager.return_value = MagicMock()
        
        client = WhoopClient()
        
        # Test without parameters
        key1 = client._get_cache_key('/user/profile/basic')
        self.assertEqual(key1, '/user/profile/basic:{}')
        
        # Test with parameters
        params = {'limit': 5, 'start_date': '2024-01-01'}
        key2 = client._get_cache_key('/workout', params)
        self.assertIn('/workout:', key2)
        self.assertIn('limit', key2)
        self.assertIn('start_date', key2)
    
    @patch('whoop_client.TokenManager')
    def test_cache_operations(self, mock_token_manager):
        """Test cache save and retrieve operations"""
        mock_token_manager.return_value = MagicMock()
        
        client = WhoopClient()
        cache_key = 'test_key'
        test_data = {'test': 'data'}
        
        # Test cache miss
        cached = client._get_from_cache(cache_key)
        self.assertIsNone(cached)
        
        # Test cache save
        client._save_to_cache(cache_key, test_data)
        
        # Test cache hit
        cached = client._get_from_cache(cache_key)
        self.assertEqual(cached, test_data)
    
    @patch('whoop_client.TokenManager')
    def test_cache_expiration(self, mock_token_manager):
        """Test cache expiration"""
        mock_token_manager.return_value = MagicMock()
        
        client = WhoopClient()
        cache_key = 'test_key'
        test_data = {'test': 'data'}
        
        # Save data to cache
        client._save_to_cache(cache_key, test_data)
        
        # Manually expire the cache entry
        import time
        client.cache[cache_key]['timestamp'] = time.time() - 400  # Expired
        
        # Should return None for expired cache
        cached = client._get_from_cache(cache_key)
        self.assertIsNone(cached)
        
        # Cache entry should be removed
        self.assertNotIn(cache_key, client.cache)
    
    @patch('whoop_client.TokenManager')
    @patch('whoop_client.httpx.AsyncClient.get')
    async def test_api_request_success(self, mock_get, mock_token_manager):
        """Test successful API request"""
        # Setup mocks
        mock_tm = MagicMock()
        mock_tm.get_valid_access_token.return_value = 'test_token'
        mock_token_manager.return_value = mock_tm
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'test': 'data'}
        mock_get.return_value = mock_response
        
        client = WhoopClient()
        
        # Test API request
        result = await client._api_request('/test/endpoint')
        
        self.assertEqual(result, {'test': 'data'})
        mock_get.assert_called_once()
    
    @patch('whoop_client.TokenManager')
    @patch('whoop_client.httpx.AsyncClient.get')
    async def test_api_request_rate_limit(self, mock_get, mock_token_manager):
        """Test API request with rate limiting"""
        # Setup mocks
        mock_tm = MagicMock()
        mock_tm.get_valid_access_token.return_value = 'test_token'
        mock_token_manager.return_value = mock_tm
        
        mock_response = MagicMock()
        mock_response.status_code = 429  # Rate limited
        mock_response.text = 'Rate limited'
        mock_get.return_value = mock_response
        
        client = WhoopClient()
        
        # Test API request
        with self.assertRaises(Exception) as context:
            await client._api_request('/test/endpoint')
        
        self.assertIn("Rate limit", str(context.exception))
    
    @patch('whoop_client.TokenManager')
    async def test_get_user_profile(self, mock_token_manager):
        """Test get user profile method"""
        # Setup mocks
        mock_tm = MagicMock()
        mock_tm.get_valid_access_token.return_value = 'test_token'
        mock_token_manager.return_value = mock_tm
        
        client = WhoopClient()
        
        # Mock the _api_request method
        expected_profile = {
            'user_id': 12345,
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com'
        }
        
        with patch.object(client, '_api_request', new_callable=AsyncMock) as mock_api:
            mock_api.return_value = expected_profile
            
            result = await client.get_user_profile()
            
            self.assertEqual(result, expected_profile)
            mock_api.assert_called_once_with('/user/profile/basic')
    
    @patch('whoop_client.TokenManager')
    async def test_get_workouts_with_params(self, mock_token_manager):
        """Test get workouts with parameters"""
        # Setup mocks
        mock_tm = MagicMock()
        mock_tm.get_valid_access_token.return_value = 'test_token'
        mock_token_manager.return_value = mock_tm
        
        client = WhoopClient()
        
        expected_workouts = [
            {'id': 1, 'type': 'running'},
            {'id': 2, 'type': 'cycling'}
        ]
        
        with patch.object(client, '_api_request', new_callable=AsyncMock) as mock_api:
            mock_api.return_value = expected_workouts
            
            result = await client.get_workouts(
                start_date='2024-01-01',
                end_date='2024-01-07',
                limit=10
            )
            
            self.assertEqual(result, expected_workouts)
            
            # Check that parameters were passed correctly
            call_args = mock_api.call_args
            self.assertEqual(call_args[0][0], '/activity/workout')
            params = call_args[1]['params']
            self.assertEqual(params['start'], '2024-01-01')
            self.assertEqual(params['end'], '2024-01-07')
            self.assertEqual(params['limit'], 10)
    
    @patch('whoop_client.TokenManager')
    def test_get_auth_status(self, mock_token_manager):
        """Test get auth status method"""
        mock_tm = MagicMock()
        mock_tm.get_token_info.return_value = {
            'status': 'valid',
            'expires_at': '2024-12-31T23:59:59',
            'token_type': 'Bearer',
            'has_refresh_token': True
        }
        mock_token_manager.return_value = mock_tm
        
        client = WhoopClient()
        status = client.get_auth_status()
        
        self.assertEqual(status['status'], 'valid')
        self.assertEqual(status['token_type'], 'Bearer')
        self.assertTrue(status['has_refresh_token'])
    
    @patch('whoop_client.TokenManager')
    def test_clear_cache(self, mock_token_manager):
        """Test cache clearing"""
        mock_token_manager.return_value = MagicMock()
        
        client = WhoopClient()
        
        # Add some cache data
        client.cache['test_key'] = {'data': 'test'}
        self.assertEqual(len(client.cache), 1)
        
        # Clear cache
        client.clear_cache()
        
        # Cache should be empty
        self.assertEqual(len(client.cache), 0)


class TestWhoopClientAsync(unittest.IsolatedAsyncioTestCase):
    """Test cases that require async test methods"""
    
    @patch('whoop_client.TokenManager')
    async def test_multiple_concurrent_requests(self, mock_token_manager):
        """Test multiple concurrent API requests"""
        # Setup mocks
        mock_tm = MagicMock()
        mock_tm.get_valid_access_token.return_value = 'test_token'
        mock_token_manager.return_value = mock_tm
        
        client = WhoopClient()
        
        # Mock different responses for different endpoints
        async def mock_api_request(endpoint, params=None):
            if 'profile' in endpoint:
                return {'user_id': 123}
            elif 'workout' in endpoint:
                return [{'workout_id': 1}]
            elif 'recovery' in endpoint:
                return [{'recovery_score': 85}]
            return {}
        
        with patch.object(client, '_api_request', side_effect=mock_api_request):
            # Make concurrent requests
            tasks = [
                client.get_user_profile(),
                client.get_workouts(limit=5),
                client.get_recovery(limit=5)
            ]
            
            results = await asyncio.gather(*tasks)
            
            self.assertEqual(results[0]['user_id'], 123)
            self.assertEqual(len(results[1]), 1)
            self.assertEqual(len(results[2]), 1)


if __name__ == '__main__':
    unittest.main()