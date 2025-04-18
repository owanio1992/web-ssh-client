<template>
  <div class="manage-servers">
    <h1>Manage Servers</h1>
    <div class="tab-buttons">
      <button :class="{ active: activeTab === 'add' }" @click="activeTab = 'add'">Add Server</button>
      <button :class="{ active: activeTab === 'delete' }" @click="activeTab = 'delete'">Delete Server</button>
    </div>

    <div v-if="activeTab === 'add'" class="add-server-form">
      <h2>Add New Server</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="siteName">Site Name:</label>
          <input type="text" id="siteName" v-model="newServer.siteName" required />
        </div>
        <div class="form-group">
          <label for="serverName">Server Name:</label>
          <input type="text" id="serverName" v-model="newServer.serverName" required />
        </div>
        <div class="form-group">
          <label for="user">User:</label>
          <input type="text" id="user" v-model="newServer.user" required />
        </div>
        <div class="form-group">
          <label for="host">Host:</label>
          <input type="text" id="host" v-model="newServer.host" required />
        </div>
        <div class="form-group">
          <label for="sshKeyName">SSH Key Name:</label>
          <v-select
            id="sshKeyName"
            :options="sshKeys"
            :reduce="key => key.id"
            label="name"
            v-model="newServer.sshKeyName"
            required
            placeholder="Select SSH Key"
          >
            <template #search="{ attributes, events }">
              <input
                class="vs__search"
                :required="!newServer.sshKeyName"
                v-bind="attributes"
                v-on="events"
              />
            </template>
          </v-select>
        </div>
        <div class="form-group">
          <label for="proxyServerName">Proxy Server:</label>
          <v-select
            id="proxyServerName"
            :options="proxyServers"
            :reduce="key => key.id"
            :get-option-label="server => `${server.site_name} - ${server.server_name}`"
            v-model="newServer.proxyServerName"
            placeholder="Select Proxy Server"
          >
            <template #search="{ attributes, events }">
              <input
                class="vs__search"
                v-bind="attributes"
                v-on="events"
              />
            </template>
          </v-select>
        </div>
        <button type="submit">Add Server</button>
      </form>
    </div>

    <div v-if="activeTab === 'delete'">
      <input type="text" v-model="searchQuery" placeholder="Search Servers" />
      <table>
        <thead>
          <tr>
            <th>Site Name</th>
            <th>Server Name</th>
            <th>User</th>
            <th>Host</th>
            <th>SSH Key Name</th>
            <th>Proxy Server</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="server in filteredServers" :key="server.id">
            <td>{{ server.site_name }}</td>
            <td>{{ server.server_name }}</td>
            <td>{{ server.user }}</td>
            <td>{{ server.host }}</td>
            <td>{{ server.ssh_key_name }}</td>
            <td>{{ server.proxy_server_name }}</td>
            <td>
              <button @click="deleteServer(server)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <Notification
      :message="notificationMessage"
      :type="notificationType"
      :trigger="notificationTrigger"
    />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { backendUrl } from '../config.js';
import Notification from './Notification.vue';
import vSelect from 'vue-select';
import 'vue-select/dist/vue-select.css'; // Import vue-select CSS

