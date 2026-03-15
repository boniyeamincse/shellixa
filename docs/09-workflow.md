# Operational Workflow

Understanding how Shellixa handles a connection from start to finish.

## Step-by-Step Lifecycle

1.  **Application Launch**
    -   User opens Shellixa.
    -   System unlocks the encrypted database (requesting Master Password if enabled).
    -   UI populates the Dashboard with recently accessed hosts.

2.  **Host Selection**
    -   User navigates the Host Manager or uses `Ctrl+P` (Quick Connect).
    -   User clicks "Connect" on a specific host card.

3.  **Authentication Handshake**
    -   Shellixa retrieves the necessary credentials (SSH Key or Password) from the secure vault.
    -   If a key is passphrase-protected, the user is prompted to enter it securely.
    -   The SSH Engine initiates a TCP connection to the remote server.

4.  **Session Establishment**
    -   Server host keys are verified against `known_hosts`.
    -   Authentication is completed; a SSH session channel is opened.
    -   A PTY (Pseudo-Terminal) is requested from the remote host.

5.  **Terminal Interaction**
    -   The Terminal Engine connects the local xterm.js instance to the remote PTY via an IPC stream.
    -   User starts typing; commands are sent in real-time.
    -   Terminal output is rendered instantly with low latency.

6.  **Logging & Teardown**
    -   Shellixa streams session data to the local log file (if enabled).
    -   User closes the tab or types `exit`.
    -   Shellixa gracefully closes the SSH channel and cleans up local resources.
    -   Connection status is updated in the logs.

---

[← UI Pages Guide](08-ui-pages.md) | [Index](README.md) | [Security Overview →](10-security.md)
