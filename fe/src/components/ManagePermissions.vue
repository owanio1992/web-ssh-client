<template>
  <div class="manage-permissions">
    <h1>Manage Permissions</h1>
    <div class="tab-buttons">
      <button :class="{ active: activeTab === 'manage-roles' }" @click="activeTab = 'manage-roles'">Manage Roles</button>
      <button :class="{ active: activeTab === 'manage-permissions' }" @click="activeTab = 'manage-permissions'">Manage Permissions</button>
      <button :class="{ active: activeTab === 'manage-user-roles' }" @click="activeTab = 'manage-user-roles'">Manage User Roles</button>
    </div>

    <div v-if="activeTab === 'manage-roles'" class="manage-roles-tab">
      <h2>Manage Roles</h2>
      <div class="add-role-form">
        <label for="roleName">Role Name:</label>
        <input type="text" id="roleName" v-model="newRoleName" required />
        <button @click="createRole">Create Role</button>
      </div>
      <table>
        <thead>
          <tr>
            <th>Role Name</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="role in roles" :key="role.id">
            <td>{{ role.name }}</td>
            <td>
              <button @click="deleteRole(role)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="activeTab === 'manage-permissions'" class="manage-permissions-tab">
      <h2>Manage Permissions</h2>
      <label for="roleSelect">Select Role:</label>
      <select id="roleSelect" v-model="selectedRole" @change="updateRolePermissions">
        <option v-for="role in roles" :key="role.id" :value="role.id">{{ role.name }}</option>
      </select>

      <table>
        <thead>
          <tr>
            <th>Site Name</th>
            <th>Server Name</th>
            <th>Permission</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="server in servers" :key="server.id">
            <td>{{ server.site_name }}</td>
            <td>{{ server.server_name }}</td>
            <td>
              <input type="checkbox" :id="'permission-' + server.id" :value="server.id" :checked="isServerPermitted(server.id)" @change="updateServerPermissions(server.id)" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="activeTab === 'manage-user-roles'" class="manage-user-roles-tab">
      <h2>Manage User Roles</h2>
      <label for="userSelect">Select User:</label>
      <select id="userSelect" v-model="selectedUser">
        <option v-for="user in users" :key="user.id" :value="user.id">{{ user.username }}</option>
      </select>

      <table>
        <thead>
          <tr>
            <th>Role Name</th>
            <th>User Role</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="role in roles" :key="role.id">
            <td>{{ role.name }}</td>
            <td>
              <input type="checkbox" :id="'user-role-' + role.id" :value="role.id" @change="updateUserRole(role)" />
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

