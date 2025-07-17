#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

const WHOOP_API_BASE_URL = "https://api.prod.whoop.com";
const WHOOP_OAUTH_URL = "https://api.prod.whoop.com/oauth/oauth2";

class WhoopMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: "whoop-mcp-server",
        version: "1.0.0",
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.axiosInstance = axios.create({
      baseURL: WHOOP_API_BASE_URL,
      timeout: 10000,
    });

    this.setupToolHandlers();
  }

  async authenticateWithRefreshToken(refreshToken) {
    try {
      const response = await axios.post(`${WHOOP_OAUTH_URL}/token`, {
        grant_type: "refresh_token",
        refresh_token: refreshToken,
        client_id: process.env.WHOOP_CLIENT_ID,
        client_secret: process.env.WHOOP_CLIENT_SECRET,
      });

      return response.data.access_token;
    } catch (error) {
      throw new Error(`Failed to refresh access token: ${error.message}`);
    }
  }

  async makeAuthenticatedRequest(endpoint, params = {}) {
    const accessToken = await this.authenticateWithRefreshToken(
      process.env.WHOOP_REFRESH_TOKEN
    );

    this.axiosInstance.defaults.headers.common["Authorization"] = `Bearer ${accessToken}`;

    return this.axiosInstance.get(endpoint, { params });
  }

  setupToolHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: "get_sleep_data",
            description: "Get sleep data from Whoop API for a specific date range",
            inputSchema: {
              type: "object",
              properties: {
                start_date: {
                  type: "string",
                  description: "Start date in YYYY-MM-DD format",
                },
                end_date: {
                  type: "string",
                  description: "End date in YYYY-MM-DD format",
                },
              },
              required: ["start_date", "end_date"],
            },
          },
          {
            name: "get_recovery_data",
            description: "Get recovery data from Whoop API for a specific date range",
            inputSchema: {
              type: "object",
              properties: {
                start_date: {
                  type: "string",
                  description: "Start date in YYYY-MM-DD format",
                },
                end_date: {
                  type: "string",
                  description: "End date in YYYY-MM-DD format",
                },
              },
              required: ["start_date", "end_date"],
            },
          },
          {
            name: "get_workout_data",
            description: "Get workout/activity data from Whoop API for a specific date range",
            inputSchema: {
              type: "object",
              properties: {
                start_date: {
                  type: "string",
                  description: "Start date in YYYY-MM-DD format",
                },
                end_date: {
                  type: "string",
                  description: "End date in YYYY-MM-DD format",
                },
              },
              required: ["start_date", "end_date"],
            },
          },
          {
            name: "get_strain_data",
            description: "Get strain/stress data from Whoop API for a specific date range",
            inputSchema: {
              type: "object",
              properties: {
                start_date: {
                  type: "string",
                  description: "Start date in YYYY-MM-DD format",
                },
                end_date: {
                  type: "string",
                  description: "End date in YYYY-MM-DD format",
                },
              },
              required: ["start_date", "end_date"],
            },
          },
          {
            name: "get_daily_summary",
            description: "Get daily summary/overview data from Whoop API for a specific date range",
            inputSchema: {
              type: "object",
              properties: {
                start_date: {
                  type: "string",
                  description: "Start date in YYYY-MM-DD format",
                },
                end_date: {
                  type: "string",
                  description: "End date in YYYY-MM-DD format",
                },
              },
              required: ["start_date", "end_date"],
            },
          },
          {
            name: "get_user_profile",
            description: "Get user profile information from Whoop API",
            inputSchema: {
              type: "object",
              properties: {},
            },
          },
          {
            name: "get_body_measurements",
            description: "Get body measurements (height, weight, max HR) from Whoop API",
            inputSchema: {
              type: "object",
              properties: {},
            },
          },
        ],
      };
    });

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case "get_sleep_data":
            return await this.getSleepData(args);
          case "get_recovery_data":
            return await this.getRecoveryData(args);
          case "get_workout_data":
            return await this.getWorkoutData(args);
          case "get_strain_data":
            return await this.getStrainData(args);
          case "get_daily_summary":
            return await this.getDailySummary(args);
          case "get_user_profile":
            return await this.getUserProfile();
          case "get_body_measurements":
            return await this.getBodyMeasurements();
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [
            {
              type: "text",
              text: `Error: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    });
  }

  async getSleepData({ start_date, end_date }) {
    const response = await this.makeAuthenticatedRequest("/v2/activity/sleep", {
      start: start_date,
      end: end_date,
    });

    return {
      content: [
        {
          type: "text",
          text: `Sleep Data (${start_date} to ${end_date}):\n\n${JSON.stringify(response.data, null, 2)}`,
        },
      ],
    };
  }

  async getRecoveryData({ start_date, end_date }) {
    const response = await this.makeAuthenticatedRequest("/v2/activity/recovery", {
      start: start_date,
      end: end_date,
    });

    return {
      content: [
        {
          type: "text",
          text: `Recovery Data (${start_date} to ${end_date}):\n\n${JSON.stringify(response.data, null, 2)}`,
        },
      ],
    };
  }

  async getWorkoutData({ start_date, end_date }) {
    const response = await this.makeAuthenticatedRequest("/v2/activity/workout", {
      start: start_date,
      end: end_date,
    });

    return {
      content: [
        {
          type: "text",
          text: `Workout Data (${start_date} to ${end_date}):\n\n${JSON.stringify(response.data, null, 2)}`,
        },
      ],
    };
  }

  async getStrainData({ start_date, end_date }) {
    const response = await this.makeAuthenticatedRequest("/v2/cycle", {
      start: start_date,
      end: end_date,
    });

    return {
      content: [
        {
          type: "text",
          text: `Strain Data (${start_date} to ${end_date}):\n\n${JSON.stringify(response.data, null, 2)}`,
        },
      ],
    };
  }


  async getDailySummary({ start_date, end_date }) {
    const [sleepResponse, recoveryResponse, strainResponse] = await Promise.all([
      this.makeAuthenticatedRequest("/v2/activity/sleep", {
        start: start_date,
        end: end_date,
      }),
      this.makeAuthenticatedRequest("/v2/activity/recovery", {
        start: start_date,
        end: end_date,
      }),
      this.makeAuthenticatedRequest("/v2/cycle", {
        start: start_date,
        end: end_date,
      }),
    ]);

    const summary = {
      sleep: sleepResponse.data,
      recovery: recoveryResponse.data,
      strain: strainResponse.data,
    };

    return {
      content: [
        {
          type: "text",
          text: `Daily Summary (${start_date} to ${end_date}):\n\n${JSON.stringify(summary, null, 2)}`,
        },
      ],
    };
  }

  async getUserProfile() {
    const response = await this.makeAuthenticatedRequest("/v2/user/profile/basic");

    return {
      content: [
        {
          type: "text",
          text: `User Profile:\n\n${JSON.stringify(response.data, null, 2)}`,
        },
      ],
    };
  }

  async getBodyMeasurements() {
    const response = await this.makeAuthenticatedRequest("/v2/user/measurement/body");

    return {
      content: [
        {
          type: "text",
          text: `Body Measurements:\n\n${JSON.stringify(response.data, null, 2)}`,
        },
      ],
    };
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error("Whoop MCP server running on stdio");
  }
}

const server = new WhoopMCPServer();
server.run().catch(console.error);