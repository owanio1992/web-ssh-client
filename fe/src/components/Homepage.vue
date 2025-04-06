<template>
  <div id="homepage">
    <aside class="sidebar">
      <ul>
        <li><a href="#" @click.prevent="selectPage('SummaryPage')">Summary</a></li>
        <li v-if="isAdmin"><a href="#" @click.prevent="selectPage('UploadSSHKey')">Upload SSH Key</a></li>
        <li v-if="isAdmin"><a href="#" @click.prevent="selectPage('ManageSSHKeys')">Manage SSH Keys</a></li>
        <li><a href="#" @click.prevent="selectPage('ServerListPage')">Server List</a></li>
        <li><a href="#" @click.prevent="selectPage('PermissionManagePage')">Permission Manage</a></li>
        <li><a href="#" @click.prevent="selectPage('ConnectServerPage')">Connect Server</a></li>
      </ul>
    </aside>
    <main class="content">
      <component :is="selectedPage"></component>
    </main>
  </div>
</template>

<script>
import SummaryPage from './SummaryPage.vue';
import UploadSSHKey from './UploadSSHKey.vue';
import ManageSSHKeys from './ManageSSHKeys.vue';

export default {
  name: 'Homepage',
  components: {
    SummaryPage,
    UploadSSHKey,
    ManageSSHKeys,
    ServerListPage: { template: '<div>Server List Page</div>' },
    PermissionManagePage: { template: '<div>Permission Manage Page</div>' },
    ConnectServerPage: { template: '<div>Connect Server Page</div>' }
  },
  data() {
    return {
      selectedPage: 'SummaryPage',
      isAdmin: true // TODO: Replace with actual admin check
    }
  },
  methods: {
    selectPage(pageName) {
      this.selectedPage = pageName;
    }
  },
  watch: {
    selectedPage(newPage) {
      if (newPage === 'UploadSSHKey') {
        this.selectedPage = 'UploadSSHKey';
      }
    }
  }
}
</script>

<style scoped>
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
