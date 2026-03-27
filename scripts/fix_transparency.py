from PIL import Image
import os
import numpy as np

def remove_white_bg(filepath, tolerance=60): # Increased tolerance
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    print(f"Processing {filepath}...")
    try:
        img = Image.open(filepath).convert("RGBA")
        datas = img.getdata()

        new_data = []
        for item in datas:
            # Check if pixel is white-ish
            # item is (r, g, b, a)
            # Check for very light gray/white (shadows)
            if item[0] > 255 - tolerance and item[1] > 255 - tolerance and item[2] > 255 - tolerance:
                new_data.append((255, 255, 255, 0)) # Transparent
            else:
                new_data.append(item)

        img.putdata(new_data)
        img.save(filepath, "PNG")
        print(f"Saved transparency to {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

assets_dir = r"c:\Users\nasan\OneDrive\Desktop\game\assets"
remove_white_bg(os.path.join(assets_dir, "player.png"))
remove_white_bg(os.path.join(assets_dir, "obstacle.png"))
