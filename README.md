# 🎬 Video File Consolidator

> A desktop app that gathers scattered video files from deeply nested folders into a single destination folder — in one click.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python) ![tkinter](https://img.shields.io/badge/GUI-tkinter-green) ![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?logo=windows)

---

## 📌 Overview

Managing videos across deeply nested folder structures is tedious. This tool automatically scans all subfolders recursively and consolidates every video file into one place — no installation required, just run the `.exe`.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 📁 Recursive folder scan | Automatically detects videos in all subfolders |
| 🔀 Move or Copy | Choose whether to keep the original files |
| 🔁 Duplicate handling | Renames conflicts automatically (e.g. `video_1.mp4`) |
| 📊 Real-time progress | Live progress bar + activity log |
| 🎞️ 19 formats supported | mp4, mkv, avi, mov, wmv, flv, webm, m4v, mpg, ts, mts, and more |

---

## 🖥️ How to Use

1. Double-click `VideoConsolidator.exe`
2. Select the **source folder** (all subfolders will be scanned automatically)
3. Select the **destination folder**
4. Choose **Move** or **Copy**
5. Click **Start**

---

## 🛠️ Tech Stack

- **Language:** Python 3
- **GUI:** tkinter
- **Build:** PyInstaller (standalone `.exe`, no install needed)

---

## 📂 Project Structure

```
video_mover/
├── video_mover.py        # Main source code
└── dist/
    └── VideoConsolidator.exe  # Standalone executable
```

---

## 💡 Motivation

When working with large video libraries, footage is often organized by date, subject, or camera — leading to deeply nested directories. This tool was built to eliminate the repetitive manual work of gathering files before editing.

---

## 🚀 Build from Source

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name VideoConsolidator video_mover.py
```
