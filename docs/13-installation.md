# Installation Guide

Shellixa is currently optimized for Linux systems. Below are the various ways to get it running.

## 📦 Package Install (Recommended)

### Debian / Ubuntu (.deb)
```bash
wget https://github.com/shellixa/shellixa/releases/download/v1.0.0/shellixa_1.0.0_amd64.deb
sudo dpkg -i shellixa_1.0.0_amd64.deb
sudo apt install -f
```

### Fedora / RHEL (.rpm)
```bash
sudo dnf install https://github.com/shellixa/shellixa/releases/download/v1.0.0/shellixa-1.0.0.x86_64.rpm
```

## 💎 AppImage
The AppImage works on almost any modern Linux distribution.
1. Download the `.AppImage` from the releases page.
2. Make it executable: `chmod +x Shellixa.AppImage`.
3. Run it: `./Shellixa.AppImage`.

## 🏗️ Source Build
If you want to build the latest version from source:

1.  **Clone the Repo**:
    ```bash
    git clone https://github.com/shellixa/shellixa.git
    cd shellixa
    ```

2.  **Install Dependencies**:
    ```bash
    npm install
    # or if using Rust core
    cargo build 
    ```

3.  **Run Development Mode**:
    ```bash
    npm run dev
    ```

4.  **Build Production Package**:
    ```bash
    npm run build
    ```

## 🚀 Post-Installation
After installing, you can find Shellixa in your application menu. On first launch, you will be prompted to set up your master password for the secure vault.

---

[← Contributing Guide](12-contributing.md) | [Index](README.md) | [License Information →](14-license.md)
