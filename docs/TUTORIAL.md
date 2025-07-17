# 📚 Complete Tutorial: Setting Up Whoop MCP Server

This comprehensive tutorial will guide you through the entire process of setting up the Whoop MCP Server to work with Claude Desktop.

## 🎯 What You'll Learn

By the end of this tutorial, you'll have:
- A fully configured Whoop MCP server
- Integration with Claude Desktop
- The ability to query your Whoop data through natural language

## 📋 Prerequisites

Before starting, ensure you have:

### Required
- **Whoop Device**: An active Whoop 4.0 or later device
- **Whoop Membership**: Current subscription to Whoop services
- **Node.js**: Version 18.0.0 or higher ([Download here](https://nodejs.org/))
- **Claude Desktop**: Installed and running ([Download here](https://claude.ai/desktop))

### Recommended
- Basic familiarity with command line/terminal
- Text editor (VS Code, Sublime Text, etc.)
- Git installed (for cloning the repository)

## 🚀 Step-by-Step Setup

### Step 1: Clone and Install the Server

```bash
# Clone the repository
git clone https://github.com/yourusername/whoop-mcp-server.git
cd whoop-mcp-server

# Install dependencies
npm install

# Run the automated setup
npm run setup
```

The setup script will:
- ✅ Verify Node.js version
- ✅ Install dependencies
- ✅ Create environment file template
- ✅ Test the server

### Step 2: Create a Whoop Developer Application

1. **Visit Whoop Developer Portal**
   - Go to [developer.whoop.com](https://developer.whoop.com/)
   - Sign in with your Whoop credentials

2. **Create New Application**
   - Click "Create New App"
   - Fill in the application details:
     ```
     App Name: Claude MCP Server
     Description: Personal MCP server for Claude Desktop
     Redirect URI: http://localhost:3000/callback
     ```
   - Click "Create App"

3. **Save Your Credentials**
   - Copy your **Client ID**
   - Copy your **Client Secret**
   - Keep these secure - you'll need them next

### Step 3: Get Your OAuth Tokens

The server includes a helpful OAuth flow assistant:

```bash
# Run the OAuth helper
npm run oauth
```

Follow the prompts:

1. **Enter your Client ID** (from Step 2)
2. **Enter your Client Secret** (from Step 2)
3. **Enter your Redirect URI**: `http://localhost:3000/callback`
4. **Visit the authorization URL** displayed in your terminal
5. **Authorize the application** in your browser
6. **Copy the authorization code** from the redirect URL
7. **Paste the code** into the terminal

The helper will exchange your authorization code for tokens and display them.

### Step 4: Configure Environment Variables

1. **Edit the .env file**:
   ```bash
   # Open the .env file in your text editor
   nano .env
   # or
   code .env
   ```

2. **Add your credentials**:
   ```env
   WHOOP_CLIENT_ID=your_actual_client_id_here
   WHOOP_CLIENT_SECRET=your_actual_client_secret_here
   WHOOP_REFRESH_TOKEN=your_actual_refresh_token_here
   ```

3. **Save the file**

### Step 5: Test the Server

```bash
# Test the server
npm test
```

You should see output like:
```
✅ Server responded with tools:
  - get_sleep_data: Get sleep data from Whoop API
  - get_recovery_data: Get recovery data from Whoop API
  - get_workout_data: Get workout/activity data from Whoop API
  ...
✅ Test completed successfully!
```

### Step 6: Configure Claude Desktop

1. **Find your Claude Desktop config file**:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. **Edit the configuration**:
   ```json
   {
     "mcpServers": {
       "whoop": {
         "command": "node",
         "args": ["index.js"],
         "cwd": "/full/path/to/your/whoop-mcp-server",
         "env": {
           "WHOOP_CLIENT_ID": "your_client_id_here",
           "WHOOP_CLIENT_SECRET": "your_client_secret_here",
           "WHOOP_REFRESH_TOKEN": "your_refresh_token_here"
         }
       }
     }
   }
   ```

3. **Update the paths and credentials**:
   - Replace `/full/path/to/your/whoop-mcp-server` with your actual path
   - Replace the environment variables with your actual values

4. **Save the configuration file**

5. **Restart Claude Desktop**

## 🎉 Testing Your Setup

Once Claude Desktop restarts, you can test the integration:

### Basic Test
Ask Claude: "Can you show me what Whoop tools are available?"

### Data Queries
Try these example queries:

```
"Show me my sleep data for yesterday"
"What was my recovery score this morning?"
"Get my workout data for the last 7 days"
"Show me my daily summary for today"
"How has my HRV been trending this week?"
```

## 🔧 Troubleshooting

### Common Issues

#### 1. "Failed to refresh access token"
**Solution**: Your refresh token may have expired
- Re-run `npm run oauth` to get new tokens
- Update your `.env` file with the new refresh token

#### 2. "Command not found: node"
**Solution**: Node.js is not installed or not in PATH
- Install Node.js from [nodejs.org](https://nodejs.org/)
- Restart your terminal

#### 3. "Tools not showing in Claude Desktop"
**Solution**: Configuration issues
- Verify your `claude_desktop_config.json` file syntax
- Check that the `cwd` path is correct
- Ensure environment variables are set correctly
- Restart Claude Desktop

#### 4. "Permission denied"
**Solution**: File permissions issue
- Run `chmod +x setup.sh` to make scripts executable
- Ensure you have read/write permissions to the project directory

#### 5. "Network error" or "Rate limit exceeded"
**Solution**: API connectivity issues
- Check your internet connection
- Verify your Whoop account is active
- Wait a few minutes and try again (rate limiting)

### Advanced Troubleshooting

#### Enable Debug Mode
Add debug logging to the server:

```bash
# Start server with debug output
DEBUG=* npm start
```

#### Check Server Status
Verify the server is running correctly:

```bash
# Check if server responds to list tools
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | npm start
```

## 📈 Usage Tips

### Best Practices

1. **Use Specific Date Ranges**
   - "Show me my sleep data for the last 7 days"
   - "Get my recovery data from 2024-01-01 to 2024-01-31"

2. **Combine Multiple Metrics**
   - "Show me my daily summary for this week"
   - "Compare my sleep and recovery data for the last month"

3. **Ask for Analysis**
   - "What patterns do you see in my sleep data?"
   - "How does my recovery correlate with my workouts?"

### Sample Queries

```
Sleep Analysis:
"Show me my sleep stages for the last week"
"What's my average sleep efficiency this month?"
"How many hours of deep sleep did I get last night?"

Recovery Tracking:
"What was my HRV yesterday morning?"
"Show me my recovery trend for the past month"
"Compare my recovery scores to my sleep quality"

Workout Insights:
"List all my workouts from last week"
"What was my highest strain score this month?"
"Show me my calorie burn for today's workout"

Health Monitoring:
"What's my resting heart rate trend?"
"Show me my body measurements"
"Get my user profile information"
```

## 🔒 Security Notes

- **Never share your API credentials** with anyone
- **Use environment variables** for sensitive data
- **Regularly rotate your tokens** for security
- **Monitor your API usage** in the Whoop developer dashboard

## 📞 Getting Help

If you encounter issues:

1. **Check the troubleshooting section** above
2. **Review the logs** for error messages
3. **Search existing issues** on GitHub
4. **Create a new issue** with detailed information

## 🎊 Congratulations!

You now have a fully functional Whoop MCP server integrated with Claude Desktop! You can query your health and fitness data using natural language and get insights about your wellness journey.

## 🚀 Next Steps

- Explore the [API Reference](./API.md) for advanced usage
- Check out the [How-To Guide](./HOW_TO.md) for specific configurations
- Read the [Privacy Policy](../PRIVACY.md) to understand data handling

---

**Need help?** Open an issue on GitHub or check our [discussions](https://github.com/yourusername/whoop-mcp-server/discussions) page!