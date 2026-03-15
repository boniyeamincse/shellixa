# UI Pages Guide

Shellixa is built as a **first-class GUI application**, ensuring that every interaction follows modern desktop design patterns. Below is a breakdown of the primary screens and components.

## 📊 Dashboard / Home Screen
The high-level command center for your infrastructure.
-   **Connection Overview**: A visual grid or list of all saved hosts featuring:
    -   **OS Icons**: Clear indicators for Linux (Ubuntu, Debian, Fedora), Windows, and macOS.
    -   **Live Status**: Real-time Online/Offline indicators.
    -   **Last Connected**: Time-stamps for the most recent access.
-   **Quick Actions**: Prominent buttons for **"New Connection,"** **"Group Connection,"** and **"Favorites."**
-   **Unified Search Bar**: Instant, fuzzy-search for hosts, groups, labels, and tags.
-   **Recent Connections**: A dedicated section or carousal for the top 5 most recently accessed servers.

## 🛠️ Sidebar Navigation
Intuitive, keyboard-friendly navigation.
-   **Groups & Favorites**: A collapsible tree structure to organize vast server fleets with inherited settings.
-   **History & Logs**: Instant access to previous session logs and command history.
-   **Settings & Profiles**: A central hub to manage:
    -   **Keychain**: SSH keys and passwords.
    -   **Appearance**: Themes (Cyberpunk, Kanagawa, Nord) and Fonts (Nerd Fonts supported).
    -   **Preferences**: Terminal behavior and global shortcuts.

## 🖥️ Connection Tab / Terminal
The primary interaction workspace.
-   **Tabbed Terminal**: Supports multiple SSH sessions in individual tabs or a native **Split View**.
-   **Session Info Bar**: A persistent header showing `hostname`, `IP`, `username`, and `encryption_status`.
-   **Command History Panel**: An optional slide-out panel showing recent commands for quick re-execution.
-   **Copy/Paste Enhancements**: Smart context-aware copying that strips unnecessary prompts or multi-line characters.
-   **Dark/Light Mode Toggle**: High-contrast themes for day and night workflows.

## 🔑 Key Management Panel
Dedicated interface for identity management.
-   **SSH Keys Management**: A clean interface to add, import, export, and generate new key pairs.
-   **Auto-Apply Logic**: A "Smart Assign" feature that automatically matches the correct key to a connection based on host metadata.

## 🌍 Multi-Platform UX Strategy
While Linux-first, Shellixa adapts its UI to feel native on every platform:
-   **Linux**: Native GTK/Qt integration with system tray icons and global hotkeys.
-   **Windows**: Modern Ribbon-style top menus and integration with Windows 11 Action Center for session alerts.
-   **macOS**: Minimalistic toolbar, native San Francisco typography, and menu bar item for background sessions.

## 🎨 Design & Style Inspirations
-   **Clean and Minimal**: Inspired by **Termius**—prioritizing content and terminal readability over heavy decoration.
-   **Vibrant Accent Colors**: Highlighting active sessions and critical "Connect" actions with curated palettes.
-   **Intuitive Iconography**: Using identifiable OS and status icons to minimize cognitive load.

---

[← API Design](07-api-design.md) | [Index](README.md) | [Operation Workflow →](09-workflow.md)
