# 🐛 Troubleshooting Guide

This guide helps you diagnose and fix common issues with the WHOOP MCP Server.

## Quick Diagnostics

### 1. Test Server Directly
```bash
cd whoop-mcp-server/src
python whoop_mcp_server.py
```

**Expected Output:**
```
Starting WHOOP MCP Server with FastMCP...
Initializing WHOOP client...
WHOOP auth status: valid
FastMCP server ready
```

### 2. Check Authentication
```bash
python -c "
import sys; sys.path.append('src')
from whoop_client import WhoopClient
client = WhoopClient()
print(f'Auth status: {client.get_auth_status()}')
"
```

### 3. Verify Dependencies
```bash
pip show mcp httpx pydantic cryptography python-dotenv
```

## Common Issues & Solutions

### 🔐 Authentication Problems

#### "No valid access token available"

**Symptoms:**
- Claude shows authentication errors
- Server logs show token errors
- Cannot access WHOOP data

**Solutions:**
1. **Re-run setup:**
   ```bash
   python setup.py
   ```

2. **Check WHOOP account status:**
   - Log into WHOOP app/website
   - Verify your subscription is active
   - Check for any account restrictions

3. **Clear corrupted tokens:**
   ```bash
   rm -rf ~/.whoop-mcp-server/
   python setup.py
   ```

#### "Token refresh failed"

**Symptoms:**
- Server starts but fails to refresh tokens
- Intermittent authentication failures

**Solutions:**
1. **Manual re-authorization:**
   ```bash
   python setup.py
   ```

2. **Check network connectivity:**
   ```bash
   curl -I https://api.prod.whoop.com/developer/v1/
   ```

3. **Verify OAuth service:**
   ```bash
   curl -I https://personal-integrations-462307.uc.r.appspot.com/health
   ```

### 🔌 Connection Issues

#### Claude Desktop doesn't see WHOOP server

**Symptoms:**
- No WHOOP tools appear in Claude
- Claude doesn't respond to WHOOP queries

**Diagnosis Steps:**
1. **Check Claude Desktop logs:**
   ```bash
   # macOS
   tail -f ~/Library/Logs/Claude/mcp.log
   tail -f ~/Library/Logs/Claude/mcp-server-whoop.log
   
   # Windows
   tail -f %LOCALAPPDATA%\Claude\logs\mcp.log
   
   # Linux
   tail -f ~/.local/share/Claude/logs/mcp.log
   ```

2. **Validate JSON configuration:**
   ```bash
   python -c "import json; print(json.load(open('path/to/claude_desktop_config.json')))"
   ```

**Solutions:**
1. **Fix configuration path:**
   - Use absolute paths only
   - Verify file exists at specified location
   - Check PYTHONPATH is correct

2. **Restart Claude Desktop completely:**
   - Quit application entirely
   - Wait 5 seconds
   - Relaunch

3. **Test configuration:**
   ```json
   {
     "mcpServers": {
       "whoop": {
         "command": "python",
         "args": ["/absolute/path/to/whoop-mcp-server/src/whoop_mcp_server.py"],
         "env": {
           "PYTHONPATH": "/absolute/path/to/whoop-mcp-server/src"
         }
       }
     }
   }
   ```

### 🐍 Python Environment Issues

#### Import errors or module not found

**Symptoms:**
- `ModuleNotFoundError: No module named 'mcp'`
- `ImportError: cannot import name 'FastMCP'`

**Solutions:**
1. **Verify virtual environment:**
   ```bash
   which python
   pip list | grep mcp
   ```

2. **Reinstall dependencies:**
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

3. **Check Python version:**
   ```bash
   python --version  # Should be 3.8+
   ```

4. **Update PYTHONPATH:**
   ```json
   {
     "env": {
       "PYTHONPATH": "/absolute/path/to/whoop-mcp-server/src:/additional/paths"
     }
   }
   ```

### 📡 Network and API Issues

#### Rate limiting errors

**Symptoms:**
- "Rate limit exceeded" messages
- Slow or failed API responses

**Solutions:**
1. **Wait and retry:**
   - WHOOP API has rate limits
   - Wait 1 minute before retrying

2. **Use cached data:**
   - Server caches responses for 5 minutes
   - Ask Claude to use recent cached data

3. **Reduce request frequency:**
   - Don't make rapid successive requests
   - Use reasonable limits in queries

#### Network connectivity issues

**Symptoms:**
- Timeout errors
- Connection refused messages

**Solutions:**
1. **Check internet connection:**
   ```bash
   ping api.prod.whoop.com
   ```

2. **Verify HTTPS access:**
   ```bash
   curl -I https://api.prod.whoop.com/developer/v1/
   ```

3. **Check firewall settings:**
   - Allow outbound HTTPS (port 443)
   - Whitelist WHOOP API domains

### 💾 Storage and Permissions

#### Storage directory issues

**Symptoms:**
- Cannot create storage directory
- Permission denied errors

**Solutions:**
1. **Check permissions:**
   ```bash
   ls -la ~/
   mkdir -p ~/.whoop-mcp-server/
   ```

2. **Fix ownership:**
   ```bash
   sudo chown -R $USER ~/.whoop-mcp-server/
   chmod 700 ~/.whoop-mcp-server/
   ```

3. **Use custom storage path:**
   ```bash
   export WHOOP_STORAGE_DIR="/path/to/writable/directory"
   ```

#### Encryption key problems

