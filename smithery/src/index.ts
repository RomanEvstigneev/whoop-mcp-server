/**
 * WHOOP MCP Server for Smithery
 * 
 * A Model Context Protocol server that provides access to WHOOP fitness data
 * through Claude Desktop, deployed on Smithery platform.
 */

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';
import { WhoopClient } from './whoop-client.js';
import { WhoopConfig } from './types.js';

// Configuration schema validation
const ConfigSchema = z.object({
  accessToken: z.string().min(1, 'Access token is required'),
  refreshToken: z.string().optional(),
  baseUrl: z.string().url().default('https://api.prod.whoop.com/developer/v1'),
  cacheTimeout: z.number().min(60).max(3600).default(300),
  rateLimitPerMinute: z.number().min(10).max(1000).default(100)
});

export default function createServer({ config }: { config: any }) {
  // Validate configuration
  const validatedConfig = ConfigSchema.parse(config) as WhoopConfig;
  
  // Initialize WHOOP client
  const whoopClient = new WhoopClient(validatedConfig);

  // Create MCP server
  const server = new McpServer({
    name: 'whoop-mcp-server',
    version: '1.0.0'
  });

  // Helper function to format tool responses
  const formatResponse = (toolName: string, data: any, error?: string) => {
    return {
      tool: toolName,
      data: error ? undefined : data,
      error: error || undefined,
      timestamp: new Date().toISOString()
    };
  };

  /**
   * Get WHOOP authentication status
   */
  server.tool(
    'get_whoop_auth_status',
    'Get WHOOP authentication status and connection info',
    {},
    async () => {
      try {
        const status = whoopClient.getAuthStatus();
        const response = formatResponse('get_whoop_auth_status', status);
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response, null, 2)
            }
          ]
        };
      } catch (error) {
        const response = formatResponse('get_whoop_auth_status', null, error instanceof Error ? error.message : String(error));
        
        return {
          content: [
            {
              type: 'text', 
              text: JSON.stringify(response, null, 2)
            }
          ]
        };
      }
    }
  );

  /**
   * Get WHOOP user profile
   */
  server.tool(
    'get_whoop_profile',
    'Get WHOOP user profile information including name and basic details',
    {},
    async () => {
      try {
        const profile = await whoopClient.getUserProfile();
        const response = formatResponse('get_whoop_profile', profile);
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response, null, 2)
            }
          ]
        };
      } catch (error) {
        const response = formatResponse('get_whoop_profile', null, error instanceof Error ? error.message : String(error));
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response, null, 2)
            }
          ]
        };
      }
    }
  );

  /**
   * Get WHOOP workouts
   */
  server.tool(
    'get_whoop_workouts',
    'Get WHOOP workout data with optional date range and limit',
    {
      start_date: z.string().optional().describe('Start date in YYYY-MM-DD format'),
      end_date: z.string().optional().describe('End date in YYYY-MM-DD format'),
      limit: z.number().min(1).max(50).default(5).describe('Number of workouts to return (1-50)')
    },
    async ({ start_date, end_date, limit }) => {
      try {
        const workouts = await whoopClient.getWorkouts({
          start: start_date,
          end: end_date,
          limit
        });
        
        const response = formatResponse('get_whoop_workouts', workouts);
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response, null, 2)
            }
          ]
        };
      } catch (error) {
        const response = formatResponse('get_whoop_workouts', null, error instanceof Error ? error.message : String(error));
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response, null, 2)
            }
          ]
        };
      }
    }
  );

  /**
   * Get WHOOP recovery data
   */
  server.tool(
    'get_whoop_recovery',
    'Get WHOOP recovery data with optional date range and limit',
    {
      start_date: z.string().optional().describe('Start date in YYYY-MM-DD format'),
      end_date: z.string().optional().describe('End date in YYYY-MM-DD format'),
      limit: z.number().min(1).max(50).default(5).describe('Number of recovery records to return (1-50)')
    },
    async ({ start_date, end_date, limit }) => {
      try {
        const recovery = await whoopClient.getRecovery({
          start: start_date,
          end: end_date,
          limit
        });
        
        const response = formatResponse('get_whoop_recovery', recovery);
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response, null, 2)
            }
          ]
        };
      } catch (error) {
        const response = formatResponse('get_whoop_recovery', null, error instanceof Error ? error.message : String(error));
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response, null, 2)
            }
          ]
        };
      }
    }
  );

  /**
   * Get WHOOP sleep data
   */
  server.tool(
    'get_whoop_sleep',
    'Get WHOOP sleep data with optional date range and limit',
    {
      start_date: z.string().optional().describe('Start date in YYYY-MM-DD format'),
      end_date: z.string().optional().describe('End date in YYYY-MM-DD format'),
      limit: z.number().min(1).max(50).default(5).describe('Number of sleep records to return (1-50)')
    },
    async ({ start_date, end_date, limit }) => {
      try {
        const sleep = await whoopClient.getSleep({
          start: start_date,
          end: end_date,
          limit
        });
        
        const response = formatResponse('get_whoop_sleep', sleep);
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response, null, 2)
            }
          ]
        };
      } catch (error) {
        const response = formatResponse('get_whoop_sleep', null, error instanceof Error ? error.message : String(error));
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response, null, 2)
            }
          ]
        };
      }
    }
  );

  /**
   * Get WHOOP physiological cycles
   */
  server.tool(
    'get_whoop_cycles',
    'Get WHOOP physiological cycle data (daily summaries) with optional date range and limit',
    {
      start_date: z.string().optional().describe('Start date in YYYY-MM-DD format'),
      end_date: z.string().optional().describe('End date in YYYY-MM-DD format'),
      limit: z.number().min(1).max(50).default(5).describe('Number of cycles to return (1-50)')
    },
    async ({ start_date, end_date, limit }) => {
      try {
        const cycles = await whoopClient.getCycles({
          start: start_date,
          end: end_date,
          limit
        });
        
        const response = formatResponse('get_whoop_cycles', cycles);
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response, null, 2)
            }
          ]
        };
      } catch (error) {
        const response = formatResponse('get_whoop_cycles', null, error instanceof Error ? error.message : String(error));
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response, null, 2)
            }
          ]
        };
      }
    }
  );

  /**
   * Clear WHOOP data cache
   */
  server.tool(
    'clear_whoop_cache',
    'Clear all cached WHOOP data to force fresh API calls',
    {},
    async () => {
      try {
        const stats = whoopClient.getCacheStats();
        whoopClient.clearCache();
        
        const response = formatResponse('clear_whoop_cache', {
          message: 'Cache cleared successfully',
          previousCacheSize: stats.size,
          clearedEntries: stats.entries
        });
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response, null, 2)
            }
          ]
        };
      } catch (error) {
        const response = formatResponse('clear_whoop_cache', null, error instanceof Error ? error.message : String(error));
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response, null, 2)
            }
          ]
        };
      }
    }
  );

  return server.server;
}