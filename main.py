import os
import shutil
import json
import argparse
from datetime import datetime

# --- Load config ---
with open("config.json") as f:
    config = json.load(f)

BASE_DIR = config.get("base_dir", "to_sort")
FOLDERS = config.get("folders", {})
LOG_FILE = config.get("log_file", "log.txt")

# --- CLI Args ---
parser = argparse.ArgumentParser(description="AutoFile-Butler v2")
parser.add_argument("--dry-run", action="store_true", help="Show actions without moving files")
parser.add_argument("--path", type=str, help="Folder path to sort")
args = parser.parse_args()

if args.path:
    BASE_DIR = args.path

# --- Logging ---
def log_action(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

# --- Determine folder ---
def get_folder(extension):
    for folder, exts in FOLDERS.items():
        if extension in exts:
            return folder
    return "Others"

# --- Organize files ---
def organize(dry_run=False):
    if not os.path.exists(BASE_DIR):
        print(f"Folder '{BASE_DIR}' not found.")
        return

    for file in os.listdir(BASE_DIR):
        file_path = os.path.join(BASE_DIR, file)
        if os.path.isfile(file_path):
            name, ext = os.path.splitext(file)
            folder = get_folder(ext.lower())
            target_dir = os.path.join(BASE_DIR, folder)

            if dry_run:
                print(f"[DRY-RUN] {file} -> {folder}")
            else:
                os.makedirs(target_dir, exist_ok=True)
                shutil.move(file_path, os.path.join(target_dir, file))
                log_action(f"Moved {file} to {folder}")

if __name__ == "__main__":
    organize(dry_run=args.dry_run)
    print("Done ✅" if not args.dry_run else "Dry-run complete 🔍")
