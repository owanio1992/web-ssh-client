<template>
  <div>
    <h2>Manage Server List</h2>
    <nav>
      <button :class="{ active: activeTab === 'add' }" @click="activeTab = 'add'">Add Server</button>
      <button :class="{ active: activeTab === 'delete' }" @click="activeTab = 'delete'">Delete Server</button>
    </nav>

    <div v-if="activeTab === 'add'">
      <h3>Add Server</h3>
      <form @submit.prevent="addServer">
        <div>
          <label for="siteName">Site Name:</label>
          <input type="text" id="siteName" v-model="newServer.siteName" required>
        </div>
        <div>
          <label for="serverName">Server Name:</label>
          <input type="text" id="serverName" v-model="newServer.serverName" required>
        </div>
        <div>
          <label for="user">User:</label>
          <input type="text" id="user" v-model="newServer.user" required>
        </div>
        <div>
          <label for="host">Host:</label>
          <input type="text" id="host" v-model="newServer.host" required>
        </div>
        <div>
          <label for="sshKey">SSH Key:</label>
          <select id="sshKey" v-model="newServer.sshKey" required>
            <option v-for="key in sshKeys" :key="key.id" :value="key.id">{{ key.name }}</option>
          </select>
        </div>
        <button type="submit">Add Server</button>
      </form>
    </div>

    <div v-if="activeTab === 'delete'">
      <h3>Delete Server</h3>
      <ul>
        <li v-for="server in servers" :key="server.id">
          {{ server.site_name }} - {{ server.server_name }}
          <button @click="deleteServer(server.id)">Delete</button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { backendUrl } from '../config.js';

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export default {
  setup() {
    const activeTab = ref('add');
    const newServer = ref({
      siteName: '',
      serverName: '',
      user: '',
      host: '',
      sshKey: ''
    });
    const servers = ref([]);
    const sshKeys = ref([]);

    onMounted(async () => {
      try {
        const sshKeysResponse = await fetch(backendUrl + '/api/ssh-keys/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (!sshKeysResponse.ok) {
          throw new Error('Failed to fetch SSH keys');
        }
        const sshKeysData = await sshKeysResponse.json();
        sshKeys.value = sshKeysData;

        const serversResponse = await fetch(backendUrl + '/api/servers/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (!serversResponse.ok) {
          throw new Error('Failed to fetch servers');
        }
        const serversData = await serversResponse.json();
        servers.value = serversData;
      } catch (error) {
        console.error('Error fetching data:', error);
        alert('Failed to fetch data: ' + error.message);
      }
    });

    const addServer = async () => {
      try {
        const csrftoken = getCookie('csrftoken');
        const response = await fetch(backendUrl + '/api/servers/add/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'X-CSRFToken': csrftoken
          },
          body: JSON.stringify({
            site_name: newServer.value.siteName,
            server_name: newServer.value.serverName,
            user: newServer.value.user,
            host: newServer.value.host,
            ssh_key: newServer.value.sshKey
          })
        });
        if (!response.ok) {
          throw new Error('Failed to add server');
        }
        const data = await response.json();
        console.log('Server added:', data);
        alert('Server added: ' + data.message);
      } catch (error) {
        console.error('Error adding server:', error);
        alert('Failed to add server: ' + error.message);
      }
    };

    const deleteServer = async (serverId) => {
      try {
        const response = await fetch(backendUrl + '/api/servers/' + serverId + '/delete/', {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (!response.ok) {
          throw new Error('Failed to delete server');
        }
        const data = await response.json();
        console.log('Server deleted:', data);
        alert('Server deleted: ' + data.message);
        // Refresh the server list
        const serversResponse = await fetch(backendUrl + '/api/servers/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (!serversResponse.ok) {
          throw new Error('Failed to fetch servers');
        }
        const serversData = await serversResponse.json();
        servers.value = serversData;
      } catch (error) {
        console.error('Error deleting server:', error);
        alert('Failed to delete server: ' + error.message);
      }
    };

    return {
      activeTab,
      newServer,
      sshKeys,
      servers,
      addServer,
      deleteServer
    };
  },
};
</script>

<style scoped>
.active {
  background-color: #ddd;
}
</style>