export default {
  components: {
    Notification,
    vSelect
  },
  setup() {
    const activeTab = ref('add');
    const servers = ref([]);
    const newServer = ref({
      siteName: '',
      serverName: '',
      user: '',
      host: '',
      sshKeyName: '',
      proxyServerName: '',
    });
    const sshKeys = ref([]);
    const proxyServers = ref([]);
    const searchQuery = ref('');
    const notificationMessage = ref('');
    const notificationType = ref('success');
    const notificationTrigger = ref(0);

    const fetchServers = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${backendUrl}/api/servers/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        console.log('API Response:', response);
        if (Array.isArray(response.data)) {
          servers.value = response.data;
        } else {
          servers.value = [];
          console.error('API returned non-array data for servers:', response.data);
        }
        console.log('Type of servers.value:', typeof servers.value);
      } catch (error) {
        console.error('Error fetching servers:', error);
      } finally {
        // Optional: Add any cleanup code here
      }
    };

    const fetchSSHKeys = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${backendUrl}/api/ssh-keys/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        sshKeys.value = response.data;
        console.log('SSH Keys fetched:', sshKeys.value);
      } catch (error) {
        console.error('Error fetching SSH keys:', error);
      }
    };

    const fetchProxyServers = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${backendUrl}/api/servers/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        // Filter out the current server being created
        proxyServers.value = response.data.filter(server => server.id !== newServer.value.id);
        console.log('Proxy Servers fetched:', proxyServers.value);
      } catch (error) {
        console.error('Error fetching proxy servers:', error);
      }
    };

    onMounted(async () => {
      fetchServers();
      fetchSSHKeys();
      fetchProxyServers();
      console.log('ManageServers component mounted');
    });

    const filteredServers = computed(() => {
      return servers.value.filter((server) =>
        server.server_name && server.server_name.toLowerCase().includes(searchQuery.value.toLowerCase())
      );
    });

    const handleSubmit = async () => {
      // Handle form submission here
      console.log('Form submitted:', newServer.value);
      try {
        const token = localStorage.getItem('token');
        await axios.post(`${backendUrl}/api/servers/add/`, {
          site_name: newServer.value.siteName,
          server_name: newServer.value.serverName,
          user: newServer.value.user,
          host: newServer.value.host,
          ssh_key: newServer.value.sshKeyName, // Use sshKeyName for ssh_key_id
          proxy_server: newServer.value.proxyServerName,
        }, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        // Refresh server list after adding a new server
        fetchServers();
        // Clear the form
        newServer.value = {
          siteName: '',
          serverName: '',
          user: '',
          host: '',
          sshKeyName: '',
          proxyServerName: '',
        };
        // Refresh proxy servers list
        fetchProxyServers();
        // Show success notification
        notificationMessage.value = 'Server added successfully!';
        notificationType.value = 'success';
        notificationTrigger.value++;
      } catch (error) {
        console.error('Error adding server:', error);
        let errorMessage = 'Error adding server.';
        if (error.response && error.response.data && error.response.data.error) {
          errorMessage = error.response.data.error; // Use specific error from backend
        }
        // Show error notification
        notificationMessage.value = errorMessage;
        notificationType.value = 'error';
        notificationTrigger.value++;
      }
    };

    const deleteServer = async (server) => {
      if (confirm(`Are you sure you want to delete the server "${server.server_name}"?`)) {
        try {
          const token = localStorage.getItem('token');
          await axios.delete(`${backendUrl}/api/servers/${server.id}/delete/`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          fetchServers();
          // Show success notification
          notificationMessage.value = 'Server deleted successfully!';
          notificationType.value = 'success';
          notificationTrigger.value++;
        } catch (error) {
          console.error('Error deleting server:', error);
          // Show error notification
          notificationMessage.value = 'Error deleting server.';
          notificationType.value = 'error';
          notificationTrigger.value++;
        }
      }
    };

    return {
      activeTab,
      servers,
      newServer,
      sshKeys,
      handleSubmit,
      filteredServers,
      deleteServer,
      fetchServers,
      searchQuery,
      notificationMessage,
      notificationType,
      notificationTrigger,
      proxyServers,
    };
  },
};
</script>

<style scoped>
.manage-servers {
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}

.tab-buttons {
  display: flex;
  margin-bottom: 10px;
}

.tab-buttons button {
  padding: 10px 20px;
  border: none;
  background-color: #f2f2f2;
  cursor: pointer;
  margin-right: 5px;
}

.tab-buttons button.active {
  background-color: #ddd;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 8px;
  border: 1px solid #ccc;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

button {
  padding: 5px 10px;
  margin-right: 5px;
  cursor: pointer;
}

.add-server-form {
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

/* Removed custom .vs__... styles */

</style>
