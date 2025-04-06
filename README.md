# describe
This is a web SSH client project that helps users quickly connect to servers via the SSH protocol. Users can select a server from a list, and the system will provide a web SSH console to connect to the client without additional configuration.

## Authentication

This project now includes authentication to protect the homepage. Only logged-in users can access the homepage.

### Session Management

-   Upon successful login, a session token and expiry time are stored in `localStorage`.
-   The session expiry time is configurable in `fe/src/config.js` (default: 30 minutes).
-   If the session token is missing or expired, the user is redirected to the login page.
