**[Credits: **adrfrank** (Original Creator)](https://github.com/adrfrank/appimage_desktop_creator)**

# AppImage Desktop Installer

A Python script that creates desktop entries for AppImage files, either on-demand or automatically.

For automatic appimage installation, it monitors a specified directory (and its subdirectories) for AppImage files and creates corresponding `.desktop` files, making your AppImages easily accessible from your desktop environment.

For manual appimage installation, the `install` and `uninstall` subcommands are provided

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

**[**enigma0Z**](https://github.com/enigma0Z/Appimage-Desktop-Installer)**
- Add install/uninstall subcommands
- Add PyPi-ready packaging

## Requirements

- Python 3.x
- Linux operating system
- [pipx](https://pipx.pypa.io/stable/how-to/install-pipx/)

## Installation (developer/tinkerer)

1. Clone this repository:
```bash
git clone https://github.com/enigma0Z/AppImage-Desktop-Installer.git
```

2. Install using pipx:
```bash
pipx install -e ./AppImage-Desktop-Installer
```

## Usage

### Monitor a directory (default is ~/Applications)

```bash
nohup adi watch > ~/appimage-watcher.log 2>&1 &
echo $! > ~/appimage-watcher.pid
```

In watch mode, the script will:
- Create desktop entries for existing AppImages in the watch directory
- Monitor the directory for new AppImages
- Create desktop entries for new AppImages automatically
- Remove desktop entries when AppImages are deleted

### Manually install an appimage

```bash
adi install path/to/the/application.AppImage
```

### Manually uninstall an appimage

```bash
adi uninstall path/to/the/installed/application.AppImage
```

### Notes

You can override the default directory of `~/Applications` by specifying `--install-dir` on the CLI
```bash
adi --install-dir ~/SomethingElse daemon
```

## Directory Structure

- `~/Applications` (default watch directory) - Place your AppImages here
- `~/.local/share/applications` - Desktop entries are created here
- `~/.local/share/icons` - Application icons are stored here

## Customization

You can customize the script (`src/appimage_desktop_installer/__init__.py`) by modifying:
- `USER_APP_DIR`: Change the default directory to monitor / where apps are installed by the `install` subcommand
- `DESKTOP_DIR`: Change where desktop entries are created
- Desktop entry template in the `generate_desktop_file` function

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 
