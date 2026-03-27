import shutil
import os

# Source Directory (Brain) - Hardcoded absolute path for reliability in this session
src_dir = r"C:\Users\nasan\.gemini\antigravity\brain\6bf4624f-54c6-4857-acd1-ec19ef02f16b"

# Destination Directory (Game Assets)
dest_dir = os.path.join(os.getcwd(), "game", "assets")

# Ensure destination exists
os.makedirs(dest_dir, exist_ok=True)

files = {
    "cartoon_floor_1765980581063.png": "floor.png",
    "cartoon_wall_1765980737460.png": "wall.png",
    "cartoon_obstacle_1765981100394.png": "obstacle.png",
    "cartoon_coin_1765980903667.png": "coin.png"
}

print(f"Copying assets from {src_dir} to {dest_dir}...")

for src_name, dest_name in files.items():
    src_path = os.path.join(src_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    
    try:
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            print(f"OK: {dest_name}")
        else:
            print(f"MISSING: {src_path}")
    except Exception as e:
        print(f"ERROR copying {src_name}: {e}")

print("Done.")
