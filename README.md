# Shellixa: The Modern SSH Workstation for Linux

![Shellixa Logo](https://via.placeholder.com/150)

**Shellixa** is a professional-grade, open-source, GUI-based SSH client designed with a **Linux-first** approach. Built for power users, it provides a premium remote management experience that is expanding to support Windows and macOS.

## 🚀 Why Shellixa?

Inspired by premium tools like Termius, Shellixa aims to be the fully open-source alternative that respects your privacy and fits perfectly into your Linux workflow.

-   **Clean GUI**: Visual host management with drag-and-drop and OS icons.
-   **AI Intelligence**: Helium autocomplete and Gloria AI agent for shell commands.
-   **Multi-Protocol**: Native support for SSH, Mosh, Telnet, and SFTP.
-   **Security**: E2EE Vault, FIDO2 hardware keys, and Biometric auth.
-   **Productivity**: Project-based Workspaces, Split View, and Snippets.

## 📖 Documentation

Everything you need to know about Shellixa is available in our [Documentation Center](docs/README.md).

### ⚡ Quick Links
1.  **[Overview](docs/01-overview.md)**: What is Shellixa?
2.  **[Installation Guide](docs/13-installation.md)**: Get started in seconds.
3.  **[Security](docs/10-security.md)**: How we keep your keys safe.
4.  **[Development Plan](docs/11-roadmap.md)**: Phased implementation status and remaining feature work.

## 🗺️ Development Plan

Shellixa is being delivered in six phases, moving from core infrastructure to premium productivity features and release packaging.

-   **Phase 1: Core Foundation** `[Done]` - Database layer, configuration system, main window layout, and logging.
-   **Phase 2: SSH Connectivity & Terminal** `[Done]` - Interactive SSH sessions, terminal integration, command streaming, and multi-session support.
-   **Phase 3: Host Management & UX** `[Done]` - Visual host manager, grouping and inheritance, search, and recent connections.
-   **Phase 4: Security & Vault** `[Done]` - Key management, AES-256 vault encryption, master password, and FIDO2 support.
-   **Phase 5: Productivity & Polish** `[In Progress]` - Snippet library, Helium AI suggestions, theme engine, and SFTP basics.
-   **Phase 6: Packaging & Distribution** `[Planned]` - `.deb` and `.rpm` installers built with PyInstaller or similar tooling.

See the full phased roadmap in **[docs/11-roadmap.md](docs/11-roadmap.md)**.

## 📦 Installation

To install Shellixa on Ubuntu/Debian:

```bash
sudo apt update
sudo apt install ./shellixa_1.0.0_amd64.deb
```

For other distributions (Fedora, AppImage, or Source), see the **[Full Installation Guide](docs/13-installation.md)**.

## 🤝 Contributing

We welcome contributions from everyone! Whether it's fixing a bug, suggesting a feature, or improving documentation.

-   Read our **[Contributing Guide](docs/12-contributing.md)**.
-   Report issues on **[GitHub](https://github.com/shellixa/shellixa/issues)**.

## ⚖️ License

Shellixa is released under the [MIT License](docs/14-license.md).

---

Built with ❤️ for the Linux community.
