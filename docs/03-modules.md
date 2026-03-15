# System Modules

Shellixa is built using a modular architecture to ensure scalability, ease of maintenance, and robust performance. Below are the core modules that power the application.

## 🔗 Connection Manager
The heart of the application. It handles the lifecycle of all SSH connections.
-   **Responsibilities**: Managing active sessions, heartbeat/keep-alive logic, and reconnection strategies.
-   **State**: Tracks which hosts are currently connected and their resource usage.

## 💻 Terminal Engine
Based on `xterm.js`, this module handles the rendering of the terminal interface.
-   **Responsibilities**: Rendering text, handling input/output buffers, ANSI color parsing, and scrollback management.
-   **Customization**: Manages terminal themes and font scaling.

## 🛡️ SSH Engine
The low-level communication layer using the **Paramiko** library.
-   **Responsibilities**: Performing SSH-2 handshakes, handling SFTP operations, and managing SSH channels and tunnels.
-   **Performance**: Lightweight and Pythonic, optimized for quick session initialization.

## 🔐 Authentication Manager
Manages user credentials and security tokens.
-   **Responsibilities**: Securely retrieving keys from the vault, interacting with system keyrings (like Secret Service or KWallet), and handling password prompts.

## ⚙️ Settings Manager
Handles application-wide and per-host configurations.
-   **Responsibilities**: Loading/saving JSON configuration files, handling default overrides, and managing UI state persistence.

## 🎨 UI Layer
The frontend component (built with a modern framework like React, Vue, or Svelte).
-   **Responsibilities**: Orchestrating the Dashboard, Terminal views, and configuration forms.
-   **Interactions**: Uses an IPC (Inter-Process Communication) bridge to talk to the backend modules.

## 🧠 Helium AI Engine
The intelligence layer of Shellixa.
-   **Responsibilities**: Providing real-time command autocomplete, parsing natural language queries via "Gloria", and managing command snippets.
-   **Security**: Ensures AI processing remains private or uses secure API bridges.

## ☁️ Sync & Vault Engine
Handles cross-device data persistence.
-   **Responsibilities**: Managing the End-to-End Encrypted (E2EE) data vault, conflict resolution during sync, and integration with the cloud backend.

## 📝 Logging System
Captures application events and terminal output.
-   **Responsibilities**: Writing structured logs for debugging and raw session logs for user auditing.
-   **Compliance**: Ensures logs are stored securely and can be rotated to save space.

---

[← Key Features](02-features.md) | [Index](README.md) | [User Roles →](04-user-roles.md)
