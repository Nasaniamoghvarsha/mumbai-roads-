from PIL import Image, ImageDraw
import os

def flood_fill_transparent(img, x, y, tolerance=40):
    try:
        from skimage.segmentation import flood_fill
    except ImportError:
        # Fallback to simple BFS if skimage not installed
        # Or better: "ImageDraw.floodfill" is not for transparency directly on some versions
        # Let's use a robust BFS implementation here
        pass

    # Simple BFS for flood fill transparency interactively
    pixels = img.load()
    width, height = img.size
    target_color = pixels[x, y]
    
    # If target is already translucent, skip
    if len(target_color) == 4 and target_color[3] < 10:
        return img

    queue = [(x, y)]
    visited = set([(x, y)])
    
    # Tolerance checker
    def match(c1, c2):
        return abs(c1[0]-c2[0]) < tolerance and abs(c1[1]-c2[1]) < tolerance and abs(c1[2]-c2[2]) < tolerance

    while queue:
        cx, cy = queue.pop(0)
        pixels[cx, cy] = (0, 0, 0, 0) # Clear pixel

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in visited:
                    if match(pixels[nx, ny], target_color):
                        visited.add((nx, ny))
                        queue.append((nx, ny))
    return img

def process_image(filename, mode='simple'):
    path = os.path.join(r"c:\Users\nasan\OneDrive\Desktop\game\assets", filename)
    if not os.path.exists(path):
        print(f"Missing {filename}")
        return

    print(f"Processing {filename}...")
    img = Image.open(path).convert("RGBA")
    
    if mode == 'dashboard':
        # 1. Aggressive Center Punch (Windshield is usually here)
        center_x = img.width // 2
        center_y = int(img.height * 0.35) # Usually upper 1/3
        print(f"Punching hole at {center_x}, {center_y}")
        # Reduced tolerance to avoid eating into the beige dashboard
        img = flood_fill_transparent(img, center_x, center_y, tolerance=40)
        
        # 2. Also clear top corners (Sky)
        img = flood_fill_transparent(img, 10, 10, tolerance=50)
        img = flood_fill_transparent(img, img.width-10, 10, tolerance=50)
        
    elif mode == 'simple':
        # Replace all white
        datas = img.getdata()
        new_data = []
        for item in datas:
            if item[0] > 220 and item[1] > 220 and item[2] > 220:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        img.putdata(new_data)
        
    img.save(path)
    print(f"Saved {filename}")

# Run
process_image('dashboard.png', mode='dashboard') # Use smart center-punch
process_image('needle.png', mode='simple')
process_image('coin.png', mode='simple')
process_image('obstacle.png', mode='simple')
