import os
import shutil

ARTIFACT_DIR = r"c:\Users\nasan\.gemini\antigravity\brain\6bf4624f-54c6-4857-acd1-ec19ef02f16b"
DEST_DIR = r"c:\Users\nasan\OneDrive\Desktop\game\assets"

FILES = {
    'auto_rickshaw_symmetric_back_1766256507951.png': 'player.png',
    'mumbai_road_texture_1766255895884.png': 'floor.png',
    'mumbai_buildings_texture_1766255911757.png': 'wall.png',
    'indian_barricade_front_view_1766259685112.png': 'obstacle.png',
    'auto_rickshaw_dashboard_pixar_1766257706325.png': 'dashboard.png',
    'speedometer_needle_1766257639560.png': 'needle.png',
    'cartoon_coin_1766257868330.png': 'coin.png'
}

if not os.path.exists(DEST_DIR):
    os.makedirs(DEST_DIR)
    print(f"Created {DEST_DIR}")
else:
    print(f"Assets dir exists: {DEST_DIR}")

for art, dest in FILES.items():
    src = os.path.join(ARTIFACT_DIR, art)
    dst = os.path.join(DEST_DIR, dest)
    
    if os.path.exists(src):
        print(f"Copying {art} -> {dest}")
        try:
            shutil.copy2(src, dst)
            if os.path.exists(dst):
                print("   [OK] Copied successfully.")
            else:
                print("   [FAILED] Copy call finished but file missing.")
        except Exception as e:
            print(f"   [ERROR] Copy failed: {e}")
    else:
        print(f"[MISSING] Source not found: {src}")

print("Installation Complete.")
