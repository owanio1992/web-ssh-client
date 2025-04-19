<template>
  <div class="terminal-container">
    <h1>Terminal</h1>
    <p>Connecting to: {{ site }} - {{ server }}</p>
    <div id="terminal"></div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, reactive } from 'vue';
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
    const originalStyles = reactive({
      body: {},
      app: {}
    });

    onMounted(async () => {
      // Store original styles
      originalStyles.body = {
        margin: document.body.style.margin,
        padding: document.body.style.padding,
        overflow: document.body.style.overflow,
        height: document.body.style.height,
        width: document.body.style.width
      };
      const appEl = document.getElementById('app');
      if (appEl) {
        originalStyles.app = {
          margin: appEl.style.margin,
          padding: appEl.style.padding,
          maxWidth: appEl.style.maxWidth,
          height: appEl.style.height,
          display: appEl.style.display,
          flexDirection: appEl.style.flexDirection
        };
      }

      // Apply full screen styles
      document.body.style.margin = '0';
      document.body.style.padding = '0';
      document.body.style.overflow = 'hidden';
      document.body.style.height = '100vh';
      document.body.style.width = '100vw';

      if (appEl) {
        appEl.style.margin = '0';
        appEl.style.padding = '0';
        appEl.style.maxWidth = 'none';
        appEl.style.height = '100vh';
        appEl.style.width = '100%'; // Explicitly set width to 100%
        appEl.style.display = 'flex';
        appEl.style.flexDirection = 'column';
      }

      // Check and refresh token before proceeding
      const isAuthenticated = await checkAndRefreshToken();
      if (!isAuthenticated) {
        // Redirect to login if token refresh fails
        term.writeln('Authentication failed. Please log in again.');
        // Optionally redirect to login page after a delay
        // router.push('/login');
        return;
      }

      const term = new Terminal({
        copyOnSelect: true
      });
      const fitAddon = new FitAddon();
      term.loadAddon(fitAddon);
      document.title = `Connecting to: ${site} - ${server}`;
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
        console.log('Attempting to connect to WebSocket:', websocketUrl); // Added log
        const ws = new WebSocket(websocketUrl);

        ws.onopen = () => {
          console.log('WebSocket connection established.'); // Added log
          term.writeln('WebSocket connection established.');
        };

        ws.onmessage = (event) => {
          console.log('WebSocket message received:', event.data); // Added log
          try {
            const data = JSON.parse(event.data);
            if (data.type === 'time_update') {
              term.writeln(`Received time from backend: ${data.time}`);
            } else if (data.output) {
              term.write(data.output);
            } else {
              term.write(event.data);
            }
          } catch (e) {
            term.write(event.data);
          }
        };

        ws.onclose = () => {
          console.log('WebSocket connection closed.'); // Added log
          term.writeln('WebSocket connection closed.');
        };

        ws.onerror = (error) => {
          console.error('WebSocket error:', error); // Added log
        };

        // Handle user input from the terminal
        term.onData((data) => {
          if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ message: data }));
          }
        });

      } catch (error) {
        console.error("Error connecting to server:", error); // Added log
        term.writeln('Error connecting to server. Please check the console.');
      }
    });

    onUnmounted(() => {
      // Restore original styles
      document.body.style.margin = originalStyles.body.margin;
      document.body.style.padding = originalStyles.body.padding;
      document.body.style.overflow = originalStyles.body.overflow;
      document.body.style.height = originalStyles.body.height;
      document.body.style.width = originalStyles.body.width;

      const appEl = document.getElementById('app');
      if (appEl) {
        appEl.style.margin = originalStyles.app.margin;
        appEl.style.padding = originalStyles.app.padding;
        appEl.style.maxWidth = originalStyles.app.maxWidth;
        appEl.style.height = originalStyles.app.height;
        appEl.style.width = originalStyles.app.width; // Restore original width
        appEl.style.display = originalStyles.app.display;
        appEl.style.flexDirection = originalStyles.app.flexDirection;
      }
    });

    // Function to check token expiry and refresh if needed
    const checkAndRefreshToken = async () => {
      const token = localStorage.getItem('token');
      const expiry = localStorage.getItem('expiry');
      const refreshToken = localStorage.getItem('refresh_token');

      if (!token || !expiry || !refreshToken) {
        // No token or expiry found, user is not logged in
        console.log('No token, expiry, or refresh token found.'); // Added log
        return false;
      }

      const currentTime = new Date().getTime();
      if (currentTime < parseInt(expiry)) {
        // Token is still valid
        console.log('Token is still valid.'); // Added log
        return true;
      }

      // Token is expired, attempt to refresh
      console.log('Token expired, attempting refresh.'); // Added log
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
.terminal-container {
  display: flex;
  flex-direction: column;
  flex-grow: 1; /* Allow container to take remaining height */
  height: 100%; /* Use 100% of parent height */
  overflow: hidden; /* Prevent scrollbars on the container */
}

#terminal {
  flex-grow: 1; /* Allow terminal to take remaining space */
  width: 100% !important; /* Ensure terminal takes full width */
}
</style>
