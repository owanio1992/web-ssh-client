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
export default {
  data() {
    return {
      keyName: '',
      sshKey: ''
    };
  },
  methods: {
    handleSubmit() {
      // TODO: Implement upload logic
      console.log('Key Name:', this.keyName);
      console.log('SSH Key:', this.sshKey);
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
  height: 150px; /* Increased height */
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
