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
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import 'xterm/css/xterm.css';
import { backendUrl } from '../config.js';
import TerminalPage from './TerminalPage.vue';

export default {
  name: 'ConnectServerPage',
  components: {
    vSelect,
    TerminalPage,
  },
  data() {
    return {
      selectedSite: null,
      selectedServer: null,
      sites: [],
      servers: [],
    };
  },
  async mounted() {
    await this.fetchData();
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
        const userId = user.id;

        // Fetch user roles
        const userRolesResponse = await axios.get(`${backendUrl}/api/users/${userId}/roles/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        const userRoles = userRolesResponse.data;

        // Check if userRoles is an array
        if (!Array.isArray(userRoles)) {
          console.error("userRoles is not an array:", userRoles);
          return; // Exit the function if userRoles is not an array
        }

        // Fetch permissions for all user roles concurrently
        const roleServers = (await Promise.all(
          userRoles.map(role =>
            axios.get(`${backendUrl}/api/roles/${role.id}/`, {
              headers: {
                Authorization: `Bearer ${token}`
              }
            })
          )
        )).flatMap(roleResponse => roleResponse.data.permissions);

        // Use mergeServerData to format roleServers
        const formattedRoleServers = this.mergeServerData(roleServers);
        this.roleServers = formattedRoleServers;
        this.sites = Object.keys(formattedRoleServers);

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
    updateServers(site) {
      this.selectedServer = null;
      this.servers = this.roleServers[site] || [];
    },
    async connectToServer() {
      if (this.selectedSite && this.selectedServer) {
        window.open('/terminal/index.html', '_blank');
      }
    },
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
