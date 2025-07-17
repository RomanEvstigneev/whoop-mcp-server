#!/bin/bash

echo "🏃‍♂️ Setting up Whoop MCP Server..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ and try again."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'.' -f1 | cut -d'v' -f2)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18+ is required. Current version: $(node --version)"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.template .env
    echo "⚠️  Please edit .env file with your Whoop API credentials"
else
    echo "✅ .env file already exists"
fi

# Test the server
echo "🧪 Testing server..."
npm test

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Whoop API credentials"
echo "2. Add this server to your Claude Desktop configuration"
echo "3. Restart Claude Desktop"
echo ""
echo "See README.md for detailed instructions."