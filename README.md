# Android File Browser (PyQt + ADB)

This is a desktop application built using **PyQt6** that allows you to browse files and folders on a connected Android device via **ADB** (Android Debug Bridge). It supports basic navigation, drag-and-drop upload from Finder, and file download via drag-out.

---

## ✅ Features

* List files/folders on the Android device
* Navigate into folders (double-click)
* Go back to previous folder
* Drag-and-drop files **from Finder to Android**
* Basic support for **pulling files** to Mac `/tmp` (can be extended)

---

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

---

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
pip install -r requirements.txt  # optional if created
```

### 3. Run the App

```bash
python main.py
```

You should see a window listing files under `/storage/emulated/0`.

---

## 📁 Project Structure

```
android-file-browser/
├── main.py               # Entry point
├── adb_utils.py          # Handles adb commands
├── ui/
│   └── main_window.py    # PyQt UI logic
├── .gitignore
├── README.md
└── requirements.txt      # (optional)
```

---

## 🧪 Troubleshooting

### Empty screen / no files?

* Ensure device is authorized (`adb devices`)
* Check if `/storage/emulated/0` is accessible (`adb shell ls /storage/emulated/0`)
* Try updating the path in `main_window.py`

---

## 🔧 Roadmap

* [ ] File previews / icons
* [ ] Pull via drag to Finder
* [ ] Delete/rename support
* [ ] Right-click context menu
* [ ] Packaging into `.app` or `.dmg`

---

## 📜 License

MIT

---

Made with ❤️ using Python and Qt.
