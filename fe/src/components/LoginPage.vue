<template>
  <div class="login-page">
    <div class="logo">web ssh client</div>
    <h1>Login</h1>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <button type="submit">Login</button>
    </form>
    <div id="success-message" v-if="successMessage">{{ successMessage }}</div>
    <div id="fail-message" v-if="failMessage">{{ failMessage }}</div>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { backendUrl, sessionExpiryTime } from '../config';

export default {
  setup() {
    const username = ref('');
    const password = ref('');
    const router = useRouter();
    const successMessage = ref('');
    const failMessage = ref('');

    const login = async () => {
      try {
        const response = await axios.post(backendUrl + '/api/token/', {
          username: username.value,
          password: password.value
        });

        if (response.status === 200) {
          // Login successful
          successMessage.value = 'Login successful!';
          failMessage.value = '';

          // Store the token and expiry time in local storage
          const token = response.data.access;
          const refresh = response.data.refresh;
          const expiry = new Date().getTime() + sessionExpiryTime * 60 * 1000; // Calculate expiry time

          localStorage.setItem('token', token);
          localStorage.setItem('refresh_token', refresh);
          localStorage.setItem('expiry', expiry.toString());

          // Redirect to home page
          router.push('/homepage');
        }
         else {
          // Login failed
          console.error('Login failed', response.data);
          successMessage.value = '';
          failMessage.value = 'Login fail!';
        }
      }
       catch (error) {
        console.error('Error during login:', error);
        successMessage.value = '';
        failMessage.value = 'Login fail!';
      }
    };

    return {
      username,
      password,
      login,
      successMessage,
      failMessage
    };
  }
}
</script>

<style scoped>
.login-page {
  width: 400px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center; /* Center the content */
}

.logo {
  font-size: 2em; /* Adjust size as needed */
  margin-bottom: 20px; /* Space below the logo */
  color: #333; /* Adjust color as needed */
}

.form-group {
  margin-bottom: 10px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

#success-message {
  color: green;
  margin-top: 10px;
}

#fail-message {
  color: red;
  margin-top: 10px;
}

button:hover {
  background-color: #3e8e41;
}
</style>
