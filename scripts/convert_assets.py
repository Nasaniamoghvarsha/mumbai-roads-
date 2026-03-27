import cv2
import os

# Asset Directory
assets_dir = os.path.join(os.getcwd(), "game", "assets")
brain_dir = r"C:\Users\nasan\.gemini\antigravity\brain\6bf4624f-54c6-4857-acd1-ec19ef02f16b"

# Mapping: Brain File -> (Target Name, Extension)
files = {
    "cartoon_floor_1765980581063.png": ("floor.jpg", "jpg"),
    "cartoon_wall_1765980737460.png": ("wall.jpg", "jpg"),
    "cartoon_obstacle_1765981100394.png": ("obstacle.jpg", "jpg"),
    "cartoon_coin_1765980903667.png": ("coin.png", "png")
}

print(f"Converting assets from {brain_dir}...")

for brain_name, (target_name, ext) in files.items():
    src = os.path.join(brain_dir, brain_name)
    dst = os.path.join(assets_dir, target_name)
    
    if os.path.exists(src):
        img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
        if img is None:
            print(f"FAILED to read {src}")
            continue
            
        # Resize to 512x512 (Power of 2)
        img = cv2.resize(img, (512, 512), interpolation=cv2.INTER_AREA)
        
        # Save
        if ext == "jpg":
            # Drop alpha if exists for JPG
            if img.shape[2] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            cv2.imwrite(dst, img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        else:
            cv2.imwrite(dst, img)
            
        print(f"Saved {dst}")
    else:
        print(f"MISSING {src}")

print("Conversion Complete.")
