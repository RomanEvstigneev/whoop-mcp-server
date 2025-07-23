# 🏃 WHOOP MCP Server - Smithery Deployment

> Connect your WHOOP fitness data to Claude Desktop through Smithery's hosted MCP platform

This is the **Smithery-hosted version** of the WHOOP MCP Server, providing an alternative to local installation with zero configuration complexity.

## 🚀 Quick Start with Smithery

### Option 1: Use Hosted Server (Recommended)

1. **Get your WHOOP tokens**:
   - **Quick Link**: 👉 **[Authorize WHOOP Access](https://personal-integrations-462307.uc.r.appspot.com/)**
   - After authorization, copy your `access_token` and `refresh_token` from the response
   - Or follow the detailed [local setup guide](../README.md#3-setup)
2. **Add to Claude Desktop** with your tokens:

```json
{
  "mcpServers": {
    "whoop": {
      "type": "http", 
      "url": "https://server.smithery.ai/@romanevstigneev/whoop-mcp-server/mcp",
      "config": {
        "accessToken": "your_whoop_access_token_here",
        "refreshToken": "your_whoop_refresh_token_here"
      }
    }
  }
}
```

3. **Restart Claude Desktop** - that's it! 🎉

### Option 2: Deploy Your Own

1. **Fork this repository**
2. **Connect to Smithery**:
   - Sign up at [smithery.ai](https://smithery.ai)
   - Connect your GitHub account
   - Deploy the entire repository (Smithery config is in root)

3. **Configure in Claude Desktop** with your deployment URL

## 🔧 Configuration Options

| Setting | Description | Default | Required |
|---------|-------------|---------|----------|
| `accessToken` | Your WHOOP API access token | - | ✅ |
| `refreshToken` | Your WHOOP refresh token | - | ❌ |
| `baseUrl` | WHOOP API base URL | `https://api.prod.whoop.com/developer/v1` | ❌ |
| `cacheTimeout` | Cache duration in seconds | `300` | ❌ |
| `rateLimitPerMinute` | API requests per minute | `100` | ❌ |

## 🛠️ Available Tools

All tools from the main server are available:

- `get_whoop_auth_status` - Check authentication status
- `get_whoop_profile` - Get user profile information  
- `get_whoop_workouts` - Get workout data (with date range & limit)
- `get_whoop_recovery` - Get recovery data (with date range & limit)
- `get_whoop_sleep` - Get sleep data (with date range & limit)
- `get_whoop_cycles` - Get physiological cycle data (with date range & limit)
- `clear_whoop_cache` - Clear cached data for fresh API calls

## 💡 Usage Examples

Once configured, ask Claude:
- **"Show my WHOOP profile"**
- **"What were my workouts this week?"**
- **"How is my recovery trending?"**
- **"Show my sleep data for the last 7 days"**

## 🆚 Smithery vs Local Installation

| Feature | Smithery Hosted | Local Installation |
|---------|-----------------|-------------------|
| **Setup Complexity** | ⭐ Minimal (just add URL) | ⭐⭐⭐ Complex (Python, OAuth, paths) |
| **Maintenance** | ⭐⭐⭐ Zero (auto-updates) | ⭐ Manual (updates, dependencies) |
| **Performance** | ⭐⭐⭐ Optimized hosting | ⭐⭐ Depends on local setup |
| **Security** | ⭐⭐ Hosted platform | ⭐⭐⭐ Fully local |
| **Cost** | Free tier available | Free |
| **Reliability** | ⭐⭐⭐ Enterprise hosting | ⭐⭐ Depends on local setup |

## 🔐 Security & Privacy

- **Your tokens are secure**: Configuration is encrypted in transit and at rest
- **No data storage**: Smithery doesn't store your WHOOP data permanently
- **Direct API calls**: Your WHOOP data goes directly from WHOOP → Smithery → Claude
- **Rate limiting**: Built-in protection against API abuse

## 🐛 Troubleshooting

### Common Issues

**"Authentication failed"**
- Check your `accessToken` is correct
- Ensure your WHOOP account is active
- Try regenerating tokens from WHOOP

**"Rate limit exceeded"**
- Built-in rate limiting protects your API quota
- Wait a minute before retrying
- Use `clear_whoop_cache` to reset if needed

**"Invalid configuration"**
- Verify JSON syntax in Claude Desktop config
- Ensure required `accessToken` is provided
- Check the server URL is correct

## 📚 Development

To develop this Smithery server locally:

```bash
# From repository root (where smithery.yaml is located)
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

**Note**: The TypeScript source files are in `smithery/src/` but the configuration files (`smithery.yaml`, `package.json`, `tsconfig.json`) are in the repository root per Smithery requirements.

## 🔗 Links

- **Main Repository**: [WHOOP MCP Server](../README.md)
- **Smithery Platform**: [smithery.ai](https://smithery.ai)
- **WHOOP API Docs**: [developer.whoop.com](https://developer.whoop.com)
- **MCP Protocol**: [modelcontextprotocol.io](https://modelcontextprotocol.io)

## 📄 License

MIT License - same as the main project.