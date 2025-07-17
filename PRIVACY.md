# 🔒 Privacy Policy - Whoop MCP Server

**Last Updated:** July 17, 2025

## 📋 Overview

This Privacy Policy explains how the Whoop MCP Server handles your personal health data when you use it with Claude Desktop. We are committed to protecting your privacy and being transparent about our data practices.

## 🔍 What This Server Does

The Whoop MCP Server is a **local application** that:
- Runs entirely on your computer
- Connects to the Whoop API on your behalf
- Provides your data to Claude Desktop when you request it
- Does not store or transmit your health data to any external servers

## 📊 Data We Access

### Health Data from Whoop API

When you use this server, it accesses the following data from your Whoop account:

- **Sleep Data**: Sleep duration, stages, efficiency, disturbances
- **Recovery Data**: Recovery scores, heart rate variability, resting heart rate
- **Workout Data**: Exercise sessions, duration, strain scores, calories burned
- **Cycle Data**: Daily strain, stress measurements, physiological cycles
- **Profile Data**: Basic profile information (name, email)
- **Body Measurements**: Height, weight, maximum heart rate

### Authentication Data

To access your Whoop data, the server uses:
- **OAuth Tokens**: Access tokens and refresh tokens
- **API Credentials**: Client ID and Client Secret from your Whoop developer app

## 🛡️ How We Protect Your Data

### Local Processing Only

- **No Cloud Storage**: Your health data is never stored on remote servers
- **No Database**: The server does not maintain any persistent storage of your data
- **Memory Only**: Data is only held in memory during request processing
- **Immediate Disposal**: All data is discarded after responding to your query

### Secure Communication

- **HTTPS Only**: All API communications use encrypted HTTPS
- **OAuth 2.0**: Industry-standard authentication protocol
- **Token Encryption**: Refresh tokens are securely stored locally
- **No Logging**: Health data is never logged to files

### Access Controls

- **Your Device Only**: The server only runs on your local machine
- **No Network Access**: No external network connections except to Whoop API
- **Authorization Required**: Each request requires your explicit authorization
- **Session-Based**: No persistent sessions or stored authentication

## 🔐 Data Storage and Retention

### What We Store

The server stores **only** the following on your local machine:
- **Configuration Files**: Server settings and preferences
- **Environment Variables**: API credentials in `.env` file
- **OAuth Tokens**: Access and refresh tokens for API authentication

### What We Don't Store

- **Health Data**: No sleep, recovery, workout, or biometric data
- **Personal Information**: No personally identifiable information
- **Usage Analytics**: No tracking of how you use the server
- **Query History**: No record of your questions or requests

### Data Retention

- **Health Data**: Immediately deleted after each request
- **OAuth Tokens**: Stored until you delete them or they expire
- **Configuration**: Stored until you uninstall the server

## 🚀 Data Sharing

### We Do NOT Share Your Data

- **No Third Parties**: Your data is never shared with any external services
- **No Analytics**: We don't collect or share usage analytics
- **No Advertising**: No data is used for advertising purposes
- **No Research**: Data is not used for research or development

### Claude Desktop Integration

- **Local Communication**: Data is only shared with Claude Desktop on your machine
- **Request-Response**: Data is only provided when you specifically ask for it
- **No Persistence**: Claude Desktop doesn't store your health data either

## 👤 Your Rights and Controls

### Data Access

- **Full Access**: You can access all your data through the Whoop app
- **API Access**: You control which data the server can access via OAuth scopes
- **Transparency**: You can view all server code and data handling

### Data Control

- **Revoke Access**: You can revoke API access at any time in your Whoop developer dashboard
- **Delete Tokens**: You can delete stored tokens by removing the `.env` file
- **Uninstall**: You can completely remove the server and all local data

### Data Portability

- **Whoop Export**: You can export your data directly from Whoop
- **API Access**: You have full access to your data via the Whoop API
- **No Lock-in**: Your data remains fully accessible outside this server

## 🔧 Technical Safeguards

### Security Measures

