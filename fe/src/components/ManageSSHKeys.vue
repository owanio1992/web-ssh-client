<template>
  <div class="manage-ssh-keys">
    <h1>Manage SSH Keys</h1>
    <div class="tab-buttons">
      <button :class="{ active: activeTab === 'add' }" @click="activeTab = 'add'">Add SSH Key</button>
      <button :class="{ active: activeTab === 'delete' }" @click="activeTab = 'delete'">Delete SSH Key</button>
    </div>

    <div v-if="activeTab === 'add'" class="upload-ssh-key">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="keyName">Key Name:</label>
          <input type="text" id="keyName" v-model="keyName" required>
        </div>
        <div class="form-group">
          <label for="sshKey">SSH Key:</label>
          <textarea id="sshKey" v-model="sshKey" required></textarea>
        </div>
        <button type="submit">Upload</button>
      </form>
    </div>

    <div v-if="activeTab === 'delete'">
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
    <Notification
      :message="notificationMessage"
      :type="notificationType"
      :trigger="notificationTrigger"
    />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { backendUrl } from '../config.js';
import axios from 'axios';
import Notification from './Notification.vue'; // Import Notification component

export default {
  components: { // Register Notification component
    Notification,
  },
  data() {
    return {
      activeTab: 'add',
      keyName: '',
      sshKey: ''
    };
  },
  setup() {
    const sshKeys = ref([]);
    const searchQuery = ref('');
    const notificationMessage = ref('');
    const notificationType = ref('success');
    const notificationTrigger = ref(0);

    const fetchKeys = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${backendUrl}/api/ssh-keys/`, {
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
      if (confirm(`Are you sure you want to delete the SSH key "${key.name}"?`)) {
        try {
          const token = localStorage.getItem('token');
          await axios.delete(`${backendUrl}/api/ssh-keys/${key.id}/delete/`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          console.log('SSH key deleted successfully.');
          // Refresh the key list
          fetchKeys();
          // Show success notification
          notificationMessage.value = 'SSH key deleted successfully!';
          notificationType.value = 'success';
          notificationTrigger.value++;
        } catch (error) {
          console.error('Error deleting SSH key:', error);
          // Show error notification
          notificationMessage.value = 'Error deleting SSH key.';
          notificationType.value = 'error';
          notificationTrigger.value++;
        }
      }
    };

    return {
      sshKeys,
      searchQuery,
      filteredKeys,
      deleteKey,
      fetchKeys,
      notificationMessage,
      notificationType,
      notificationTrigger,
    };
  },
  methods: {
    async handleSubmit() {
      try {
        const response = await fetch(`${backendUrl}/api/ssh-key/upload/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({
            name: this.keyName,
            key_content: this.sshKey
          })
        });

        if (response.ok) {
          // alert('SSH Key uploaded successfully!');
          this.keyName = '';
          this.sshKey = '';
          // Show success notification
          this.notificationMessage = 'SSH Key uploaded successfully!';
          this.notificationType = 'success';
          this.notificationTrigger++;
        } else {
          const errorData = await response.json();
          // alert(`Error uploading SSH Key: ${errorData.message || response.statusText}`);
          // Show error notification
          this.notificationMessage = `Error uploading SSH Key: ${errorData.error || response.statusText}`;
          this.notificationType = 'error';
          this.notificationTrigger++;
        }
      } catch (error) {
        // alert(`Error uploading SSH Key: ${error.message}`);
        // Show error notification
        this.notificationMessage = `Error uploading SSH Key: ${error.message}`;
        this.notificationType = 'error';
        this.notificationTrigger++;
      }
    }
  },
  watch: {
    activeTab(newTab) {
      if (newTab === 'delete') {
        this.fetchKeys();
      }
    }
  }
};
</script>

<style scoped>
.manage-ssh-keys {
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

.upload-ssh-key {
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
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

textarea {
  width: 100%;
  height: 300px; /* Increased height */
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.upload-ssh-key button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.upload-ssh-key button:hover {
  background-color: #3e8e41;
}
</style>
