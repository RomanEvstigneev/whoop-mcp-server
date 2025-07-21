# 🔧 Detailed Installation Guide

This guide provides step-by-step instructions for installing and configuring the WHOOP MCP Server.

## System Requirements

### Python Environment
- **Python Version**: 3.8 or higher
- **Operating Systems**: macOS, Windows, Linux
- **Memory**: Minimum 512MB available RAM
- **Storage**: ~50MB for installation

### External Dependencies
- **Claude Desktop**: Latest version installed
- **Internet Connection**: Required for WHOOP API access and initial setup
- **WHOOP Account**: Active WHOOP subscription with data

## Step 1: Install Python Dependencies

### Option A: Using pip (Recommended)
```bash
# Clone the repository
git clone https://github.com/romanevstigneev/whoop-mcp-server.git
cd whoop-mcp-server

# Install dependencies
pip install -r requirements.txt
```

### Option B: Using virtual environment (Advanced)
```bash
# Create virtual environment
python -m venv whoop-mcp-env

# Activate virtual environment
# macOS/Linux:
source whoop-mcp-env/bin/activate
# Windows:
whoop-mcp-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Run Setup Wizard

The interactive setup wizard handles WHOOP OAuth authorization:

```bash
python setup.py
```

### Setup Process:
1. **Dependency Check**: Verifies all required packages are installed
2. **Browser Launch**: Opens WHOOP OAuth authorization page
3. **User Authorization**: You authorize the application with your WHOOP account
4. **Token Exchange**: Authorization code is exchanged for access tokens
5. **Secure Storage**: Tokens are encrypted and saved locally
6. **Configuration Generation**: Claude Desktop config is provided

### Expected Output:
```
🏃 WHOOP MCP Server Setup
============================
🔍 Checking dependencies...
✅ All dependencies are installed
📁 Storage directory ready: ~/.whoop-mcp-server/
🔐 WHOOP OAuth Authorization
Step 1: We'll open your browser to authorize WHOOP access
Step 2: After authorization, you'll get a success page
Step 3: Copy the authorization code from the success page

Ready to start authorization? (y/n): y
🌐 Opening browser for WHOOP authorization...
📋 Please copy the authorization code from the success page
Authorization code: [PASTE CODE HERE]
🔄 Exchanging authorization code for tokens...
✅ Successfully obtained tokens!
💾 Saving tokens securely...
✅ Tokens saved successfully!
```

## Step 3: Configure Claude Desktop

### Locate Claude Desktop Configuration File

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```bash
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```bash
~/.config/claude/claude_desktop_config.json
```

### Edit Configuration File

Add the WHOOP MCP server to your configuration:

```json
{
  "mcpServers": {
    "whoop": {
      "command": "/opt/miniconda3/bin/python",
      "args": ["/full/path/to/whoop-mcp-server/src/whoop_mcp_server.py"],
      "env": {
        "PYTHONPATH": "/full/path/to/whoop-mcp-server/src"
      }
    }
  }
}
```

**Important Notes:**
- Replace `/full/path/to/whoop-mcp-server` with the actual path to your installation
- **Use absolute paths**, not relative paths
- **Use full Python path**: Find your Python with `which python3` or `which python`
- On Windows, use forward slashes (`/`) or escape backslashes (`\\\\`)
- **Common Python paths:**
  - macOS with Homebrew: `/opt/homebrew/bin/python3`
  - macOS with Miniconda: `/opt/miniconda3/bin/python`
  - Linux: `/usr/bin/python3`
  - Windows: `C:/Python39/python.exe`

### Example Complete Configuration:
```json
{
  "mcpServers": {
    "whoop": {
      "command": "/opt/miniconda3/bin/python",
      "args": ["/Users/username/whoop-mcp-server/src/whoop_mcp_server.py"],
      "env": {
        "PYTHONPATH": "/Users/username/whoop-mcp-server/src",
        "LOG_LEVEL": "INFO"
      }
    },
    "other-server": {
      "command": "node",
      "args": ["other-server.js"]
    }
  }
}
```

## Step 4: Restart Claude Desktop

1. **Completely quit** Claude Desktop (not just minimize)
2. **Relaunch** Claude Desktop
3. Wait for the application to fully load
4. Check that the WHOOP server appears in available tools

## Step 5: Verification

### Test Server Connection
In Claude Desktop, try asking:
- "What WHOOP tools are available?"
- "Show my WHOOP authentication status"

### Expected Response:
Claude should recognize WHOOP tools and be able to execute them.

### Check Logs (if issues occur):
**macOS:**
```bash
tail -f ~/Library/Logs/Claude/mcp-server-whoop.log
```

**Common Log Locations:**
- macOS: `~/Library/Logs/Claude/`
- Windows: `%LOCALAPPDATA%\Claude\logs\`
- Linux: `~/.local/share/Claude/logs/`

## Troubleshooting

### Common Installation Issues

#### Issue 1: "spawn python ENOENT" Error
**Problem:** Claude Desktop can't find the Python interpreter.

**Solution:**
```bash
# Find your Python path
which python3
# or
which python

