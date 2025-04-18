<template>
  <div>
    <h1>Terminal</h1>
    <p>Connecting to: {{ site }} - {{ server }}</p>
    <div id="terminal"></div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import 'xterm/css/xterm.css';
import axios from 'axios';
import { backendUrl } from '../config.js';

export default {
  setup() {
    const route = useRoute();
    const site = route.query.site;
    const server = route.query.server;
    const serverId = route.query.serverId; // Read serverId from query params
    const terminal = ref(null);

    onMounted(async () => {
      // Check and refresh token before proceeding
      const isAuthenticated = await checkAndRefreshToken();
      if (!isAuthenticated) {
        // Redirect to login if token refresh fails
        term.writeln('Authentication failed. Please log in again.');
        // Optionally redirect to login page after a delay
        // router.push('/login');
        return;
      }

      const term = new Terminal();
      const fitAddon = new FitAddon();
      term.loadAddon(fitAddon);
      term.open(document.getElementById('terminal'));
      fitAddon.fit();

      term.writeln('Welcome to the terminal!');
      term.writeln(`Connecting to ${site} - ${server}...`);

      try {
        const token = localStorage.getItem('token'); // Get the potentially new token
        // Send server_id instead of site/server names
        const response = await axios.post(`${backendUrl}/api/connect_server`, {
          server_id: serverId
        }, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        const websocketUrl = response.data.websocket_url;
        const ws = new WebSocket(websocketUrl);

        ws.onopen = () => {
          term.writeln('WebSocket connection established.');
        };

        ws.onmessage = (event) => {
          term.write(event.data);
        };

        ws.onclose = () => {
          term.writeln('WebSocket connection closed.');
        };

        ws.onerror = (error) => {
          console.error('WebSocket error:', error);
        };

      } catch (error) {
        console.error("Error connecting to server:", error);
        term.writeln('Error connecting to server. Please check the console.');
      }
    });

    // Function to check token expiry and refresh if needed
    const checkAndRefreshToken = async () => {
      const token = localStorage.getItem('token');
      const expiry = localStorage.getItem('expiry');
      const refreshToken = localStorage.getItem('refresh_token');

      if (!token || !expiry || !refreshToken) {
        // No token or expiry found, user is not logged in
        return false;
      }

      const currentTime = new Date().getTime();
      if (currentTime < parseInt(expiry)) {
        // Token is still valid
        return true;
      }

      // Token is expired, attempt to refresh
      try {
        const response = await axios.post(`${backendUrl}/api/token/refresh/`, {
          refresh: refreshToken
        });

        if (response.status === 200) {
          // Refresh successful, update tokens and expiry
          const newToken = response.data.access;
          const newExpiry = new Date().getTime() + (response.data.access_token_lifetime || 300) * 1000; // Assuming default 5 min if not provided
          
          localStorage.setItem('token', newToken);
          localStorage.setItem('expiry', newExpiry.toString());
          // Note: refresh token is typically longer lived and doesn't need to be refreshed every time

          console.log("Token refreshed successfully.");
          return true;
        } else {
          // Refresh failed
          console.error("Token refresh failed:", response.data);
          return false;
        }
      } catch (error) {
        console.error("Error during token refresh:", error);
        return false;
      }
    };

    return {
      terminal,
      site,
      server
    };
  }
}
</script>

<style scoped>
#terminal {
  width: 800px;
  height: 600px;
}
</style>
