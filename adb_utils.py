import subprocess
import os
from typing import List, Tuple

class AdbFileEntry:
    def __init__(self, name: str, size: str, modified: str, is_dir: bool):
        self.name = name
        self.size = size
        self.modified = modified
        self.is_dir = is_dir

def list_files(path: str) -> List[AdbFileEntry]:
    try:
        result = subprocess.check_output(["adb", "shell", f"ls -la '{path}'"], text=True)
        lines = result.strip().split('\n')[1:]  # Skip total line
        entries = []
        for line in lines:
            parts = line.split()
            if len(parts) < 8:
                continue
            name = ' '.join(parts[7:])
            size = parts[4]
            modified = f"{parts[5]} {parts[6]}"
            is_dir = parts[0].startswith('d')
            entries.append(AdbFileEntry(name, size, modified, is_dir))
        return entries
    except subprocess.CalledProcessError:
        return []

def pull_file(android_path: str, local_path: str):
    subprocess.run(["adb", "pull", android_path, local_path])

def push_file(local_path: str, android_path: str):
    subprocess.run(["adb", "push", local_path, android_path])

def human_readable_size(size_bytes: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"
