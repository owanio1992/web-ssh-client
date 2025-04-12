<template>
  <div id="homepage" v-if="user">
    <aside class="sidebar">
      <ul>
        <li><a href="#" @click.prevent="selectPage('SummaryPage')">Summary</a></li>
        <li v-if="isAdmin"><a href="#" @click.prevent="selectPage('ManageSSHKeys')">Manage SSH Keys</a></li>
        <li v-if="isAdmin"><a href="#" @click.prevent="selectPage('ManageServers')">Manage Servers</a></li>
        <li v-if="isAdmin"><a href="#" @click.prevent="selectPage('ManagePermissions')">Permission Manage</a></li>
        <li><a href="#" @click.prevent="selectPage('ConnectServerPage')">Connect Server</a></li>
        <li><a href="#" @click.prevent="logout">Logout</a></li>
      </ul>
      <div class="session-expiry">
        Session expires in: {{ remainingTime }}
      </div>
    </aside>
    <main class="content">
      <component :is="selectedPage"></component>
    </main>
  </div>
  <div v-else>Loading...</div>
</template>



<script>
import SummaryPage from './SummaryPage.vue';
import ManageSSHKeys from './ManageSSHKeys.vue';
import ManageServers from './ManageServers.vue';
import ManagePermissions from './ManagePermissions.vue';
import ConnectServerPage from './ConnectServerPage.vue';
import { backendUrl } from '../config.js';

export default {
  name: 'Homepage',
  components: {
    SummaryPage,
    ManageSSHKeys,
    ManageServers,
    ManagePermissions,
    ConnectServerPage
  },
  data() {
    return {
      selectedPage: 'SummaryPage',
      isAdmin: false,
      remainingTime: '',
      user: null
    }
  },
  mounted() {
    this.checkSessionValidity();
    this.updateRemainingTime();
    this.intervalId = setInterval(this.updateRemainingTime, 1000);
  },
  beforeUnmount() {
    clearInterval(this.intervalId);
  },
  methods: {
    selectPage(pageName) {
      this.checkSessionValidity();
      this.selectedPage = pageName;
    },
    checkSessionValidity() {
      fetch(backendUrl + '/api/user/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Session invalid');
          }
          return response.json();
        })
        .then(data => {
          this.user = data;
          if (data.groups && data.groups.length > 0) {
            this.isAdmin = data.groups.some(group => group.name === 'admin');
          } else {
            this.isAdmin = false;
          }
          console.log('Session is valid');
          this.renewSession();
        })
        .catch(error => {
          console.error('Session invalid:', error);
          // Redirect to login page
          window.location.href = '/login'; // TODO: Replace with actual login page URL
        });
    },
    renewSession() {
      fetch(backendUrl + '/api/token/refresh/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: localStorage.getItem('refresh_token') }),
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to renew session');
          }
          return response.json();
        })
        .then(data => {
          localStorage.setItem('token', data.access); // Store new access token
          const expiry = new Date().getTime() + 30 * 60 * 1000; // Calculate new expiry time
          localStorage.setItem('expiry', expiry.toString());
          console.log('Session renewed');
        })
        .catch(error => {
          console.error('Failed to renew session:', error);
          // Redirect to login page if renewal fails
          window.location.href = '/login'; // TODO: Replace with actual login page URL
        });
    },
    logout() {
      if (confirm('Are you sure you want to logout?')) {
        localStorage.removeItem('token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('expiry');
        window.location.href = '/login'; // Redirect to login page
      }
    },
    updateRemainingTime() {
      const expiry = localStorage.getItem('expiry');
      if (expiry) {
        const remaining = parseInt(expiry) - new Date().getTime();
        if (remaining > 0) {
          const minutes = Math.floor((remaining % (1000 * 60 * 60)) / (1000 * 60));
          const seconds = Math.floor((remaining % (1000 * 60)) / 1000);
          this.remainingTime = `${minutes}m ${seconds}s`;
        } else {
          this.remainingTime = 'Session expired';
          clearInterval(this.intervalId);
          window.location.href = '/login';
        }
      } else {
        this.remainingTime = 'No session';
      }
    }
  }
}
</script>

<style scoped>
#homepage {
  display: flex;
  height: 100vh;
}

.session-expiry {
  padding: 10px 15px;
  text-align: center;
  color: #cbd5e1;
  font-size: 0.8em;
  position: absolute;
  bottom: 0;
  width: 100%;
}

#homepage {
  display: flex;
  height: 100vh;
  margin: 0;
}

.sidebar {
  width: 220px;
  background-color: #1e293b;
  color: #fff;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
}

.sidebar > * {
  padding: 20px;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
  flex-grow: 1;
}

.sidebar li {
  margin-bottom: 15px;
}

.sidebar a {
  color: #cbd5e1;
  text-decoration: none;
  display: block;
  padding: 10px 15px;
  border-radius: 5px;
  transition: background-color 0.2s ease;
}

.sidebar a:hover {
  background-color: #334155;
}

.content {
  flex: 1;
  padding: 20px;
  overflow: auto;
  margin-left: 220px; /* Adjust content margin when sidebar is open */
  transition: margin-left 0.3s ease;
  min-width: 800px; /* Added min-width */
}
</style>
