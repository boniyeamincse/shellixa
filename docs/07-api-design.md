# API Design (Internal)

In the Python implementation, "API" refers to the internal method interfaces between the GUI layer and the Backend/Logic modules.

## Host Management APIs

### `GET /hosts`
Loads the list of all saved hosts.
-   **Response**: Array of Host objects with nested metadata.

### `POST /hosts`
Saves a new host or updates an existing one.
-   **Payload**: `Host` object.
-   **Response**: `200 OK` with the saved host ID.

### `DELETE /hosts/:id`
Deletes a host and its associated session history.

## Connection APIs

### `POST /connect`
Initiates an SSH connection.
-   **Payload**: `{ hostId: string, options: ConnectionOptions }`.
-   **Action**: Backend spawns a new SSH channel and returns a unique `sessionId`.

### `POST /session/:id/input`
Sends terminal input (keystrokes) to the remote server.
-   **Payload**: `{ data: string }`.

### `GET /session/:id/output` (WebSocket/Event)
Broadcasts terminal output from the backend to the frontend terminal engine.

## SSH Key Management APIs

### `POST /keys/import`
Reads a local SSH key file and prepares it for encryption.
-   **Payload**: `{ path: string, passphrase?: string }`.

### `GET /keys`
Lists all references to managed SSH keys.

## Settings APIs

### `PATCH /settings`
Updates application global preferences.
-   **Payload**: `{ theme: 'dark' | 'light', fontSize: number, ... }`.

---

[← Database Design](06-database-design.md) | [Index](README.md) | [UI Pages Guide →](08-ui-pages.md)
