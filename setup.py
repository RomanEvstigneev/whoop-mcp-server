#!/usr/bin/env python3
"""
WHOOP MCP Server Setup Script
Interactive setup for WHOOP OAuth authorization
"""
import os
import sys
import webbrowser
import requests
import json
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.auth_manager import TokenManager
from src.config import OAUTH_AUTH_URL, OAUTH_TOKEN_URL

class Colors:
    """Terminal colors for better UX"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_colored(text, color=Colors.ENDC):
    """Print colored text"""
    print(f"{color}{text}{Colors.ENDC}")

def print_banner():
    """Print setup banner"""
    print_colored("=" * 60, Colors.HEADER)
    print_colored("🏃 WHOOP MCP Server Setup", Colors.HEADER)
    print_colored("=" * 60, Colors.HEADER)
    print_colored("This setup will help you connect your WHOOP account to Claude Desktop", Colors.OKBLUE)
    print()

def check_dependencies():
    """Check if required dependencies are installed"""
    print_colored("🔍 Checking dependencies...", Colors.OKBLUE)
    
    try:
        import mcp
        import httpx
        import pydantic
        import cryptography
        print_colored("✅ All dependencies are installed", Colors.OKGREEN)
        return True
    except ImportError as e:
        print_colored(f"❌ Missing dependency: {e}", Colors.FAIL)
        print_colored("Please install dependencies:", Colors.WARNING)
        print_colored("pip install -r requirements.txt", Colors.WARNING)
        return False

def setup_storage():
    """Create storage directory if it doesn't exist"""
    storage_dir = Path("storage")
    storage_dir.mkdir(exist_ok=True)
    print_colored(f"📁 Storage directory ready: {storage_dir.absolute()}", Colors.OKGREEN)

def get_authorization_code():
    """Get authorization code from user"""
    print_colored("\n🔐 WHOOP OAuth Authorization", Colors.HEADER)
    print_colored("Step 1: We'll open your browser to authorize WHOOP access", Colors.OKBLUE)
    print_colored("Step 2: After authorization, you'll get a success page", Colors.OKBLUE)
    print_colored("Step 3: Copy the authorization code from the success page", Colors.OKBLUE)
    print()
    
    # Ask user if they want to continue
    response = input("Ready to start authorization? (y/n): ").lower().strip()
    if response != 'y':
        print_colored("Setup cancelled by user", Colors.WARNING)
        return None
    
    # Open browser
    print_colored(f"🌐 Opening browser: {OAUTH_AUTH_URL}", Colors.OKBLUE)
    try:
        webbrowser.open(OAUTH_AUTH_URL)
    except Exception as e:
        print_colored(f"⚠️ Could not open browser automatically: {e}", Colors.WARNING)
        print_colored(f"Please manually open: {OAUTH_AUTH_URL}", Colors.WARNING)
    
    print()
    print_colored("After authorizing in the browser:", Colors.OKBLUE)
    print_colored("1. You'll see a success page", Colors.OKBLUE)
    print_colored("2. Look for the authorization code (long string)", Colors.OKBLUE)
    print_colored("3. Copy the ENTIRE authorization code", Colors.OKBLUE)
    print()
    
    # Get authorization code from user
    auth_code = input("📝 Paste the authorization code here: ").strip()
    
    if not auth_code:
        print_colored("❌ No authorization code provided", Colors.FAIL)
        return None
    
    # Validate format (basic check)
    if len(auth_code) < 20:
        print_colored("⚠️ Authorization code seems too short. Please check and try again.", Colors.WARNING)
        return None
    
    return auth_code

def exchange_code_for_tokens(auth_code):
    """Exchange authorization code for tokens"""
    print_colored("\n🔄 Exchanging authorization code for tokens...", Colors.OKBLUE)
    
    try:
        # Make request to our OAuth app
        url = f"{OAUTH_TOKEN_URL}/{auth_code}"
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            token_data = response.json()
            
            if token_data.get('success'):
                print_colored("✅ Successfully obtained tokens!", Colors.OKGREEN)
                return token_data
            else:
                print_colored(f"❌ Token exchange failed: {token_data.get('error', 'Unknown error')}", Colors.FAIL)
                return None
        else:
            print_colored(f"❌ HTTP Error {response.status_code}: {response.text}", Colors.FAIL)
            return None
            
    except requests.exceptions.Timeout:
        print_colored("❌ Request timed out. Please check your internet connection.", Colors.FAIL)
        return None
    except requests.exceptions.RequestException as e:
        print_colored(f"❌ Network error: {e}", Colors.FAIL)
        return None
    except Exception as e:
        print_colored(f"❌ Unexpected error: {e}", Colors.FAIL)
        return None

def save_tokens(token_data):
    """Save tokens using TokenManager"""
    print_colored("💾 Saving tokens securely...", Colors.OKBLUE)
    
    try:
        token_manager = TokenManager()
        token_manager.save_tokens(token_data)
        print_colored("✅ Tokens saved successfully!", Colors.OKGREEN)
        return True
    except Exception as e:
        print_colored(f"❌ Failed to save tokens: {e}", Colors.FAIL)
        return False

