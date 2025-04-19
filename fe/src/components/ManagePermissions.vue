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
        <button @click="createRole" :disabled="!newRoleName">Create Role</button>
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
      <v-select
        id="roleSelect"
        :options="roles"
        label="name"
        :reduce="role => role.id"
        v-model="selectedRole"
        placeholder="Search and select a role..."
      ></v-select>
      <!-- Note: The @change="updateRolePermissions" is handled automatically by v-model binding with the computed property -->

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
              <input type="checkbox" :id="'permission-' + server.id" :value="server.id" :checked="isServerPermitted(server.id)" :disabled="!selectedRole" />
            </td>
          </tr>
        </tbody>
      </table>
      <button @click="updateServerPermissions" :disabled="!selectedRole">Update Permissions</button>
    </div>

    <div v-if="activeTab === 'manage-user-roles'" class="manage-user-roles-tab">
      <h2>Manage User Roles</h2>
      <label for="userSelect">Select User:</label>
      <v-select
        id="userSelect"
        :options="users"
        label="username"
        :reduce="user => user.id"
        v-model="selectedUser"
        placeholder="Search and select a user..."
      ></v-select>

      <table>
        <thead>
          <tr>
            <th>Role Name</th>
            <th>Assigned</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="role in roles" :key="role.id">
            <td>{{ role.name }}</td>
            <td>
              <input
                type="checkbox"
                :id="'user-role-' + role.id"
                :value="role.id"
                :checked="isRoleAssignedToUser(role.id)"
                @change="toggleRoleSelection(role.id, $event.target.checked)"
                :disabled="!selectedUser"
              />
            </td>
          </tr>
        </tbody>
      </table>
      <button @click="saveUserRoles" :disabled="!selectedUser">Update Roles</button>
    </div>
    <Notification
      :message="notificationMessage"
      :type="notificationType"
      :trigger="notificationTrigger"
    />
  </div>
</template>

<script>
import { ref, onMounted, computed, watch } from 'vue';
import axios from 'axios';
import vSelect from 'vue-select'; // Import vue-select
import 'vue-select/dist/vue-select.css'; // Import vue-select CSS
import { backendUrl } from '../config.js';
import Notification from './Notification.vue';

export default {
  components: {
    vSelect, // Register vue-select component
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
    const _selectedRole = ref(null); // Keep this as is, only changing _selectedUser
    const selectedRole = computed({
      get: () => _selectedRole.value,
      set: (value) => {
        _selectedRole.value = value;
        updateRolePermissions();
      }
    });
    const users = ref([]);
    const selectedUserRef = ref(null); // Renamed internal ref
    const selectedUserRoles = ref(new Set());
    const originalUserRoles = ref(new Set()); // To track original state if needed

    // --- New function to fetch roles for a specific user ---
    const fetchUserRoles = async (userId) => {
      if (!userId) {
        selectedUserRoles.value.clear();
        originalUserRoles.value.clear();
        return;
      }
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${backendUrl}/api/users/${userId}/roles/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        selectedUserRoles.value = new Set(response.data.map(role => role.id));
        originalUserRoles.value = new Set(response.data.map(role => role.id)); // Store original state
      } catch (error) {
        console.error('Error fetching user roles:', error);
        notificationMessage.value = 'Error fetching user roles.';
        notificationType.value = 'error';
        notificationTrigger.value++;
        selectedUserRoles.value.clear();
        originalUserRoles.value.clear();
      }
    };

    // --- Watcher for selectedUser ---
    const selectedUser = computed({ // This computed property is used by v-model in the template
        get: () => selectedUserRef.value,
        set: (value) => {
            selectedUserRef.value = value;
        }
    });

    watch(selectedUserRef, (newUserId) => { // Watch the internal ref
        fetchUserRoles(newUserId);
    });
    // --- End Watcher ---


    const fetchRoles = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${backendUrl}/api/roles/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const allRoles = response.data;

        roles.value = allRoles;
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
        selectedRole.value = null; // Clear selected role after creating a new role
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

    const updateServerPermissions = async () => {
      if (!selectedRole.value) {
        notificationMessage.value = 'Please select a role.';
        notificationType.value = 'warning';
        notificationTrigger.value++;
        return;
      }

      try {
        const token = localStorage.getItem('token');
        const serverIds = servers.value
          .filter(server => document.getElementById(`permission-${server.id}`).checked)
          .map(server => server.id);

        await axios.post(`${backendUrl}/api/roles/${selectedRole.value}/update_permissions/`, {
          server_ids: serverIds,
        }, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        fetchRoles();
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

    // --- New function to handle checkbox changes ---
    const toggleRoleSelection = (roleId, isChecked) => {
      if (isChecked) {
        selectedUserRoles.value.add(roleId);
      } else {
        selectedUserRoles.value.delete(roleId);
      }
    };

    // --- New function to save user roles ---
    const saveUserRoles = async () => {
      if (!selectedUserRef.value) { // Use the ref's value
        notificationMessage.value = 'Please select a user.';
        notificationType.value = 'warning';
        notificationTrigger.value++;
        return;
      }

      try {
        const token = localStorage.getItem('token');
        const roleIdsArray = Array.from(selectedUserRoles.value).map(roleId => roleId);
        await axios.post(`${backendUrl}/api/users/${selectedUserRef.value}/update_roles/`, // Use the ref's value
          { role_ids: roleIdsArray },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        originalUserRoles.value = new Set(selectedUserRoles.value); // Update original state on success
        notificationMessage.value = 'User roles updated successfully.';
        notificationType.value = 'success';
        notificationTrigger.value++;
      } catch (error) {
        console.error('Error updating user roles:', error);
        notificationMessage.value = `Error updating user roles: ${error.response?.data?.error || error.message}`;
        notificationType.value = 'error';
        notificationTrigger.value++;
        // Optionally revert changes on error:
        // selectedUserRoles.value = new Set(originalUserRoles.value);
      }
    };


    const isServerPermitted = (serverId) => {
      if (!selectedRole.value) return false;
      const role = roles.value.find(r => r.id === selectedRole.value);
      if (!role || !role.permissions) return false;
      return role.permissions?.some(p => p.id === Number(serverId));
    };

   const updateRolePermissions = async () => {
      if (selectedRole.value) {
        try {
          const token = localStorage.getItem('token');
          const response = await axios.get(`${backendUrl}/api/roles/${selectedRole.value}/`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          const role = response.data;

          if (role) {
            servers.value.forEach(server => {
              const checkbox = document.getElementById(`permission-${server.id}`);
              if (checkbox) {
                checkbox.checked = role.permissions?.some(p => p.id === server.id) || false;
              }
            });
          }
        } catch (error) {
          console.error('Error fetching roles:', error);
          notificationMessage.value = 'Error fetching roles.';
          notificationType.value = 'error';
          notificationTrigger.value++;
        }
      }
    };

   const isRoleAssignedToUser = (roleId) => {
     const hasRole = selectedUserRoles.value.has(roleId);
     return hasRole;
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
      users,
      selectedUser, // Keep the computed property for the template v-model
      // _selectedUser, // REMOVED from return statement
      selectedUserRoles,
      fetchUserRoles, // Expose if needed, though watcher handles it
      toggleRoleSelection,
      saveUserRoles,
      isServerPermitted,
      updateServerPermissions,
      updateRolePermissions,
      isRoleAssignedToUser,
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
