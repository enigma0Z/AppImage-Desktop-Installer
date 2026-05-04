# AppImage Desktop Creator (Updated)

A Python script that automatically creates desktop entries for AppImage files. It monitors a specified directory (and its subdirectories) for AppImage files and creates corresponding `.desktop` files, making your AppImages easily accessible from your desktop environment.

## Features

**[**adrfrank** (Original Creator)](https://github.com/adrfrank/appimage_desktop_creator)**
- Automatically creates desktop entries for AppImage files
- Recursively monitors directories for new AppImages
- Extracts application name and icon from AppImages
- Handles AppImage removal by cleaning up desktop entries
- Supports relative and absolute paths
- Creates desktop entries in the user's local applications directory

**[**Klotheju**](https://github.com/Klotheju/updated_appimage_desktop_creator/)**
- Auto-makes AppImages executable (fixes manually having to 'chmod +x' so it creates a '.desktop' file)
- Visual feedback in ~/appimage-watcher.log
- Debug-friendly output

## Requirements

- Python 3.x
- Linux operating system
- Required Python packages:
  - `inotify`
  - `shutil`
  - `subprocess`

## Installation

1. Clone this repository or download the script:
```bash
git clone https://github.com/Klotheju/updated_appimage_desktop_creator
cd updated_appimage_desktop_creator
```

2. Install the required Python package:
```bash
python -m venv venv
source venv/bin/activate
pip install inotify
```
3. Make it run in background (Daemon Mode - Universal):
```bash
cd /path/to/appimage_desktop_creator
source venv/bin/activate
nohup venv/bin/python appimage_desktop_creator.py > ~/appimage-watcher.log 2>&1 &
echo $! > ~/appimage-watcher.pid
```

## Usage

1. Edit the `WATCH_DIR` variable in the script to point to your desired directory:
```python
WATCH_DIR = os.path.expanduser('~/Applications')  # Change this to your preferred directory to detect and watch for .AppImage
```

2. Run the script:
```bash
python appimage_desktop_creator.py
```

The script will:
- Create desktop entries for existing AppImages in the watch directory
- Monitor the directory for new AppImages
- Create desktop entries for new AppImages automatically
- Remove desktop entries when AppImages are deleted

## Directory Structure

- `~/Applications` (default watch directory) - Place your AppImages here
- `~/.local/share/applications` - Desktop entries are created here
- `~/.local/share/icons` - Application icons are stored here

## How It Works

1. The script monitors the specified directory and its subdirectories for AppImage files
2. When an AppImage is detected:
   - It extracts the AppImage to a temporary directory
   - Reads the application name and icon from the embedded .desktop file
   - Copies the icon to the local icons directory
   - Creates a desktop entry in the local applications directory
3. When an AppImage is removed:
   - The corresponding desktop entry is automatically deleted

## Customization

You can customize the script by modifying:
- `WATCH_DIR`: Change the directory to monitor
- `DESKTOP_DIR`: Change where desktop entries are created
- Desktop entry template in the `generate_desktop_file` function

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 

