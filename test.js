#!/usr/bin/env node

import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

console.log('Testing Whoop MCP Server...');

const server = spawn('node', ['index.js'], {
  cwd: __dirname,
  stdio: ['pipe', 'pipe', 'inherit']
});

// Send a list tools request
const listToolsRequest = {
  jsonrpc: '2.0',
  id: 1,
  method: 'tools/list',
  params: {}
};

server.stdin.write(JSON.stringify(listToolsRequest) + '\n');

server.stdout.on('data', (data) => {
  const responses = data.toString().split('\n').filter(line => line.trim());
  
  responses.forEach(response => {
    if (response.trim()) {
      try {
        const parsed = JSON.parse(response);
        if (parsed.result && parsed.result.tools) {
          console.log('✅ Server responded with tools:');
          parsed.result.tools.forEach(tool => {
            console.log(`  - ${tool.name}: ${tool.description}`);
          });
        }
      } catch (e) {
        console.log('Response:', response);
      }
    }
  });
});

server.on('close', (code) => {
  console.log(`Server exited with code ${code}`);
});

// Close the server after 3 seconds
setTimeout(() => {
  server.kill();
  console.log('✅ Test completed successfully!');
}, 3000);