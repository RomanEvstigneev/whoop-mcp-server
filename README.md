# 🏃 WHOOP MCP Server

> Connect your WHOOP fitness data to Claude Desktop through the Model Context Protocol (MCP)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

Transform your WHOOP fitness data into actionable insights through natural language queries in Claude Desktop. Ask questions about your workouts, recovery, sleep patterns, and more - all while keeping your data secure and private.

## ✨ Features

🔐 **Secure OAuth Integration** - Safe WHOOP account connection with encrypted local storage  
🏃 **Complete Data Access** - Workouts, recovery, sleep, cycles, and profile information  
🤖 **Natural Language Queries** - Ask Claude about your fitness data in plain English  
⚡ **Smart Caching** - Optimized performance with intelligent data caching  
🛡️ **Privacy First** - All data stays on your machine, never sent to third parties  
🔄 **Auto Token Refresh** - Seamless experience with automatic authentication renewal

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- Claude Desktop
- Active WHOOP account

### 2. Installation

```bash
git clone https://github.com/romanevstigneev/whoop-mcp-server.git
cd whoop-mcp-server
pip install -r requirements.txt
```

### 3. Setup

Run the interactive setup:
```bash
python setup.py
```

This will:
- Open your browser for WHOOP OAuth authorization
- Securely save your tokens locally
- Provide Claude Desktop configuration

### 4. Configure Claude Desktop

Add to your Claude Desktop settings:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\\Claude\\claude_desktop_config.json`
**Linux**: `~/.config/claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "whoop": {
      "command": "python",
      "args": ["/path/to/whoop-mcp-server/src/whoop_mcp_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/whoop-mcp-server/src"
      }
    }
  }
}
```

### 5. Restart Claude Desktop

After adding the configuration, restart Claude Desktop to load the WHOOP server.

## 💡 Usage Examples

Once configured, you can ask Claude:

- **"Show my WHOOP profile"**
- **"What were my workouts this week?"**
- **"How is my recovery trending?"**
- **"Show my sleep data for the last 7 days"**
- **"What's my HRV looking like?"**
- **"Compare my recovery to last month"**

## 🛠️ Available Tools

### `get_whoop_profile`
Get your WHOOP user profile information.

### `get_whoop_workouts`
Get workout data with optional filters:
- `start_date` (YYYY-MM-DD)
- `end_date` (YYYY-MM-DD)
- `limit` (number of results)

### `get_whoop_recovery`
Get recovery data with optional filters:
- `start_date` (YYYY-MM-DD)
- `end_date` (YYYY-MM-DD)
- `limit` (number of results)

### `get_whoop_sleep`
Get sleep data with optional filters:
- `start_date` (YYYY-MM-DD)
- `end_date` (YYYY-MM-DD)
- `limit` (number of results)

### `get_whoop_cycles`
Get physiological cycles (daily data) with optional filters:
- `start_date` (YYYY-MM-DD)
- `end_date` (YYYY-MM-DD)
- `limit` (number of results)

### `get_whoop_auth_status`
Check authentication status and token information.

### `clear_whoop_cache`
Clear cached data to force fresh API calls.

## 🔐 Security

- **Token Encryption**: All tokens are encrypted at rest using AES encryption
- **Local Storage**: Tokens are stored locally on your machine, never sent to third parties
- **Secure Permissions**: Token files have restricted permissions (600)
- **Auto-Refresh**: Tokens are automatically refreshed when expired

## 📊 Data Caching

- **Smart Caching**: API responses are cached for 5 minutes to improve performance
- **Rate Limiting**: Built-in rate limiting to respect WHOOP API limits
- **Cache Control**: Manual cache clearing available

## 🔧 Configuration

Environment variables (optional):
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `LOG_FILE`: Log file path (default: console only)

## 📁 File Structure

```
whoop-mcp-server/
├── src/
│   ├── whoop_mcp_server.py    # Main MCP server
│   ├── whoop_client.py        # WHOOP API client
│   ├── auth_manager.py        # Token management
│   └── config.py              # Configuration
├── storage/
│   ├── tokens.json            # Encrypted tokens (auto-generated)
│   └── .encryption_key        # Encryption key (auto-generated)
├── setup.py                   # Interactive setup script
└── requirements.txt           # Python dependencies
```

## 🐛 Troubleshooting

### "No valid access token available"
- Run `python setup.py` to re-authorize
- Check that your WHOOP account is active

### "Authentication failed"
- Your tokens may have expired beyond refresh
- Run `python setup.py` to get new tokens

### "Rate limit exceeded"
- Wait a minute before making more requests
- Consider using cached data or reducing request frequency

### Claude Desktop doesn't see the server
- Check that the path in `claude_desktop_config.json` is correct
- Restart Claude Desktop after configuration changes
- Verify Python can be found in your PATH

## 🔄 Token Refresh

The server automatically refreshes expired tokens using the refresh token. If this fails, you'll need to re-authorize:

```bash
python setup.py
```

## 📝 Logging

Logs are written to console by default. To log to a file:

```bash
export LOG_FILE="/path/to/whoop-mcp.log"
export LOG_LEVEL="INFO"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This is an unofficial integration with WHOOP. It uses the official WHOOP API but is not endorsed by WHOOP.

## 📞 Support

- Check the troubleshooting section above
- Open an issue on GitHub
- Review WHOOP API documentation at https://developer.whoop.com/

## 🎯 Roadmap

- [ ] Historical data analysis
- [ ] Custom date range queries
- [ ] Data export functionality
- [ ] Webhook support for real-time updates
- [ ] Advanced analytics and insights