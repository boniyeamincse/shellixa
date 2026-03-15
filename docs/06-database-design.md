# Database Design

Shellixa uses a local, encrypted database to store your sensitive information. This ensures that your host configurations and credentials stay private even if your device is compromised.

## Storage Strategy
-   **Engine**: SQLite (via SQLCipher) or Encrypted JSON documents.
-   **Security**: All sensitive fields (passwords, private key content) are encrypted using **AES-256-GCM**.
-   **Location**: `~/.config/shellixa/data.db` (Linux).

## Example Schema

### `hosts` Table
Stores information about remote servers.
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID | Primary Key |
| `name` | String | User-defined label |
| `hostname` | String | IP address or domain |
| `port` | Integer | SSH port (default 22) |
| `username` | String | SSH username |
| `group_id` | UUID | Foreign Key to `groups` |
| `auth_id` | UUID | Foreign Key to `authentications` |

### `groups` Table
Organizes hosts into folders.
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID | Primary Key |
| `name` | String | Group name |
| `parent_id`| UUID | For nested groups |
| `icon` | String | Icon identifier |

### `authentications` Table
Stores credentials.
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID | Primary Key |
| `type` | Enum | `password`, `private_key`, `agent` |
| `secret` | Blob | **Encrypted** password or key content |
| `key_path` | String | Path to key file (if not stored in DB) |

### `settings` Table
Key-value store for application preferences.
| Column | Type | Description |
| :--- | :--- | :--- |
| `key` | String | Unique setting name |
| `value` | JSON | Serialized setting value |

### `logs` Table
Activity and session logs.
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID | Primary Key |
| `host_id` | UUID | Link to host |
| `timestamp`| DateTime | Event time |
| `event` | String | Description (e.g., "Connected", "Failed") |

---

[← System Architecture](05-system-architecture.md) | [Index](README.md) | [API Design →](07-api-design.md)
