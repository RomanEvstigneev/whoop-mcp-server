"""
WHOOP API Client for MCP Server
"""
import httpx
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from config import (
    WHOOP_API_BASE,
    REQUEST_TIMEOUT,
    MAX_REQUESTS_PER_MINUTE,
    CACHE_STORAGE_PATH,
    CACHE_DURATION
)
from auth_manager import TokenManager

logger = logging.getLogger(__name__)

class WhoopClient:
    """WHOOP API client with caching and rate limiting"""
    
    def __init__(self):
        self.base_url = WHOOP_API_BASE
        self.token_manager = TokenManager()
        self.cache = {}
        self.request_count = 0
        self.request_window_start = datetime.now()
        
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with valid access token"""
        access_token = self.token_manager.get_valid_access_token()
        if not access_token:
            raise Exception("No valid access token available")
        
        return {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    
    def _check_rate_limit(self) -> None:
        """Check if we're within rate limits"""
        now = datetime.now()
        
        # Reset counter if window has passed
        if (now - self.request_window_start).total_seconds() >= 60:
            self.request_count = 0
            self.request_window_start = now
        
        if self.request_count >= MAX_REQUESTS_PER_MINUTE:
            raise Exception("Rate limit exceeded. Please wait before making more requests.")
        
        self.request_count += 1
    
    def _get_cache_key(self, endpoint: str, params: Dict[str, Any] = None) -> str:
        """Generate cache key for endpoint and parameters"""
        if params:
            param_str = json.dumps(params, sort_keys=True)
            return f"{endpoint}:{param_str}"
        return endpoint
    
    def _get_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get data from cache if still valid"""
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            cache_time = datetime.fromisoformat(cached_data['cached_at'])
            
            if (datetime.now() - cache_time).total_seconds() < CACHE_DURATION:
                logger.debug(f"Cache hit for {cache_key}")
                return cached_data['data']
            else:
                # Remove expired cache entry
                del self.cache[cache_key]
        
        return None
    
    def _save_to_cache(self, cache_key: str, data: Dict[str, Any]) -> None:
        """Save data to cache"""
        self.cache[cache_key] = {
            'data': data,
            'cached_at': datetime.now().isoformat()
        }
        logger.debug(f"Cached data for {cache_key}")
    
    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make authenticated request to WHOOP API"""
        # Check rate limits
        self._check_rate_limit()
        
        # Check cache first
        cache_key = self._get_cache_key(endpoint, params)
        cached_data = self._get_from_cache(cache_key)
        if cached_data:
            return cached_data
        
        # Make API request
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers()
        
        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
                response = await client.get(url, headers=headers, params=params or {})
                
                if response.status_code == 200:
                    data = response.json()
                    # Cache successful responses
                    self._save_to_cache(cache_key, data)
                    return data
                elif response.status_code == 401:
                    # Token might be expired, clear cache and try once more
                    self.token_manager.clear_tokens()
                    raise Exception("Authentication failed. Please re-authorize your WHOOP account.")
                else:
                    raise Exception(f"API request failed with status {response.status_code}: {response.text}")
                    
        except httpx.TimeoutException:
            raise Exception("Request timed out. Please try again.")
        except Exception as e:
            logger.error(f"Request failed for {endpoint}: {e}")
            raise
    
    async def get_user_profile(self) -> Dict[str, Any]:
        """Get user profile information"""
        return await self._make_request("/user/profile/basic")
    
    async def get_workouts(self, start_date: str = None, end_date: str = None, limit: int = 25) -> Dict[str, Any]:
        """Get user workouts"""
        params = {'limit': limit}
        
        if start_date:
            params['start'] = start_date
        if end_date:
            params['end'] = end_date
            
        return await self._make_request("/activity/workout", params)
    
    async def get_recovery(self, start_date: str = None, end_date: str = None, limit: int = 25) -> Dict[str, Any]:
        """Get user recovery data"""
        params = {'limit': limit}
        
        if start_date:
            params['start'] = start_date
        if end_date:
            params['end'] = end_date
            
        return await self._make_request("/recovery", params)
    
    async def get_sleep(self, start_date: str = None, end_date: str = None, limit: int = 25) -> Dict[str, Any]:
        """Get user sleep data"""
        params = {'limit': limit}
        
        if start_date:
            params['start'] = start_date
        if end_date:
            params['end'] = end_date
            
        return await self._make_request("/activity/sleep", params)
    
    async def get_cycles(self, start_date: str = None, end_date: str = None, limit: int = 25) -> Dict[str, Any]:
        """Get user physiological cycles"""
        params = {'limit': limit}
        
        if start_date:
            params['start'] = start_date
        if end_date:
            params['end'] = end_date
            
        return await self._make_request("/cycle", params)
    
    def get_auth_status(self) -> Dict[str, Any]:
        """Get authentication status"""
        return self.token_manager.get_token_info()
    
    def clear_cache(self) -> None:
        """Clear all cached data"""
        self.cache.clear()
        logger.info("Cache cleared")