- **Encryption**: All data transmission is encrypted
- **Authentication**: OAuth 2.0 with proper token management
- **Validation**: Input validation and sanitization
- **Error Handling**: Secure error handling that doesn't leak data

### Code Security

- **Open Source**: All code is publicly available for review
- **No Backdoors**: No hidden data collection or transmission
- **Dependencies**: All dependencies are publicly audited
- **Regular Updates**: Security updates are applied promptly

## 📱 Third-Party Services

### Whoop API

- **Data Source**: We only access data through the official Whoop API
- **Whoop's Terms**: Your data is subject to [Whoop's Privacy Policy](https://www.whoop.com/privacy/)
- **API Limits**: We respect all Whoop API rate limits and terms

### Claude Desktop

- **Integration**: Data is only sent to Claude Desktop on your local machine
- **Anthropic's Terms**: Claude Desktop usage is subject to [Anthropic's Privacy Policy](https://www.anthropic.com/privacy)
- **Local Processing**: All AI processing happens locally through Claude Desktop

## 🌍 International Data Transfers

### Data Location

- **Local Processing**: All data processing happens on your local machine
- **No Transfers**: No international data transfers occur
- **Whoop API**: API calls go directly to Whoop's servers (US-based)

### Compliance

- **GDPR**: Compliant with EU data protection regulations
- **CCPA**: Compliant with California privacy laws
- **HIPAA**: While not a covered entity, we follow HIPAA-like practices

## 🔄 Changes to This Policy

### Updates

- **Notification**: We will notify users of any material changes
- **GitHub**: Updates will be posted on our GitHub repository
- **Version Control**: All changes are tracked in version control

### Your Consent

- **Continued Use**: Continued use after changes constitutes acceptance
- **Opt-Out**: You can stop using the server at any time
- **Feedback**: We welcome feedback on privacy practices

## 📞 Contact Information

### Questions or Concerns

If you have questions about this privacy policy:

- **GitHub Issues**: Open an issue on our [GitHub repository](https://github.com/yourusername/whoop-mcp-server/issues)
- **Discussions**: Join our [GitHub discussions](https://github.com/yourusername/whoop-mcp-server/discussions)
- **Email**: Contact us at [privacy@yourdomain.com](mailto:privacy@yourdomain.com)

### Data Protection Officer

For privacy-related inquiries:
- **Email**: [dpo@yourdomain.com](mailto:dpo@yourdomain.com)
- **Response Time**: We respond to privacy inquiries within 7 days

## ⚖️ Legal Basis

### Lawful Processing

Our processing of your data is based on:
- **Consent**: You explicitly consent by using the server
- **Legitimate Interest**: Providing the health data integration you requested
- **Necessary Performance**: Required to provide the service you requested

### Data Minimization

We follow the principle of data minimization:
- **Only Necessary Data**: We only access data needed for your requests
- **Minimal Retention**: Data is deleted immediately after use
- **Limited Scope**: OAuth scopes are limited to required permissions

## 🛠️ Technical Details

### Data Flow

1. **User Request**: You ask Claude Desktop about your health data
2. **API Call**: Server makes authenticated request to Whoop API
3. **Data Processing**: Server processes and formats the response
4. **Response**: Data is provided to Claude Desktop
5. **Cleanup**: All data is immediately deleted from memory

### Security Architecture

- **No Network Exposure**: Server only listens on localhost
- **Encrypted Storage**: OAuth tokens are stored securely
- **Process Isolation**: Server runs in isolated process
- **Memory Protection**: Health data is never swapped to disk

## 🎯 Summary

**In Plain English:**

- Your health data **never leaves your computer**
- We **don't store** any of your health information
- We **don't share** your data with anyone
- You have **full control** over what data we access
- You can **revoke access** or **delete everything** at any time
- All code is **open source** and publicly auditable

This server is designed with privacy-first principles to give you secure, local access to your own health data through Claude Desktop.

---

**Questions?** Please don't hesitate to reach out through our GitHub repository or email us directly.