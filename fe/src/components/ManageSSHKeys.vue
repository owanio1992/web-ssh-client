<template>
  <div class="manage-ssh-keys">
    <h1>Manage SSH Keys</h1>
    <input type="text" v-model="searchQuery" placeholder="Search SSH Keys" />
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Key</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="key in filteredKeys" :key="key.id">
          <td>{{ key.name }}</td>
          <td>{{ key.key.substring(0, 20) }}***</td>
          <td>
            <button @click="deleteKey(key)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { backendUrl as config } from '../config';
import axios from 'axios';

export default {
  setup() {
    const sshKeys = ref([]);
    const searchQuery = ref('');

    const fetchKeys = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${config}/api/ssh-keys/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        sshKeys.value = response.data;
      } catch (error) {
        console.error('Error fetching SSH keys:', error);
      }
    };

    onMounted(() => {
      fetchKeys();
    });

    const filteredKeys = computed(() => {
      return sshKeys.value.filter((key) =>
        key.name.toLowerCase().includes(searchQuery.value.toLowerCase())
      );
    });

    const deleteKey = async (key) => {
      try {
        const token = localStorage.getItem('token');
        await axios.delete(`${config}/api/ssh-keys/${key.id}/delete/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        console.log('SSH key deleted successfully.');
        // Refresh the key list
        fetchKeys();
      } catch (error) {
        console.error('Error deleting SSH key:', error);
      }
    };

    return {
      sshKeys,
      searchQuery,
      filteredKeys,
      deleteKey,
    };
  },
};
</script>

<style scoped>
.manage-ssh-keys {
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 8px;
  border: 1px solid #ddd;
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
</style>
