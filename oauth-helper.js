#!/usr/bin/env node

import axios from 'axios';
import readline from 'readline';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

console.log('🔐 Whoop OAuth Helper');
console.log('This script will help you get your refresh token for the Whoop API.');
console.log('');

async function getRefreshToken() {
  try {
    const clientId = await askQuestion('Enter your Whoop Client ID: ');
    const clientSecret = await askQuestion('Enter your Whoop Client Secret: ');
    const redirectUri = await askQuestion('Enter your redirect URI (e.g., http://localhost:3000/callback): ');
    
    console.log('');
    console.log('📋 Step 1: Visit this URL to authorize your app:');
    console.log('');
    const authUrl = `https://api.prod.whoop.com/oauth/oauth2/auth?response_type=code&client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&scope=read:recovery read:sleep read:workout read:profile read:body_measurement read:cycles&state=random_state_string`;
    console.log(authUrl);
    console.log('');
    
    const authCode = await askQuestion('After authorizing, enter the "code" parameter from the redirect URL: ');
    
    console.log('');
    console.log('🔄 Exchanging code for tokens...');
    
    const tokenResponse = await axios.post('https://api.prod.whoop.com/oauth/oauth2/token', {
      grant_type: 'authorization_code',
      code: authCode,
      redirect_uri: redirectUri,
      client_id: clientId,
      client_secret: clientSecret
    });
    
    console.log('');
    console.log('✅ Success! Here are your tokens:');
    console.log('');
    console.log('Access Token:', tokenResponse.data.access_token);
    console.log('Refresh Token:', tokenResponse.data.refresh_token);
    console.log('');
    console.log('🔧 Add these to your .env file:');
    console.log('');
    console.log(`WHOOP_CLIENT_ID=${clientId}`);
    console.log(`WHOOP_CLIENT_SECRET=${clientSecret}`);
    console.log(`WHOOP_REFRESH_TOKEN=${tokenResponse.data.refresh_token}`);
    console.log('');
    
  } catch (error) {
    console.error('❌ Error:', error.response?.data || error.message);
  }
  
  rl.close();
}

function askQuestion(question) {
  return new Promise((resolve) => {
    rl.question(question, resolve);
  });
}

getRefreshToken();