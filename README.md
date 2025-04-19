# Web SSH Client

This project is a web-based SSH client that allows users to connect to servers via the SSH protocol through a web browser. It provides a convenient way to manage servers and user permissions without requiring additional client-side configuration.

## Features

-   **Authentication:** Secure user login.
-   **Manage Accounts (Admin Only):** Create and manage user accounts via the Django admin interface.
-   **Manage SSH Keys (Admin Only):** Add, view, and remove SSH keys used for server connections.
-   **Manage Servers (Admin Only):** Configure server details including site, server name, user, host, and associated SSH keys.
-   **Manage Permissions (Admin Only):** Implement Role-Based Access Control (RBAC) to manage which users have access to which servers.
-   **Connect to Server:** Users can select from a list of servers they have permission to access and open a web-based terminal session.

## User Guide

### Authentication

Users cannot self-register. An administrator must create your account. Once your account is created, you can log in using the login page provided by the frontend.

### Manage Accounts (Admin Only)

User accounts are managed through the Django administration interface.

1.  **Access Admin:** Navigate to `<your-frontend-host>/admin/` in your web browser.
2.  **Login:** Log in using an administrator account.
3.  **Create User:** Go to the "Users" section and click "Add user". Fill in the required details (username, password, etc.). It is recommended to also fill in the "First name" and "Last name" fields for better identification.
4.  **Create Admin Account:** To make a user an administrator, add them to the "admin" group in the Django admin. If the "admin" group does not exist, you may need to create it first in the "Groups" section.
5.  **Manage Existing Users:** From the "Users" list, you can click on a user to edit their details, change their password, or manage their group memberships (including adding/removing them from the "admin" group).

### Manage SSH Keys (Admin Only)

This feature allows administrators to manage the SSH keys used by the system to connect to servers.

1.  Navigate to the "Manage SSH Keys" section in the web interface (accessible after logging in as an admin).
2.  Here you can add new SSH keys (likely by pasting the private key content and giving it a name) or delete existing ones. These keys are stored securely on the backend.

### Manage Servers (Admin Only)

Administrators can define the servers that users can connect to.

1.  Navigate to the "Manage Servers" section in the web interface (accessible after logging in as an admin).
2.  You can add new server configurations, specifying:
    *   **Site:** A grouping for servers (must be unique).
    *   **Server Name:** The name of the server within a site (must be unique within that site, but can be duplicated across different sites).
    *   **User:** The username to use for the SSH connection on the remote server.
    *   **Host:** The hostname or IP address of the remote server.
    *   **SSH Key Name:** Select an SSH key that has been previously added in the "Manage SSH Keys" section.
3.  You can also edit or delete existing server configurations from the list.

### Manage Permissions (Admin Only)

This section implements Role-Based Access Control (RBAC).

1.  Navigate to the "Manage Permissions" section in the web interface (accessible after logging in as an admin).
2.  **Manage Roles:**
    *   Create new roles by entering a role name and clicking "Create Role".
    *   Delete existing roles from the list.
3.  **Manage Permissions:**
    *   Select a role from the dropdown list.
    *   A list of servers will be displayed. Check the boxes next to the servers that the selected role should have permission to connect to.
    *   Click "Update Permissions" to save the changes for the selected role.
4.  **Manage User Roles:**
    *   Select a user from the dropdown list.
    *   A list of roles will be displayed. Check the boxes next to the roles that the selected user should be assigned to.
    *   Click "Update Roles" to save the role assignments for the selected user.

### Connect to Server

Users can connect to servers they have been granted permission to access.

1.  Navigate to the "Connect Server" section in the web interface.
2.  You will see a list of "Sites" and "Server Names".
3.  Select a Site from the first list. The second list will update to show the servers available within that site that you have permission to access.
4.  Select a Server Name from the second list.
5.  Click the "Connect" button.
6.  The system will check your permissions. If you have permission, a new browser tab will open with a web-based terminal console connected to the selected server. The tab title will be in the format "<Site>-<Server Name>". The console should automatically log you in to the server using the configured SSH key.