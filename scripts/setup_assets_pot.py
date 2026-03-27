import shutil
import os
import cv2

# Source Directory (Brain)
src_dir = r"C:\Users\nasan\.gemini\antigravity\brain\6bf4624f-54c6-4857-acd1-ec19ef02f16b"

# Destination Directory (Game Assets)
dest_dir = os.path.join(os.getcwd(), "game", "assets")
os.makedirs(dest_dir, exist_ok=True)

files = {
    "cartoon_floor_1765980581063.png": "floor.png",
    "cartoon_wall_1765980737460.png": "wall.png",
    "cartoon_obstacle_1765981100394.png": "obstacle.png",
    "cartoon_coin_1765980903667.png": "coin.png"
}

print(f"Processing assets from {src_dir} to {dest_dir}...")

for src_name, dest_name in files.items():
    src_path = os.path.join(src_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    
    try:
        if os.path.exists(src_path):
            # Read with OpenCV
            img = cv2.imread(src_path)
            if img is None:
                print(f"Failed to read image: {src_path}")
                continue
                
            # Resize to power of two (512x512)
            img = cv2.resize(img, (512, 512), interpolation=cv2.INTER_AREA)
            
            # Write key
            cv2.imwrite(dest_path, img)
            print(f"Resized and Saved: {dest_name}")
        else:
            print(f"MISSING: {src_path}")
    except Exception as e:
        print(f"ERROR processing {src_name}: {e}")

print("Done.")