export default {
  components: {
    Notification,
  },
  setup() {
    const activeTab = ref('manage-roles');
    const notificationMessage = ref('');
    const notificationType = ref('success');
    const notificationTrigger = ref(0);
    const roles = ref([]);
    const newRoleName = ref('');
    const servers = ref([]);
    const selectedRole = ref(null);
    const users = ref([]);
    const selectedUser = ref(null);

    const fetchRoles = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${backendUrl}/api/roles/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        roles.value = response.data;
      } catch (error) {
        console.error('Error fetching roles:', error);
        notificationMessage.value = 'Error fetching roles.';
        notificationType.value = 'error';
        notificationTrigger.value++;
      }
    };

    const fetchServers = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${backendUrl}/api/servers/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        servers.value = response.data;
      } catch (error) {
        console.error('Error fetching servers:', error);
        notificationMessage.value = 'Error fetching servers.';
        notificationType.value = 'error';
        notificationTrigger.value++;
      }
    };

    const fetchUsers = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${backendUrl}/api/users/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        users.value = response.data;
      } catch (error) {
        console.error('Error fetching users:', error);
        notificationMessage.value = 'Error fetching users.';
        notificationType.value = 'error';
        notificationTrigger.value++;
      }
    };

    const createRole = async () => {
      try {
        const token = localStorage.getItem('token');
        await axios.post(`${backendUrl}/api/roles/create/`, { name: newRoleName.value }, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        newRoleName.value = '';
        fetchRoles();
        notificationMessage.value = 'Role created successfully.';
        notificationType.value = 'success';
        notificationTrigger.value++;
      } catch (error) {
        console.error('Error creating role:', error);
        notificationMessage.value = 'Error creating role.';
        notificationType.value = 'error';
        notificationTrigger.value++;
      }
    };

    const deleteRole = async (role) => {
      if (confirm(`Are you sure you want to delete the role "${role.name}"?`)) {
        try {
          const token = localStorage.getItem('token');
          await axios.delete(`${backendUrl}/api/roles/${role.id}/delete/`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          fetchRoles();
          notificationMessage.value = 'Role deleted successfully.';
          notificationType.value = 'success';
          notificationTrigger.value++;
        } catch (error) {
          console.error('Error deleting role:', error);
          notificationMessage.value = 'Error deleting role.';
          notificationType.value = 'error';
          notificationTrigger.value++;
        }
      }
    };

    const updateServerPermissions = async (serverId) => {
      if (!selectedRole.value) {
        notificationMessage.value = 'Please select a role.';
        notificationType.value = 'warning';
        notificationTrigger.value++;
        return;
      }

      try {
        const token = localStorage.getItem('token');
        const role = roles.value.find(r => r.id === selectedRole.value);
        const isPermitted = isServerPermitted(serverId);
        let serverIds = [];

        if (role.permissions) {
          serverIds = role.permissions.map(p => p.id);
        }

        if (document.getElementById(`permission-${serverId}`).checked) {
          if (!isPermitted) {
            serverIds.push(serverId);
          }
        } else {
          if (isPermitted) {
            serverIds = serverIds.filter(id => id !== serverId);
          }
        }

        await axios.post(`${backendUrl}/api/roles/${selectedRole.value}/update_permissions/`, {
          server_ids: serverIds,
        }, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        updateRolePermissions();
        notificationMessage.value = 'Permissions updated successfully.';
        notificationType.value = 'success';
        notificationTrigger.value++;
      } catch (error) {
        console.error('Error updating permission:', error);
        notificationMessage.value = 'Error updating permission.';
        notificationType.value = 'error';
        notificationTrigger.value++;
      }
    };

    const updateUserRole = async (role) => {
      if (!selectedUser.value) {
        notificationMessage.value = 'Please select a user.';
        notificationType.value = 'warning';
        notificationTrigger.value++;
        return;
      }

      try {
        const token = localStorage.getItem('token');
        // Check if user role exists
        const userRoleExists = await axios.get(`${backendUrl}/api/user-roles/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          params: {
            user_id: selectedUser.value,
            role_id: role.id,
          },
        });

        if (userRoleExists.data.length > 0) {
          // Remove user from role
          await axios.delete(`${backendUrl}/api/user-roles/${userRoleExists.data[0].id}/delete/`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          notificationMessage.value = 'User removed from role successfully.';
          notificationType.value = 'success';
          notificationTrigger.value++;
        } else {
          // Add user to role
          await axios.post(`${backendUrl}/api/user-roles/add/`, {
            user_id: selectedUser.value,
            role_id: role.id,
          }, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          notificationMessage.value = 'User added to role successfully.';
          notificationType.value = 'success';
          notificationTrigger.value++;
        }
      } catch (error) {
        console.error('Error updating user role:', error);
        notificationMessage.value = 'Error updating user role.';
        notificationType.value = 'error';
        notificationTrigger.value++;
      }
    };

    const isServerPermitted = (serverId) => {
      if (!selectedRole.value) return false;
      const role = roles.value.find(r => r.id === selectedRole.value);
      if (!role || !role.permissions) return false;
      return role.permissions.some(p => p.id === serverId);
    };

    const updateRolePermissions = () => {
      if (selectedRole.value) {
        const role = roles.value.find(r => r.id === selectedRole.value);
        if (role && role.permissions) {
          servers.value.forEach(server => {
            const checkbox = document.getElementById(`permission-${server.id}`);
            if (checkbox) {
              checkbox.checked = role.permissions.some(p => p.id === server.id);
            }
          });
        } else {
          servers.value.forEach(server => {
            const checkbox = document.getElementById(`permission-${server.id}`);
            if (checkbox) {
              checkbox.checked = false;
            }
          });
        }
      }
    };

    onMounted(() => {
      fetchRoles();
      fetchServers();
      fetchUsers();
    });

    return {
      activeTab,
      notificationMessage,
      notificationType,
      notificationTrigger,
      roles,
      newRoleName,
      fetchRoles,
      createRole,
      deleteRole,
      servers,
      selectedRole,
      updateUserRole,
      users,
      selectedUser,
      isServerPermitted,
      updateServerPermissions,
      updateRolePermissions,
    };
  },
};
</script>

<style scoped>
.manage-permissions {
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

.add-role-form {
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

select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}
</style>
