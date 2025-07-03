import subprocess
import os
from typing import List


class AdbFileEntry:
    def __init__(self, name: str, size: str, modified: str, is_dir: bool):
        self.name = name
        self.size = size
        self.modified = modified
        self.is_dir = is_dir


def list_files(path: str) -> List[AdbFileEntry]:
    try:
        result = subprocess.check_output(
            ["adb", "shell", f"ls -la '{path}'"], text=True
        )
        lines = result.strip().split("\n")[1:]  # Skip total line
        entries: List[AdbFileEntry] = []
        for line in lines:
            parts = line.split()
            if len(parts) < 8:
                continue
            name = " ".join(parts[7:])
            size = parts[4]
            modified = f"{parts[5]} {parts[6]}"
            is_dir = parts[0].startswith("d")
            entries.append(AdbFileEntry(name, size, modified, is_dir))
        return entries
    except subprocess.CalledProcessError:
        return []


def pull_file(android_path: str, local_path: str):
    subprocess.run(["adb", "pull", android_path, local_path])


def push_file(local_path: str, android_path: str):
    subprocess.run(["adb", "push", local_path, android_path])


def is_device_connected() -> bool:
    try:
        result = subprocess.check_output(["adb", "get-state"], text=True).strip()
        return result == "device"
    except subprocess.CalledProcessError:
        return False


def pull_files(android_paths: List[str], local_dir: str) -> None:
    for path in android_paths:
        filename: str = os.path.basename(path)
        local_path: str = os.path.join(local_dir, filename)
        subprocess.run(["adb", "pull", path, local_path])


def delete_files_on_device(android_paths: List[str]) -> None:
    for path in android_paths:
        subprocess.run(["adb", "shell", "rm", "-rf", f'"{path}"'])
