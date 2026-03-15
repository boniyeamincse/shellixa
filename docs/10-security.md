# Security Overview

Security is the foundational pillar of Shellixa. We implement industry-standard best practices to ensure your remote access is never compromised.

## 🔒 End-to-End Encrypted (E2EE) Vault
Your data is encrypted before it ever leaves your machine.
-   **Architecture**: Zero-knowledge sync ensures that even the sync servers cannot read your host lists or credentials.
-   **Encryption**: AES-256-GCM with keys periodically rotated.

## 🔑 Keychain & Advanced Auth
Centralized management for all your digital identities.
-   **Biometrics**: Support for Fingerprint/FaceID via system APIs (SSH.id).
-   **Hardware Keys**: Full support for **FIDO2** (YubiKey) tokens.
-   **SSH Certificates**: Infrastructure-ready authentication for enterprise environments.

## 🛑 Host Verification
To prevent Man-in-the-Middle (MitM) attacks:
-   Shellixa maintains its own `known_hosts` file or integrates with the system one.
-   If a host key changes, Shellixa will block the connection and alert the user with a critical warning.

## 🛡️ Secure Configuration
-   **No Telemetry**: By default, Shellixa does not send any usage data or session details to external servers.
-   **Process Isolation**: Terminal sessions run in separate execution contexts to prevent memory leaks or cross-session data bleeding.
-   **Minimal Dependencies**: We audit our dependencies regularly to minimize the attack surface.

## 🛠️ Best Practices
1.  **Use a Master Password**: Always enable this feature to encrypt your local database.
2.  **Use Ed25519 Keys**: These provide the best balance of security and performance.
3.  **Regular Audits**: Periodically check your `09-workflow.md` logs for unauthorized connection attempts.

---

[← Operation Workflow](09-workflow.md) | [Index](README.md) | [Development Plan →](11-roadmap.md)
