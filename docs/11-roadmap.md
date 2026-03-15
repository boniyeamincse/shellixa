# Shellixa: Phased Development Plan

This document outlines the step-by-step development roadmap for the Shellixa SSH workstation.

## 🏗️ Phase 1: Core Foundation (The Skeleton)
Goal: Establish the basic application structure and data persistence.

- [x] **1.1 Database Layer**: Finalize `DBHandler` with full CRUD for hosts and groups.
- [x] **1.2 Configuration System**: Implement global settings (theme, font, auto-connect).
- [x] **1.3 Main Window Layout**: Refine the PyQt6 `MainWindow` with a collapsible sidebar and tabbed content area.
- [x] **1.4 Logging & Error Handling**: Set up comprehensive application-wide logging.

## 🔌 Phase 2: SSH Connectivity & Terminal (The Nervous System)
Goal: Enable remote server communication and interactive shell.

- [x] **2.1 Backend Wrapper**: Enhance `SSHConnection` to support long-lived interactive sessions (channels).
- [x] **2.2 Terminal Emulator Integration**: Integrate a terminal emulator (e.g., `pyte` or a custom bridge to system terminal).
- [x] **2.3 Command Execution**: Implement basic command execution and output streaming to the UI.
- [x] **2.4 Multi-session Management**: Allow switching between active terminal tabs without losing connection state.

## 🗂️ Phase 3: Host Management & UX (The Muscle)
Goal: Make the connection management professional and efficient.

- [x] **3.1 Visual Host Manager**: Create a visual dashboard to add/edit/delete hosts with OS icon selection.
- [x] **3.2 Grouping & Inheritance**: Implement the folder/tree structure in the sidebar with credential inheritance.
- [x] **3.3 Search & Filter**: Add a global search bar to instantly find hosts or groups.
- [x] **3.4 Recent Connections**: Implement a "Recents" list with one-click reconnect.

## 🛡️ Phase 4: Security & Vault (The Shield)
Goal: Ensure all sensitive data is locked down.

- [x] **4.1 Key Management Panel**: Full interface to generate, import, and assign SSH keys.
- [x] **4.2 Data Encryption**: Implement AES-256 encryption for the SQLite database (Vault).
- [x] **4.3 Master Password**: Add an optional master password gate on application startup.
- [x] **4.4 FIDO2/Biometrics**: Integration with hardware keys (YubiKey, etc.).

## 🚀 Phase 5: Productivity & Polish (The Brain)
Goal: Add premium productivity features and styling.

- [ ] **5.1 Snippet Library**: Implement a panel to save, tag, and quickly run shell snippets.
- [ ] **5.2 Helium AI Suggestions**: Basic integration with AI for command autocomplete.
- [ ] **5.3 Theme Engine**: Support for multiple dark/light color schemes.
- [ ] **5.4 SFTP Basics**: Integrated file browser for remote file manipulation.

## 📦 Phase 6: Packaging & Distribution (The Launch Pad)
Goal: Prepare Shellixa for repeatable Linux distribution and installation.

- [ ] **6.1 Packaging**: Create `.deb` and `.rpm` installers using PyInstaller or similar tools.

---

[← Security Overview](10-security.md) | [Index](README.md) | [Contributing Guide →](12-contributing.md)