def verify_setup():
    """Verify that setup was successful"""
    print_colored("\n🔍 Verifying setup...", Colors.OKBLUE)
    
    try:
        token_manager = TokenManager()
        token_info = token_manager.get_token_info()
        
        if token_info['status'] == 'no_tokens':
            print_colored("❌ No tokens found after setup", Colors.FAIL)
            return False
        
        if token_info['status'] == 'expired':
            print_colored("⚠️ Tokens are expired, but setup completed", Colors.WARNING)
            print_colored("   The refresh token should allow automatic renewal", Colors.WARNING)
        else:
            print_colored("✅ Valid tokens found", Colors.OKGREEN)
        
        print_colored(f"   Token type: {token_info['token_type']}", Colors.OKBLUE)
        print_colored(f"   Expires at: {token_info['expires_at']}", Colors.OKBLUE)
        print_colored(f"   Has refresh token: {token_info['has_refresh_token']}", Colors.OKBLUE)
        
        return True
        
    except Exception as e:
        print_colored(f"❌ Setup verification failed: {e}", Colors.FAIL)
        return False

def show_claude_config():
    """Show Claude Desktop configuration"""
    print_colored("\n🤖 Claude Desktop Configuration", Colors.HEADER)
    print_colored("Add this to your Claude Desktop settings:", Colors.OKBLUE)
    print()
    
    # Get absolute path
    server_path = Path(__file__).parent / "src" / "whoop_mcp_server.py"
    
    config = {
        "mcpServers": {
            "whoop": {
                "command": "python",
                "args": [str(server_path.absolute())]
            }
        }
    }
    
    print_colored("Configuration JSON:", Colors.OKGREEN)
    print_colored(json.dumps(config, indent=2), Colors.OKGREEN)
    print()
    
    # Platform-specific instructions
    if sys.platform == "darwin":  # macOS
        print_colored("📍 Claude Desktop settings location (macOS):", Colors.OKBLUE)
        print_colored("~/Library/Application Support/Claude/claude_desktop_config.json", Colors.OKBLUE)
    elif sys.platform == "win32":  # Windows
        print_colored("📍 Claude Desktop settings location (Windows):", Colors.OKBLUE)
        print_colored("%APPDATA%\\Claude\\claude_desktop_config.json", Colors.OKBLUE)
    else:  # Linux
        print_colored("📍 Claude Desktop settings location (Linux):", Colors.OKBLUE)
        print_colored("~/.config/claude/claude_desktop_config.json", Colors.OKBLUE)

def show_usage_examples():
    """Show usage examples"""
    print_colored("\n💡 Usage Examples", Colors.HEADER)
    print_colored("Once configured, you can ask Claude:", Colors.OKBLUE)
    print()
    print_colored("• \"Show my WHOOP profile\"", Colors.OKGREEN)
    print_colored("• \"What were my workouts this week?\"", Colors.OKGREEN)
    print_colored("• \"How is my recovery trending?\"", Colors.OKGREEN)
    print_colored("• \"Show my sleep data for the last 7 days\"", Colors.OKGREEN)
    print_colored("• \"What's my HRV looking like?\"", Colors.OKGREEN)
    print()

def main():
    """Main setup function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup storage
    setup_storage()
    
    # Check if already configured
    try:
        token_manager = TokenManager()
        token_info = token_manager.get_token_info()
        
        if token_info['status'] in ['valid', 'expired']:
            print_colored("⚠️ WHOOP tokens already exist", Colors.WARNING)
            print_colored(f"   Status: {token_info['status']}", Colors.WARNING)
            print_colored(f"   Expires: {token_info['expires_at']}", Colors.WARNING)
            print()
            
            response = input("Reconfigure anyway? (y/n): ").lower().strip()
            if response != 'y':
                print_colored("Setup cancelled. Existing tokens preserved.", Colors.WARNING)
                show_claude_config()
                show_usage_examples()
                return
    except Exception:
        pass  # No existing tokens, continue with setup
    
    # Get authorization code
    auth_code = get_authorization_code()
    if not auth_code:
        sys.exit(1)
    
    # Exchange for tokens
    token_data = exchange_code_for_tokens(auth_code)
    if not token_data:
        sys.exit(1)
    
    # Save tokens
    if not save_tokens(token_data):
        sys.exit(1)
    
    # Verify setup
    if not verify_setup():
        sys.exit(1)
    
    # Show success and configuration
    print_colored("\n🎉 Setup Complete!", Colors.OKGREEN)
    print_colored("Your WHOOP account is now connected to the MCP server!", Colors.OKGREEN)
    
    show_claude_config()
    show_usage_examples()
    
    print_colored("\n🚀 Next Steps:", Colors.HEADER)
    print_colored("1. Add the configuration to Claude Desktop", Colors.OKBLUE)
    print_colored("2. Restart Claude Desktop", Colors.OKBLUE)
    print_colored("3. Start asking Claude about your WHOOP data!", Colors.OKBLUE)
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\n⚠️ Setup interrupted by user", Colors.WARNING)
        sys.exit(1)
    except Exception as e:
        print_colored(f"\n❌ Unexpected error: {e}", Colors.FAIL)
        sys.exit(1)