# cleanup_crops.py
import os
from pathlib import Path

# Move existing crops to organized folder
debug_folder = Path("debug_crops")
debug_folder.mkdir(exist_ok=True)

root_files = Path(".").glob("crop_*.jpg")
for file in root_files:
    file.rename(debug_folder / file.name)
    print(f"Moved {file.name} to debug_crops/")

print("Cleanup complete!")
