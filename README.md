# Android File Browser (PyQt + ADB)

This is a desktop application built using **PyQt6** that allows you to browse files and folders on a connected Android device via **ADB** (Android Debug Bridge). It supports basic navigation, drag-and-drop upload from Finder, and file download via drag-out.

## ✅ Features

* 📂 List files and folders under `/storage/emulated/0`
* 📁 Navigate into folders (double-click)
* ◀ Go back to the previous folder (with disabled state on home)
* 👁 Toggle hidden files (dot-prefixed)
* ↕ Sort files by name, size, or modified date
* 🗑 Right-click to **delete** file(s) from device
* 📤 Right-click to **export** file(s) to local machine
* 🖱 Drag-and-drop files **from Finder to Android**
* 🔔 Warning shown if app is closed with USB debugging enabled
* 📡 Dialog if no device is connected or USB debugging is disabled

## 📦 Requirements

### Python

* Python 3.8+

### Dependencies

```bash
pip install PyQt6
```

### ADB (Android Debug Bridge)

Install via Homebrew (macOS):

```bash
brew install android-platform-tools
```

Make sure your device is connected and authorized:

```bash
adb devices
```

> You should see your phone listed as a connected device.

## 🚀 How to Run

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/android-file-browser.git
cd android-file-browser
```

### 2. Set up a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the App

```bash
python main.py
```

You should see a window listing files under `/storage/emulated/0`.

## 🧪 Troubleshooting

### Empty screen / no files?

* Ensure device is authorized (`adb devices`)
* Check if `/storage/emulated/0` is accessible (`adb shell ls /storage/emulated/0`)
* Try updating the path in `main_window.py`

## 📜 License

MIT

---
Made with ❤️ using Python and Qt.
