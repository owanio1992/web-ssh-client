<template>
  <div>
    <h1>Connect to Server</h1>
    <p>Select a site and server to connect to.</p>

    <label for="site">Site:</label>
    <v-select
      id="site"
      v-model="selectedSite"
      :options="sites"
      @input="updateServers"
      :reduce="site => site"
      label="site"
    />

    <label for="server">Server:</label>
    <v-select
      id="server"
      v-model="selectedServer"
      :options="servers"
      :reduce="server_name => server_name"
      label="server_name"
    />

    <button @click="connectToServer">Connect</button>
  </div>
</template>

<script>
import vSelect from 'vue-select';
import 'vue-select/dist/vue-select.css';
import axios from 'axios';
import { backendUrl } from '../config.js';

export default {
  name: 'ConnectServerPage',
  components: {
    vSelect
  },
  data() {
    return {
      selectedSite: null,
      selectedServer: null,
      sites: [],
      servers: [],
      mergedData: {},
    };
  },
  async mounted() {
    await this.fetchData();
    console.log("Merged Data:", this.mergedData); // Print merged data to console
  },
  methods: {
    async fetchData() {
      try {
        const token = localStorage.getItem('token');
        const serversResponse = await axios.get(`${backendUrl}/api/servers/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        const servers = serversResponse.data;

        // Merge data
        this.mergedData = this.mergeData(servers);
        this.sites = Object.keys(this.mergedData);

      } catch (error) {
        console.error("Error fetching data:", error);
        alert("Failed to fetch data. Please check the console.");
      }
    },
    mergeData(servers) {
      const merged = {};
      servers.forEach(server => {
        if (!merged[server.site_name]) {
          merged[server.site_name] = [];
        }
        merged[server.site_name].push(server.server_name);
      });
      return merged;
    },
    updateServers(site) {
      this.selectedServer = null;
      this.servers = this.mergedData[site] || [];
    },
    connectToServer() {
      if (this.selectedSite && this.selectedServer) {
        const url = `/terminal/${this.selectedSite}-${this.selectedServer}`;
        window.open(url, '_blank');
      } else {
        alert('Please select a site and server.');
      }
    }
  },
  watch: {
    selectedSite(newVal) {
      if (newVal) {
        this.updateServers(newVal);
      } else {
        this.servers = [];
        this.selectedServer = null;
      }
    }
  }
};
</script>

<style scoped>
label {
  display: block;
  margin-top: 10px;
}

.v-select {
  width: 200px;
  margin-top: 5px;
}

button {
  margin-top: 10px;
  padding: 5px 10px;
  cursor: pointer;
}
</style>
