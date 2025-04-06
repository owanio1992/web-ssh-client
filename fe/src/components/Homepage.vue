<template>
  <div id="homepage">
    <div class="sidebar">
      <!-- Sidebar content -->
      <ul>
        <li><router-link to="/summary">Summary</router-link></li>
        <li><router-link to="/upload">Upload SSH Key</router-link></li>
        <li><router-link to="/servers">Server List</router-link></li>
        <li><router-link to="/permissions">Permission Manage</router-link></li>
        <li><router-link to="/connect">Connect Server</router-link></li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Homepage',
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
}
</style>
