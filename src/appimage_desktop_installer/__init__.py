import os
import subprocess
import shutil
import inotify.adapters

USER_APP_DIR = os.path.expanduser('~/Applications')
DESKTOP_DIR = os.path.expanduser('~/.local/share/applications')

def find_appimages(directory):
    """Recursively find all AppImage files in the given directory."""
    appimages = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.AppImage'):
                appimages.append(os.path.join(root, file))
    return appimages

def extract_appimage_info(appimage_path):
    # Create a temp dir
    tmp_dir = f"/tmp/appimage-extract-{os.path.basename(appimage_path)}"
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir, exist_ok=True)
    # Extract the appimage
    extract_cmd = [appimage_path, '--appimage-extract']
    try:
        subprocess.run(extract_cmd, cwd=tmp_dir, timeout=60, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"Error extracting {appimage_path}: {e}")
        return None

    # Find the .desktop file inside squashfs-root/
    desktop_path = None
    for root, dirs, files in os.walk(os.path.join(tmp_dir, 'squashfs-root')):
        for f in files:
            if f.endswith('.desktop'):
                desktop_path = os.path.join(root, f)
                break
        if desktop_path:
            break

    if not desktop_path:
        print(f"No .desktop file found in {appimage_path}")
        shutil.rmtree(tmp_dir)
        return None

    # Parse .desktop for Name and Icon
    name = None
    icon = None
    with open(desktop_path) as f:
        for line in f:
            if line.startswith('Name='):
                name = line.strip().split('=', 1)[1]
            if line.startswith('Icon='):
                icon = line.strip().split('=', 1)[1]
    # Try to find the icon file
    icon_path = None
    if icon:
        icon_basename = os.path.basename(icon)
        for root, dirs, files in os.walk(os.path.join(tmp_dir, 'squashfs-root')):
            for f in files:
                if f.startswith(icon_basename):
                    icon_path = os.path.join(root, f)
                    break
            if icon_path:
                break
    # Copy icon to local icons dir
    if icon_path:
        target_icon = os.path.join(os.path.expanduser('~/.local/share/icons'), os.path.basename(icon_path))
        os.makedirs(os.path.dirname(target_icon), exist_ok=True)
        shutil.copy(icon_path, target_icon)
        icon = target_icon
    else:
        icon = None

    shutil.rmtree(tmp_dir)
    return {'name': name or os.path.basename(appimage_path), 'icon': icon}

def generate_desktop_file(appimage_path, name, icon):
    exec_line = f'"{appimage_path}"'
    icon_line = f"Icon={icon}" if icon else ""
    desktop_entry = f"""[Desktop Entry]
Type=Application
Name={name}
Exec={exec_line}
{icon_line}
Comment=AppImage: {name}
Terminal=false
Categories=Utility;
"""
    desktop_filename = os.path.join(DESKTOP_DIR, f"{os.path.splitext(os.path.basename(appimage_path))[0]}.desktop")
    with open(desktop_filename, 'w') as f:
        f.write(desktop_entry)
    os.chmod(desktop_filename, 0o755)
    print(f"Generated: {desktop_filename}")

def process_appimage(appimage_path):
    """Process AppImage: chmod + extract + create desktop"""
    # 1. Make executable (handles .part files too)
    os.chmod(appimage_path, 0o755)
    print(f"✓ Executable: {os.path.basename(appimage_path)}")
    
    # 2. Wait for download completion
    import time
    time.sleep(1)
    
    # 3. Extract & generate desktop
    info = extract_appimage_info(appimage_path)
    if info:
        generate_desktop_file(appimage_path, info['name'], info['icon'])
        print(f"✓ Desktop created: {info['name']}")
    else:
        print(f"✗ Failed to process: {appimage_path}")

def uninstall(appimage: str, remove_appimage=False):
    if (remove_appimage):
        os.remove(appimage)

    desktop_file = os.path.join(DESKTOP_DIR, f"{os.path.splitext(appimage)[0]}.desktop")
    if os.path.exists(desktop_file):
        os.remove(desktop_file)
        print(f"Removed: {desktop_file}")

def monitor_directory(watch_dir: str = USER_APP_DIR):
    # Initial scan
    appimages = find_appimages(watch_dir)
    for appimage_path in appimages:
        process_appimage(appimage_path)

    i = inotify.adapters.Inotify()
    # Add watch recursively
    for root, dirs, _ in os.walk(watch_dir):
        i.add_watch(root)
        for dir_name in dirs:
            i.add_watch(os.path.join(root, dir_name))

    print(f"Monitoring {watch_dir} and subdirectories for AppImages...")
    for event in i.event_gen(yield_nones=False):
        assert event is not None
        (_, type_names, path, filename) = event
        if filename.endswith('.AppImage'):
            file_path = os.path.join(path, filename)
            if 'IN_CREATE' in type_names or 'IN_MOVED_TO' in type_names:
                print(f"New AppImage found: {file_path}")
                process_appimage(file_path)
            elif 'IN_DELETE' in type_names or 'IN_MOVED_FROM' in type_names:
                # Optionally remove the .desktop file
                desktop_file = os.path.join(DESKTOP_DIR, f"{os.path.splitext(filename)[0]}.desktop")
                if os.path.exists(desktop_file):
                    os.remove(desktop_file)
                    print(f"Removed: {desktop_file}")
