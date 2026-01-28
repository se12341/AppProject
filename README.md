# MultiAppGUI

A modern, multi-threaded desktop GUI utility application built with CustomTkinter that provides 4 powerful file management tools.

## Features

### 🎬 App 1: Web2Real - File Format Converter
- Convert `.webm` video files to `.mp4` format
- Convert `.webp` image files to `.jpg` format
- Multi-threaded processing (10 threads) for fast conversions
- Real-time progress tracking
- Recursive directory processing

### 📁 App 2: Empty Folders - Directory Flattener
- Move all files from subdirectories to the root folder
- Automatically delete empty subdirectories
- Multi-threaded file operations (10 threads)
- Progress bar for file movement operations
- Preserves file structure while consolidating location

### 🏷️ App 3: Replace Names - Duplicate Name Resolver
- Identify files with duplicate names between two folders
- Rename duplicate files with random suffixes (format: `filename_xxxxxxxx.ext`)
- Multi-threaded renaming (10 threads)
- Progress tracking during bulk operations
- Prevents filename conflicts

### 🔍 App 4: Duplicate Finder - SHA256-Based Deduplication
- Find duplicate files using SHA256 hash comparison
- Automatically delete duplicates while keeping the first occurrence
- Multi-threaded hashing (10 threads) for rapid file analysis
- Real-time processing status updates
- Works with any file type and handles large directories efficiently

## Technical Details

- **Framework:** CustomTkinter (modern Python GUI framework)
- **Threading:** ThreadPoolExecutor with 10 workers per app for responsive UI
- **Python Version:** 3.12+
- **GUI Theme:** Supports Dark/Light/System modes
- **Architecture:** Single-window multi-app interface with seamless app switching

## Requirements

- Python 3.12 or higher
- All dependencies listed in `requirements.txt`

## Installation

### Option 1: Using Pre-built Executable (Windows)
1. Download `MultiAppGUI.exe` from the releases
2. Run the executable directly (no installation required)

### Option 2: Using Python Source Code
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   source .venv/bin/activate # macOS/Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python MultiAppGUIver1.5.1.py
   ```

## Usage

1. **Launch the application** - Run the executable or Python script
2. **Select an app** - Click one of the 4 navigation buttons on the left
3. **Enter the directory path** - Paste the folder path where you want to perform operations
4. **Click the action button** - Start the operation (progress bar will display)
5. **Wait for completion** - Operations run in background threads, keeping UI responsive

### Example Operations:

**Web2Real:** Convert video/image formats
```
Input: C:\Users\Documents\media
Output: All .webm files converted to .mp4, all .webp files converted to .jpg
```

**Empty Folders:** Flatten directory structure
```
Input: C:\Users\Documents\nested_folders
Output: All files moved to root, all subdirectories deleted
```

**Replace Names:** Fix duplicate names
```
Input: Folder A and Folder B with overlapping filenames
Output: Duplicates in Folder A renamed with random suffixes
```

**Duplicate Finder:** Remove duplicate files
```
Input: C:\Users\Documents\files_with_duplicates
Output: Duplicates identified and deleted, keeping first occurrence only
```

## Performance

All operations use multi-threading with 10 concurrent workers:
- **Video Conversion:** ~2-5 videos per second (varies by size)
- **File Movement:** Moves thousands of files in seconds
- **Duplicate Detection:** Processes large file collections efficiently using parallel hashing
- **UI Responsiveness:** Never freezes, all operations run in background threads

## Architecture

```
MultiAppGUI (Main Window)
├── App1 (Web2Real)
│   ├── convert_videos() - Multi-threaded .webm to .mp4 conversion
│   └── convert_images() - Multi-threaded .webp to .jpg conversion
├── App2 (Empty Folders)
│   └── takedir() - Multi-threaded file consolidation
├── App3 (Replace Names)
│   └── rename_duplicate_files() - Multi-threaded name resolution
└── App4 (Duplicate Finder)
    └── find_and_delete_duplicates() - Multi-threaded hash-based detection
```

## Building Executable (PyInstaller)

To create a standalone `.exe` file:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "MultiAppGUI" \
  --hidden-import=imageio \
  --hidden-import=imageio_ffmpeg \
  --hidden-import=moviepy \
  --hidden-import=PIL \
  --hidden-import=customtkinter \
  --collect-all imageio \
  --collect-all imageio_ffmpeg \
  MultiAppGUIver1.5.1.py
```

The executable will be created in the `dist/` folder.

## Troubleshooting

**GUI freezes during operation:**
- This shouldn't happen as all operations use background threading
- If it does, please report the issue

**File conversion errors:**
- Ensure sufficient disk space
- Check that source files aren't corrupted
- Verify write permissions in the target directory

**Duplicate Finder takes too long:**
- Progress label shows processing status
- Large directories (100k+ files) may take several minutes
- Can be optimized by splitting into subdirectories

## License

MIT License

## Author

Created as a utility application for efficient file management and format conversion tasks.

---

**Version:** 1.5.1  
**Last Updated:** January 2026
