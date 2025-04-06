<template>
  <div class="upload-ssh-key">
    <h1>Upload SSH Key</h1>
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
</template>

<script>
import { backendUrl } from '../config.js';

export default {
  data() {
    return {
      keyName: '',
      sshKey: ''
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
          alert('SSH Key uploaded successfully!');
          this.keyName = '';
          this.sshKey = '';
        } else {
          const errorData = await response.json();
          alert(`Error uploading SSH Key: ${errorData.message || response.statusText}`);
        }
      } catch (error) {
        alert(`Error uploading SSH Key: ${error.message}`);
      }
    }
  }
};
</script>

<style scoped>
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

button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #3e8e41;
}
</style>
