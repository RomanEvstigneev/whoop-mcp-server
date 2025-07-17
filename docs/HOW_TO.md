# 🔧 How-To Guide: Whoop MCP Server

This guide covers specific configurations and advanced usage scenarios for the Whoop MCP Server.

## 📋 Table of Contents

- [Claude Desktop Configuration](#claude-desktop-configuration)
- [Environment Variables](#environment-variables)
- [OAuth Token Management](#oauth-token-management)
- [API Usage Examples](#api-usage-examples)
- [Advanced Configuration](#advanced-configuration)
- [Troubleshooting](#troubleshooting)

## 🖥️ Claude Desktop Configuration

### Finding Your Configuration File

The Claude Desktop configuration file location depends on your operating system:

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```bash
%APPDATA%/Claude/claude_desktop_config.json
```

**Linux:**
```bash
~/.config/Claude/claude_desktop_config.json
```

### Basic Configuration

Create or edit your Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "whoop": {
      "command": "node",
      "args": ["index.js"],
      "cwd": "/path/to/whoop-mcp-server",
      "env": {
        "WHOOP_CLIENT_ID": "your_client_id",
        "WHOOP_CLIENT_SECRET": "your_client_secret",
        "WHOOP_REFRESH_TOKEN": "your_refresh_token"
      }
    }
  }
}
```

### Using .env File (Recommended)

Instead of putting credentials directly in the Claude config, use a `.env` file:

```json
{
  "mcpServers": {
    "whoop": {
      "command": "node",
      "args": ["index.js"],
      "cwd": "/path/to/whoop-mcp-server"
    }
  }
}
```

Then create a `.env` file in your project directory:

```env
WHOOP_CLIENT_ID=your_client_id
WHOOP_CLIENT_SECRET=your_client_secret
WHOOP_REFRESH_TOKEN=your_refresh_token
```

## 🔐 Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `WHOOP_CLIENT_ID` | Your Whoop app client ID | `abc123def456` |
| `WHOOP_CLIENT_SECRET` | Your Whoop app client secret | `secret_key_here` |
| `WHOOP_REFRESH_TOKEN` | OAuth refresh token | `refresh_token_here` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `WHOOP_API_TIMEOUT` | API request timeout (ms) | `10000` |
| `WHOOP_RATE_LIMIT` | Rate limit (requests/minute) | `60` |
| `DEBUG` | Enable debug logging | `false` |

## 🔄 OAuth Token Management

### Getting New Tokens

If your refresh token expires, get new tokens:

```bash
npm run oauth
```

### Manual Token Refresh

You can also manually refresh tokens using curl:

```bash
curl -X POST https://api.prod.whoop.com/oauth/oauth2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token&refresh_token=YOUR_REFRESH_TOKEN&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET"
```

### Token Scopes

The server requires these OAuth scopes:
- `read:recovery` - Access to recovery data
- `read:sleep` - Access to sleep data  
- `read:workout` - Access to workout data
- `read:profile` - Access to user profile
- `read:body_measurement` - Access to body measurements
- `read:cycles` - Access to cycle/strain data

## 📊 API Usage Examples

### Sleep Data Queries

```javascript
// Get sleep data for a specific date range
"Show me my sleep data from 2024-01-01 to 2024-01-07"

// Get yesterday's sleep
"What was my sleep like yesterday?"

// Sleep quality analysis
"How has my sleep quality been this week?"
```

### Recovery Data Queries

```javascript
// Recovery score for today
"What's my recovery score today?"

// Recovery trends
"Show me my recovery trend for the last month"

// HRV analysis
"How has my heart rate variability been?"
```

### Workout Data Queries

```javascript
// Recent workouts
"Show me my workouts from this week"

// Specific workout analysis
"What was my strain score for today's workout?"

// Workout patterns
"How often did I work out last month?"
```

### Combined Queries

```javascript
// Daily summary
"Give me my daily summary for today"

// Weekly overview
"Show me my weekly overview including sleep, recovery, and workouts"

// Correlation analysis
"How does my sleep quality correlate with my recovery scores?"
```

## ⚙️ Advanced Configuration

### Custom API Timeout

Add timeout configuration to your server:

```javascript
// In your .env file
WHOOP_API_TIMEOUT=15000
```

### Rate Limiting

Configure rate limiting to avoid API limits:

```javascript
// In your .env file
WHOOP_RATE_LIMIT=50
```

### Debug Mode

Enable debug logging:

```javascript
// In your .env file
DEBUG=whoop:*
```

Or run with debug:

```bash
DEBUG=whoop:* npm start
```

### Custom Error Handling

The server includes built-in error handling for common scenarios:

- **Token expiration**: Automatically refreshes tokens
- **Rate limiting**: Implements backoff strategies
- **Network errors**: Retries failed requests
- **Invalid dates**: Validates date formats

## 📅 Date Format Requirements

All date parameters must use ISO 8601 format (YYYY-MM-DD):

✅ **Correct:**
- `2024-01-15`
- `2024-12-31`

❌ **Incorrect:**
- `01/15/2024`
- `15-01-2024`
- `2024/01/15`

## 🔧 Troubleshooting

### Common Issues

#### 1. "Server not responding"

**Symptoms:** Claude Desktop shows MCP server errors

**Solutions:**
```bash
# Check server status
npm test

# Verify configuration
cat claude_desktop_config.json

# Check logs
DEBUG=* npm start
```

#### 2. "Invalid credentials"

**Symptoms:** Authentication errors

**Solutions:**
```bash
# Get new tokens
npm run oauth

# Verify environment variables
cat .env

# Check Whoop developer dashboard
```

#### 3. "Rate limit exceeded"

**Symptoms:** API calls failing with 429 errors

**Solutions:**
```bash
# Wait for rate limit reset
# Reduce query frequency
# Check your usage in Whoop dashboard
```

#### 4. "Date format errors"

**Symptoms:** Invalid date parameter errors

**Solutions:**
```bash
# Use YYYY-MM-DD format
# Ensure start_date < end_date
# Check for typos in date strings
```

### Diagnostic Commands

```bash
# Test server functionality
npm test

# Check API connectivity
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.prod.whoop.com/v2/user/profile/basic

# Validate configuration
node -e "console.log(JSON.stringify(require('./claude-desktop-config.json'), null, 2))"
```

### Log Analysis

Enable detailed logging:

```bash
# Full debug output
DEBUG=* npm start

# Whoop-specific logs
DEBUG=whoop:* npm start

# Network requests only
DEBUG=axios npm start
```

## 🔒 Security Best Practices

### Environment Variables

- Use `.env` files for sensitive data
- Never commit credentials to version control
- Use different credentials for development/production

### Token Management

- Rotate refresh tokens regularly
- Monitor token usage in Whoop dashboard
- Use secure storage for production deployments

### Network Security

- Use HTTPS for all API calls
- Implement proper error handling
- Log security events appropriately

## 📝 Configuration Templates

### Development Configuration

```json
{
  "mcpServers": {
    "whoop-dev": {
      "command": "node",
      "args": ["index.js"],
      "cwd": "/path/to/whoop-mcp-server",
      "env": {
        "DEBUG": "whoop:*",
        "WHOOP_API_TIMEOUT": "15000"
      }
    }
  }
}
```

### Production Configuration

```json
{
  "mcpServers": {
    "whoop": {
      "command": "node",
      "args": ["index.js"],
      "cwd": "/path/to/whoop-mcp-server",
      "env": {
        "NODE_ENV": "production",
        "WHOOP_RATE_LIMIT": "30"
      }
    }
  }
}
```

## 🚀 Performance Optimization

### Caching

The server implements smart caching for API responses:

- Recovery data cached for 1 hour
- Sleep data cached for 6 hours
- Profile data cached for 24 hours

### Batch Requests

Use daily summary for multiple data points:

```javascript
// More efficient
"Show me my daily summary for this week"

// Less efficient
"Show me my sleep data for this week"
"Show me my recovery data for this week"
"Show me my strain data for this week"
```

### Rate Limit Management

- Implement exponential backoff
- Use batch endpoints when available
- Monitor API usage in Whoop dashboard

---

**Questions?** Check our [GitHub discussions](https://github.com/yourusername/whoop-mcp-server/discussions) or open an issue!