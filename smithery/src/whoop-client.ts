/**
 * WHOOP API Client for Smithery MCP Server
 */

import {
  WhoopConfig,
  WhoopProfile,
  WhoopWorkout,
  WhoopRecovery,
  WhoopSleep,
  WhoopCycle,
  ApiResponse,
  CacheEntry,
  RateLimitState,
  WhoopApiError
} from './types.js';

export class WhoopClient {
  private config: WhoopConfig;
  private cache = new Map<string, CacheEntry<any>>();
  private rateLimitState: RateLimitState = {
    requestCount: 0,
    windowStart: Date.now()
  };

  constructor(config: WhoopConfig) {
    this.config = config;
  }

  /**
   * Check and enforce rate limiting
   */
  private checkRateLimit(): void {
    const now = Date.now();
    const windowDuration = 60 * 1000; // 1 minute in milliseconds

    // Reset counter if window has passed
    if (now - this.rateLimitState.windowStart >= windowDuration) {
      this.rateLimitState.requestCount = 0;
      this.rateLimitState.windowStart = now;
    }

    if (this.rateLimitState.requestCount >= this.config.rateLimitPerMinute) {
      throw new Error('Rate limit exceeded. Please wait before making more requests.');
    }

    this.rateLimitState.requestCount++;
  }

  /**
   * Generate cache key for endpoint and parameters
   */
  private getCacheKey(endpoint: string, params?: Record<string, any>): string {
    if (params) {
      const paramStr = JSON.stringify(params, Object.keys(params).sort());
      return `${endpoint}:${paramStr}`;
    }
    return endpoint;
  }

  /**
   * Get data from cache if still valid
   */
  private getFromCache<T>(cacheKey: string): T | null {
    const cached = this.cache.get(cacheKey);
    if (cached && Date.now() < cached.expiresAt) {
      return cached.data as T;
    }

    if (cached) {
      // Remove expired entry
      this.cache.delete(cacheKey);
    }

    return null;
  }

  /**
   * Save data to cache
   */
  private saveToCache<T>(cacheKey: string, data: T): void {
    const expiresAt = Date.now() + (this.config.cacheTimeout * 1000);
    this.cache.set(cacheKey, {
      data,
      timestamp: Date.now(),
      expiresAt
    });
  }

  /**
   * Make authenticated request to WHOOP API
   */
  private async makeRequest<T>(
    endpoint: string,
    params?: Record<string, any>
  ): Promise<T> {
    // Check rate limits
    this.checkRateLimit();

    // Check cache first
    const cacheKey = this.getCacheKey(endpoint, params);
    const cached = this.getFromCache<T>(cacheKey);
    if (cached) {
      return cached;
    }

    // Build URL
    const url = new URL(endpoint, this.config.baseUrl);
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          url.searchParams.append(key, String(value));
        }
      });
    }

    // Make request
    const response = await fetch(url.toString(), {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${this.config.accessToken}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    });

    if (!response.ok) {
      const errorText = await response.text();
      let errorMessage = `API request failed with status ${response.status}`;

      try {
        const errorJson = JSON.parse(errorText) as WhoopApiError;
        errorMessage = errorJson.message || errorMessage;
      } catch {
        // Use the default error message if JSON parsing fails
      }

      if (response.status === 401) {
        errorMessage = 'Authentication failed. Please check your access token.';
      } else if (response.status === 429) {
        errorMessage = 'Rate limit exceeded. Please wait before making more requests.';
      }

      throw new Error(errorMessage);
    }

    const data = await response.json() as T;

    // Cache successful responses
    this.saveToCache(cacheKey, data);

    return data;
  }

  /**
   * Get user profile information
   */
  async getUserProfile(): Promise<WhoopProfile> {
    const response = await this.makeRequest<ApiResponse<WhoopProfile>>('/user/profile/basic');
    return response.data;
  }

  /**
   * Get user workouts
   */
  async getWorkouts(params?: {
    start?: string;
    end?: string;
    limit?: number;
  }): Promise<WhoopWorkout[]> {
    const response = await this.makeRequest<ApiResponse<WhoopWorkout[]>>(
      '/activity/workout',
      { limit: 25, ...params }
    );
    return response.data;
  }

  /**
   * Get user recovery data
   */
  async getRecovery(params?: {
    start?: string;
    end?: string;
    limit?: number;
  }): Promise<WhoopRecovery[]> {
    const response = await this.makeRequest<ApiResponse<WhoopRecovery[]>>(
      '/recovery',
      { limit: 25, ...params }
    );
    return response.data;
  }

  /**
   * Get user sleep data
   */
  async getSleep(params?: {
    start?: string;
    end?: string;
    limit?: number;
  }): Promise<WhoopSleep[]> {
    const response = await this.makeRequest<ApiResponse<WhoopSleep[]>>(
      '/activity/sleep',
      { limit: 25, ...params }
    );
    return response.data;
  }

  /**
   * Get user physiological cycles
   */
  async getCycles(params?: {
    start?: string;
    end?: string;
    limit?: number;
  }): Promise<WhoopCycle[]> {
    const response = await this.makeRequest<ApiResponse<WhoopCycle[]>>(
      '/cycle',
      { limit: 25, ...params }
    );
    return response.data;
  }

  /**
   * Get authentication status
   */
  getAuthStatus(): { status: string; hasToken: boolean } {
    return {
      status: this.config.accessToken ? 'valid' : 'missing',
      hasToken: Boolean(this.config.accessToken)
    };
  }

  /**
   * Clear all cached data
   */
  clearCache(): void {
    this.cache.clear();
  }

  /**
   * Get cache statistics
   */
  getCacheStats(): { size: number; entries: string[] } {
    return {
      size: this.cache.size,
      entries: Array.from(this.cache.keys())
    };
  }
}