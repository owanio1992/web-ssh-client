# describe
This is a web SSH client project that helps users quickly connect to servers via the SSH protocol. Users can select a server from a list, and the system will provide a web SSH console to connect to the client without additional configuration.

## Authentication

This project now includes authentication to protect the homepage. Only logged-in users can access the homepage.

### Session Management

-   Upon successful login, a session token and expiry time are stored in `localStorage`.
-   The session expiry time is configurable in `fe/src/config.js` (default: 30 minutes).
-   If the session token is missing or expired, the user is redirected to the login page.



## Features

### Connect Server
- Allows authenticated users to select a pre-configured server (by site and server name).
- Upon selection and connection request, the system verifies user permissions for the selected server.
- If permitted, a new browser tab opens with a web-based terminal connected to the server via SSH, using the associated SSH key stored securely on the backend.
- The connection is established using WebSockets for real-time communication between the browser terminal and the backend SSH session handler.

### User Setup
- Users must have a First Name and Last Name configured.
- Users can be assigned to groups (e.g., 'admin', 'user') for permission management (details TBD).