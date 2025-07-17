# 🏃‍♂️ Whoop MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js Version](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-blue.svg)](https://modelcontextprotocol.io/)

A Model Context Protocol (MCP) server that provides [Claude Desktop](https://claude.ai/desktop) with secure access to your Whoop fitness and health data. Get insights about your sleep, recovery, workouts, and more directly through conversations with Claude.

## 🌟 Features

### 8 Powerful MCP Tools
- **🛌 Sleep Data** - Detailed sleep tracking including stages, efficiency, and disturbances
- **🔄 Recovery Data** - Recovery scores based on HRV, RHR, and sleep quality
- **💪 Workout Data** - Exercise sessions, duration, strain, and calories burned
- **⚡ Strain Data** - Daily strain scores and stress measurements
- **❤️ Heart Rate Data** - Continuous heart rate and HRV monitoring
- **📊 Daily Summary** - Consolidated daily overview combining all metrics
- **👤 User Profile** - Basic profile information and preferences
- **📏 Body Measurements** - Height, weight, and maximum heart rate

### 🔒 Privacy & Security
- **Local Processing** - All data processing happens on your machine
- **No Data Storage** - No health data is stored by this server
- **Secure Authentication** - OAuth 2.0 with refresh token handling
- **Rate Limiting** - Built-in API rate limiting and error handling

## 🚀 Quick Start

### Prerequisites
- [Node.js 18+](https://nodejs.org/)
- Active Whoop device and membership
- [Claude Desktop](https://claude.ai/desktop) installed

### Installation

```bash
# Clone the repository
git clone https://github.com/RomanEvstigneev/whoop-mcp-server.git
cd whoop-mcp-server

# Run automated setup
npm run setup

# Get your OAuth tokens
npm run oauth

# Test the server
npm test
```

### Configuration

1. **Create Whoop Developer App**
   - Visit [developer.whoop.com](https://developer.whoop.com/)
   - Create a new app
   - Note your Client ID and Client Secret

2. **Configure Environment**
   ```bash
   # Edit .env file with your credentials
   WHOOP_CLIENT_ID=your_client_id
   WHOOP_CLIENT_SECRET=your_client_secret
   WHOOP_REFRESH_TOKEN=your_refresh_token
   ```

3. **Add to Claude Desktop**
   - Open Claude Desktop configuration
   - Add the server configuration (see [How-To Guide](./docs/HOW_TO.md))
   - Restart Claude Desktop

## 📚 Documentation

- **[Tutorial](./docs/TUTORIAL.md)** - Complete step-by-step setup guide
- **[How-To Guide](./docs/HOW_TO.md)** - Detailed configuration instructions
- **[Privacy Policy](./PRIVACY.md)** - Data handling and privacy information
- **[API Reference](./docs/API.md)** - Complete API documentation

## 🗣️ Usage Examples

Once configured, you can ask Claude Desktop:

```
"Show me my sleep data for the last week"
"What was my recovery score yesterday?"
"Get my workout data for this month"
"Show me my daily summary for today"
"How has my HRV trended over the past month?"
"What's my average strain score this week?"
```

## 🔧 Development

### Project Structure
```
whoop-mcp-server/
├── src/
│   └── index.js              # Main MCP server
├── docs/                     # Documentation
├── .github/                  # GitHub templates
├── tests/                    # Test files
├── package.json             # Dependencies
├── README.md               # This file
├── PRIVACY.md              # Privacy policy
└── LICENSE                 # MIT license
```

### Scripts
```bash
npm start          # Start the MCP server
npm test           # Run tests
npm run oauth      # OAuth token helper
npm run setup      # Automated setup
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](./CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🐛 Issues & Support

- **Bug Reports**: Use our [bug report template](.github/ISSUE_TEMPLATE/bug_report.md)
- **Feature Requests**: Use our [feature request template](.github/ISSUE_TEMPLATE/feature_request.md)
- **Questions**: Check our [discussions](https://github.com/RomanEvstigneev/whoop-mcp-server/discussions)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## ⚖️ Privacy & Legal

- **Privacy Policy**: [PRIVACY.md](./PRIVACY.md)
- **Security Policy**: [SECURITY.md](./SECURITY.md)
- This project is not affiliated with Whoop Inc.
- Use of the Whoop API is subject to [Whoop's Terms of Service](https://www.whoop.com/terms/)

## 🙏 Acknowledgments

- [Whoop](https://www.whoop.com/) for providing the API
- [Anthropic](https://www.anthropic.com/) for the MCP specification
- [Claude Desktop](https://claude.ai/desktop) for the integration platform

---

**⚠️ Important**: This server requires your Whoop API credentials. Please review our [Privacy Policy](./PRIVACY.md) to understand how your data is handled. Your health data never leaves your machine and is only used to respond to your requests through Claude Desktop.