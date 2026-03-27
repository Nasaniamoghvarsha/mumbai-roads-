from panda3d.core import Texture, NodePath, PNMImage

class AssetManager:
    def __init__(self, loader):
        self.loader = loader
        
    def load_texture(self, name, path):
        print(f"[AssetManager] Loading: {name} -> {path}")
        try:
            tex = self.loader.loadTexture(path)
        except Exception as e:
            print(f"CRITICAL ERROR: Could not load texture {path}")
            raise e
            
        # MATCHING DEBUG SCRIPT: Use simple settings
        tex.setWrapU(Texture.WMClamp)
        tex.setWrapV(Texture.WMClamp)
        
        # Use simple Bilinear filtering (No Mipmaps) to avoid artifacts
        tex.setMinfilter(Texture.FTLinear)
        tex.setMagfilter(Texture.FTLinear)
        
        return tex
        
    def create_procedural_texture(self, name, type_key):
        # Generate 512x512 textures in memory to guarantee correctness
        size = 512
        img = PNMImage(size, size)
        
        if type_key == "floor":
            # Grey stone tiles
            img.fill(0.3, 0.3, 0.3) # Base grey
            # Draw grid lines
            for x in range(size):
                for y in range(size):
                    # Grid every 64 pixels
                    if x % 64 < 4 or y % 64 < 4:
                        img.setXel(x, y, 0.1, 0.1, 0.1) # Dark grout
                    else:
                        # Add some noise/variation
                        noise = (x * y * 1321) % 100 / 1000.0
                        img.setXel(x, y, 0.3 + noise, 0.3 + noise, 0.33 + noise)
                        
        elif type_key == "wall":
            # Orange Bricks
            img.fill(0.8, 0.4, 0.1) # brick orange
            # Brick pattern: Rows every 64px
            for y in range(size):
                row = y // 64
                offset = 0 if row % 2 == 0 else 32
                for x in range(size):
                    if y % 64 < 6: # Horizontal mortar
                         img.setXel(x, y, 0.7, 0.7, 0.7)
                    elif ((x + offset) % 128) < 6: # Vertical mortar
                         img.setXel(x, y, 0.7, 0.7, 0.7)
                         
        elif type_key == "crate":
            # Wood with Red X
            img.fill(0.6, 0.4, 0.2) # Wood brown
            # Board lines
            for y in range(size):
                if y % 64 < 2:
                    for x in range(size):
                        img.setXel(x, y, 0.3, 0.2, 0.1)
            # Red stripes (Diagonal)
            for x in range(size):
                for y in range(size):
                    if abs(x - y) < 40 or abs((size-x) - y) < 40:
                        img.setXel(x, y, 0.8, 0.1, 0.1)
        
        elif type_key == "coin":
            # Gold Circle
            img.fill(0, 0, 0) # Black bg
            img.addAlpha()
            center = size / 2
            for x in range(size):
                for y in range(size):
                    dist = ((x - center)**2 + (y - center)**2)**0.5
                    if dist < 200:
                        img.setXel(x, y, 1.0, 0.8, 0.1) # Gold
                        img.setAlpha(x, y, 1.0)
                    else:
                        img.setAlpha(x, y, 0.0)

        tex = Texture(name)
        tex.load(img)
        tex.setMagfilter(Texture.FTLinear)
        tex.setMinfilter(Texture.FTLinearMipmapLinear)
        tex.setWrapU(Texture.WMRepeat)
        tex.setWrapV(Texture.WMRepeat)
        return tex
        
    def create_floor_segment(self):
         model = self.loader.loadModel("models/box")
         # Re-enable texture loading with simplified JPGs
         tex = self.load_texture("stone", "game/assets/floor.jpg") 
         model.setTexture(tex)
         # Reset color to white so texture shows true colors
         model.setColor(1, 1, 1, 1)
         return model

    def create_wall(self):
        model = self.loader.loadModel("models/box")
        tex = self.load_texture("wall", "game/assets/wall.jpg")
        model.setTexture(tex)
        model.setColor(1, 1, 1, 1)
        return model

    def create_obstacle(self):
        model = self.loader.loadModel("models/box")
        tex = self.load_texture("crate", "game/assets/obstacle.jpg")
        model.setTexture(tex)
        model.setColor(1, 1, 1, 1)
        return model
        
    def create_coin(self):
        model = self.loader.loadModel("models/box")
        tex = self.load_texture("coin", "game/assets/coin.png")
        model.setTexture(tex)
        model.setColor(1, 1, 1, 1)
        model.setTransparency(1) # Enable transparency for coin
        return model
