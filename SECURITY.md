# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Currently supported versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them privately by emailing: **evstigneevromanv@gmail.com**

Please include:
- A description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if you have one)

You can expect:
- Acknowledgment within 48 hours
- Initial assessment within 1 week
- Regular updates on our progress
- Credit in the release notes (unless you prefer to remain anonymous)

## Security Best Practices

When using WHOOP MCP Server:

### 🔐 Token Security
- Never share your WHOOP tokens with anyone
- Tokens are encrypted and stored locally only
- Regularly check your WHOOP account for suspicious activity
- Revoke access if you suspect compromise

### 🛡️ System Security
- Keep your system and Python dependencies updated
- Use strong passwords for your WHOOP account
- Enable 2FA on your WHOOP account if available
- Run the MCP server in a secure environment

### 🔒 Data Privacy
- This tool stores data locally on your machine only
- No data is sent to third parties except WHOOP
- Review the source code to understand data handling
- Delete stored tokens when uninstalling

### ⚠️ Network Security
- The tool connects to:
  - WHOOP API servers (`api.prod.whoop.com`)
  - OAuth service (`personal-integrations-462307.uc.r.appspot.com`)
- Ensure your network connection is secure
- Use HTTPS connections only

## Security Features

### Encryption
- All tokens are encrypted using AES-256 via Python's `cryptography` library
- Encryption keys are stored with restricted file permissions (600)
- Token files have restricted permissions (600)

### Authentication
- Uses OAuth 2.0 with PKCE for secure authorization
- Automatic token refresh to minimize exposure
- No long-term storage of passwords

### Data Handling
- Minimal data collection - only what's needed for functionality
- Local-only storage - no cloud synchronization
- Secure token cleanup on uninstall

## Known Security Considerations

### External Dependencies
- Relies on external OAuth service for initial setup
- WHOOP API rate limiting provides some DDoS protection
- Dependencies are regularly updated for security patches

### Threat Model
This tool is designed for:
- ✅ Personal use on trusted devices
- ✅ Secure home networks
- ✅ Users who understand the risks

This tool is NOT designed for:
- ❌ Shared or public computers
- ❌ Production server environments
- ❌ Untrusted network environments
- ❌ Multiple user scenarios

## Responsible Disclosure

We believe in responsible disclosure. If you discover a security vulnerability:

1. **Do not** create a public issue
2. **Do** send details to the security email
3. **Do** give us reasonable time to address the issue
4. **Do** follow coordinated disclosure practices

We commit to:
- Acknowledging receipt of your report
- Working with you to understand and validate the issue
- Developing and testing a fix
- Releasing a security advisory and patch
- Giving appropriate credit (if desired)

Thank you for helping keep WHOOP MCP Server secure! 🛡️