# Use the full path in claude_desktop_config.json
{
  "mcpServers": {
    "whoop": {
      "command": "/opt/miniconda3/bin/python",  # ← Use full path here
      "args": ["/path/to/whoop-mcp-server/src/whoop_mcp_server.py"]
    }
  }
}
```

#### Issue 2: Manual OAuth Setup Required
**Problem:** Interactive setup fails with "EOF when reading a line".

**Manual Solution:**
1. Get your authorization code from: https://personal-integrations-462307.uc.r.appspot.com/
2. Exchange it manually:
```bash
python -c "
import requests
import json
from pathlib import Path
import os

auth_code = 'YOUR_AUTHORIZATION_CODE_HERE'
storage_dir = Path.home() / '.whoop-mcp-server'
storage_dir.mkdir(exist_ok=True)

url = f'https://personal-integrations-462307.uc.r.appspot.com/api/get-tokens/{auth_code}'
response = requests.get(url, timeout=30)

if response.status_code == 200:
    token_data = response.json()
    if token_data.get('success'):
        token_file = storage_dir / 'tokens_raw.json'
        with open(token_file, 'w') as f:
            json.dump(token_data, f, indent=2)
        os.chmod(token_file, 0o600)
        print('✅ Tokens saved!')
    else:
        print('❌ Token exchange failed')
else:
    print(f'❌ HTTP Error: {response.status_code}')
"
```
3. Then properly encrypt the tokens:
```bash
cd whoop-mcp-server
python -c "
import sys
import json
from pathlib import Path
sys.path.insert(0, './src')
from auth_manager import TokenManager

storage_dir = Path.home() / '.whoop-mcp-server'
raw_token_file = storage_dir / 'tokens_raw.json'

with open(raw_token_file, 'r') as f:
    token_data = json.load(f)

token_manager = TokenManager()
token_manager.save_tokens(token_data)

token_info = token_manager.get_token_info()
print(f'✅ Status: {token_info[\"status\"]}')

raw_token_file.unlink()  # Clean up
"
```

#### Issue 3: Wrong Configuration File
**Problem:** Adding config to wrong file (e.g., `.claude.json` instead of `claude_desktop_config.json`).

**Solution:** Ensure you're editing the correct file:
- **Correct:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Incorrect:** `~/.claude.json` (this is for Claude Code, not Claude Desktop)

### Python Path Issues
If you get import errors:

```bash
# Check Python version
python --version

# Verify package installation
pip list | grep mcp
pip list | grep httpx

# Test import
python -c "from mcp.server.fastmcp import FastMCP; print('MCP OK')"
```

### Token Issues
If authentication fails:

```bash
# Re-run setup
python setup.py

# Check token storage
ls -la ~/.whoop-mcp-server/
```

### Claude Desktop Issues
If Claude doesn't see the server:

1. **Check JSON syntax** in config file using a JSON validator
2. **Verify paths** are absolute and correct
3. **Use full Python path** - avoid `python`, use the full path like `/opt/miniconda3/bin/python` or `/usr/local/bin/python3`
4. **Check permissions** on the script file:
   ```bash
   chmod +x /path/to/whoop-mcp-server/src/whoop_mcp_server.py
   ```
5. **Test server directly**:
   ```bash
   /opt/miniconda3/bin/python /path/to/whoop-mcp-server/src/whoop_mcp_server.py
   ```
6. **Check Claude Desktop logs** for specific errors:
   ```bash
   tail -f ~/Library/Logs/Claude/mcp-server-whoop.log
   ```

### Network Issues
If OAuth fails:

1. **Check internet connection**
2. **Verify firewall settings** allow HTTPS connections
3. **Check WHOOP service status** at https://status.whoop.com/

## Advanced Configuration

### Environment Variables
Create a `.env` file in the project root:

```bash
# Logging
LOG_LEVEL=INFO
LOG_FILE=/path/to/whoop.log

# Custom storage location
WHOOP_STORAGE_DIR=/custom/path/.whoop-mcp-server
```

### Custom Python Environment
If using a custom Python installation:

```json
{
  "mcpServers": {
    "whoop": {
      "command": "/usr/local/bin/python3.11",
      "args": ["/path/to/whoop-mcp-server/src/whoop_mcp_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/whoop-mcp-server/src"
      }
    }
  }
}
```

## Uninstallation

To completely remove WHOOP MCP Server:

```bash
# Remove installation directory
rm -rf /path/to/whoop-mcp-server

# Remove token storage
rm -rf ~/.whoop-mcp-server

# Remove from Claude Desktop config
# Edit claude_desktop_config.json and remove the "whoop" entry

# Restart Claude Desktop
```

## Getting Help

If you encounter issues:

1. **Check this guide** for common solutions
2. **Review logs** for error messages
3. **Open an issue** on GitHub with:
   - Your operating system and Python version
   - Complete error messages
   - Steps to reproduce the issue
   - Your configuration (with paths anonymized)

## Next Steps

Once installation is complete:
- Read the [Usage Examples](../examples/usage_examples.md)
- Explore available WHOOP tools in Claude Desktop
- Check the [Troubleshooting Guide](TROUBLESHOOTING.md) if you encounter issues