**Symptoms:**
- Cannot decrypt tokens
- Key file corruption errors

**Solutions:**
1. **Regenerate keys:**
   ```bash
   rm ~/.whoop-mcp-server/.encryption_key
   python setup.py
   ```

2. **Check file permissions:**
   ```bash
   chmod 600 ~/.whoop-mcp-server/.encryption_key
   chmod 600 ~/.whoop-mcp-server/tokens.json
   ```

## Diagnostic Commands

### Complete System Check
```bash
#!/bin/bash
echo "=== WHOOP MCP Server Diagnostics ==="

echo "1. Python Environment:"
python --version
which python

echo "2. Dependencies:"
pip show mcp httpx pydantic cryptography 2>/dev/null | grep Version

echo "3. Authentication Status:"
python -c "
import sys; sys.path.append('src')
try:
    from whoop_client import WhoopClient
    client = WhoopClient()
    print(client.get_auth_status())
except Exception as e:
    print(f'Error: {e}')
"

echo "4. Storage Directory:"
ls -la ~/.whoop-mcp-server/ 2>/dev/null || echo "Directory not found"

echo "5. Server Test:"
cd src && timeout 5 python whoop_mcp_server.py 2>&1 || echo "Server test completed"

echo "6. Network Connectivity:"
curl -s -I https://api.prod.whoop.com/developer/v1/ | head -1 2>/dev/null || echo "Network test failed"
```

### Enable Debug Logging
Add to Claude Desktop configuration:
```json
{
  "mcpServers": {
    "whoop": {
      "command": "python",
      "args": ["/path/to/whoop-mcp-server/src/whoop_mcp_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/whoop-mcp-server/src",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

## Log Analysis

### Common Log Messages

**Normal Operation:**
```
Starting Final WHOOP MCP Server with FastMCP...
Initializing WHOOP client...
WHOOP auth status: valid
FastMCP server ready
Tool called: get_whoop_profile
Profile result: John
```

**Python Path Issues:**
```
spawn python ENOENT
/opt/miniconda3/bin/python: can't open file '/Users/user/whoop-mcp-server/src/final_whoop_server.py': [Errno 2] No such file or directory
Server transport closed unexpectedly
```

**Solution for Python Path Issues:**
1. Use full Python path in config:
```json
{
  "command": "/opt/miniconda3/bin/python",  // Not just "python"
  "args": ["/full/path/to/whoop-mcp-server/src/whoop_mcp_server.py"]
}
```

2. Find your Python path:
```bash
which python3
which python
```

**Authentication Issues:**
```
WHOOP auth status: expired
Failed to refresh token
No valid access token available
```

**Network Issues:**
```
Request timeout
Connection refused
Rate limit exceeded
```

**Configuration Issues:**
```
ModuleNotFoundError: No module named 'whoop_client'
ImportError: cannot import name 'TokenManager'
FileNotFoundError: [Errno 2] No such file
```

### Log Locations

**macOS:**
- `~/Library/Logs/Claude/mcp-server-whoop.log`
- `~/Library/Logs/Claude/mcp.log`

**Windows:**
- `%LOCALAPPDATA%\Claude\logs\mcp-server-whoop.log`
- `%LOCALAPPDATA%\Claude\logs\mcp.log`

**Linux:**
- `~/.local/share/Claude/logs/mcp-server-whoop.log`
- `~/.local/share/Claude/logs/mcp.log`

## Getting Help

### Before Asking for Help

1. **Run diagnostics:** Use the diagnostic commands above
2. **Check logs:** Review error messages in detail
3. **Try basic fixes:** Restart, re-run setup, check paths
4. **Gather information:** Your OS, Python version, exact error messages

### Information to Include

When reporting issues, please provide:

1. **System Information:**
   - Operating System and version
   - Python version (`python --version`)
   - Claude Desktop version

2. **Error Details:**
   - Complete error messages
   - Relevant log entries
   - Steps to reproduce

3. **Configuration:**
   - Your Claude Desktop config (with paths anonymized)
   - Environment variables used
   - Installation method

### Where to Get Help

1. **GitHub Issues:** https://github.com/romanevstigneev/whoop-mcp-server/issues
2. **Documentation:** Check other docs in this folder
3. **WHOOP API Issues:** https://developer.whoop.com/

## Recovery Procedures

### Complete Reset
If nothing else works:

```bash
# 1. Remove all WHOOP MCP files
rm -rf ~/.whoop-mcp-server/
rm -rf /path/to/whoop-mcp-server/

# 2. Remove from Claude Desktop config
# Edit claude_desktop_config.json to remove "whoop" entry

# 3. Restart Claude Desktop

# 4. Fresh installation
git clone https://github.com/romanevstigneev/whoop-mcp-server.git
cd whoop-mcp-server
pip install -r requirements.txt
python setup.py

# 5. Reconfigure Claude Desktop
```

### Backup and Restore Tokens
```bash
# Backup tokens (before making changes)
cp ~/.whoop-mcp-server/tokens.json ~/.whoop-mcp-server/tokens.json.backup

# Restore tokens (if needed)
cp ~/.whoop-mcp-server/tokens.json.backup ~/.whoop-mcp-server/tokens.json
```

## Prevention Tips

1. **Keep backups** of working configurations
2. **Test changes** in a development environment first
3. **Monitor logs** regularly for early warning signs
4. **Update dependencies** periodically but carefully
5. **Document customizations** you make to the setup