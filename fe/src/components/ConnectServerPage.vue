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
      mergedServerData: {},
    };
  },
  async mounted() {
    await this.fetchData();
    console.log("mergedServerData:", this.mergedServerData); // Print merged data to console
  },
  methods: {
    async fetchData() {
      try {
        const token = localStorage.getItem('token');

        // Fetch current user
        const userResponse = await axios.get(`${backendUrl}/api/user`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        const user = userResponse.data;
        console.log("User:", user);
        const userId = user.id;

        // Fetch user roles
        const userRolesResponse = await axios.get(`${backendUrl}/api/users/${userId}/roles/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        const userRoles = userRolesResponse.data;
        console.log("User Roles:", userRoles);

        // Check if userRoles is an array
        if (!Array.isArray(userRoles)) {
          console.error("userRoles is not an array:", userRoles);
          return; // Exit the function if userRoles is not an array
        }

        // Fetch all servers
        const serversResponse = await axios.get(`${backendUrl}/api/servers/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        const servers = serversResponse.data;

        // Merge data
        this.mergedServerData = this.mergeServerData(servers);
        this.sites = Object.keys(this.mergedServerData);

        // Create mergedRoleData
        const mergedRoleData = this.createMergedRoleData(servers, userRoles);
        console.log("mergedRoleData:", mergedRoleData);

        if (Object.keys(this.mergedServerData).length === 0) {
          alert("No servers available for your roles.");
        }

      } catch (error) {
        console.error("Error fetching data:", error);
        alert("Failed to fetch data. Please check the console.");
      }
    },
    mergeServerData(servers) {
      const merged = {};
      servers.forEach(server => {
        if (!merged[server.site_name]) {
          merged[server.site_name] = [];
        }
        merged[server.site_name].push(server.server_name);
      });
      return merged;
    },
    async createMergedRoleData(servers, userRoles) {
      const merged = {};
      for (const role of userRoles) {
        if (typeof role === 'object' && role !== null && role.id) {
          try {
            const token = localStorage.getItem('token');
            const roleResponse = await axios.get(`${backendUrl}/api/roles/${role.id}/`, {
              headers: {
                Authorization: `Bearer ${token}`
              }
            });
            const roleData = roleResponse.data;
            merged[role.id] = [];
            roleData.permissions.forEach(server => {
              merged[role.id].push({
                site: server.site_name,
                server: server.server_name
              });
            });
          } catch (error) {
            console.error("Error fetching role:", error);
          }
        } else {
          console.warn("Invalid role object:", role);
        }
      }
      return merged;
    },
    updateServers(site) {
      this.selectedServer = null;
      this.servers = this.mergedServerData[site] || [];
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
