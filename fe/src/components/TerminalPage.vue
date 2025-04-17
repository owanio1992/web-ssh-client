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
    const terminal = ref(null);

    onMounted(async () => {
      const term = new Terminal();
      const fitAddon = new FitAddon();
      term.loadAddon(fitAddon);
      term.open(document.getElementById('terminal'));
      fitAddon.fit();

      term.writeln('Welcome to the terminal!');
      term.writeln(`Connecting to ${site} - ${server}...`);

      try {
        const token = localStorage.getItem('token');
        const response = await axios.post(`${backendUrl}/api/connect_server`, {
          site: site,
          server: server
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
