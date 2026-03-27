from panda3d.core import NodePath, TextureStage, Texture
import random

class LevelGenerator:
    def __init__(self, parent_node, loader):
        self.parent = parent_node
        self.loader = loader
        from game.assets import AssetManager
        self.asset_manager = AssetManager(loader)
        
        self.obstacles = []
        self.segments = []
        
        self.segment_length = 50.0
        self.next_spawn_y = -20.0
        
        # Texture Stage for UV Scaling
        self.ts = TextureStage.getDefault()
        
        # PRE-LOAD TEXTURES (Prevent GC/Reload issues)
        print("LevelGenerator: Pre-loading textures...")
        
        # Floor
        self.tex_floor = self.loader.loadTexture("game/assets/floor.jpg")
        self.tex_floor.setWrapU(Texture.WMClamp)
        self.tex_floor.setWrapV(Texture.WMClamp)
        self.tex_floor.setMinfilter(Texture.FTLinear)
        self.tex_floor.setMagfilter(Texture.FTLinear)
        
        # Wall
        self.tex_wall = self.loader.loadTexture("game/assets/wall.jpg")
        self.tex_wall.setWrapU(Texture.WMClamp)
        self.tex_wall.setWrapV(Texture.WMClamp)
        self.tex_wall.setMinfilter(Texture.FTLinear)
        self.tex_wall.setMagfilter(Texture.FTLinear)

    def update(self, player_pos):
        # Spawn new segments ahead
        while self.next_spawn_y < player_pos.y + 200:
            self.spawn_segment()
            
        # Despawn old segments
        cleanup_threshold = player_pos.y - 50
        active_segments = []
        for seg in self.segments:
            if seg.getY() < cleanup_threshold:
                seg.removeNode()
            else:
                active_segments.append(seg)
        self.segments = active_segments

    def spawn_segment(self):
        # DIRECT DEBUG LOADING (Using Cached Textures)
        
        # 1. Floor
        seg = self.loader.loadModel("models/box")
        seg.reparentTo(self.parent)
        seg.setScale(10, self.segment_length, 0.1) 
        seg.setPos(0, self.next_spawn_y + self.segment_length/2, -0.1) 
        
        # Use Cached Floor Texture
        seg.setTexture(self.tex_floor)
        seg.setColor(1, 1, 1, 1)
        
        # UV Scale 1x1
        seg.setTexScale(self.ts, 1, 1)
        
        # 2. Walls
        
        # Left
        wall_l = self.loader.loadModel("models/box")
        wall_l.reparentTo(seg)
        wall_l.setScale(0.1, 1, 100) 
        wall_l.setPos(-0.55, 0, 50) 
        wall_l.setTexture(self.tex_wall)
        wall_l.setColor(1, 1, 1, 1)
        wall_l.setTexScale(self.ts, 1, 1)
        
        # Right
        wall_r = self.loader.loadModel("models/box")
        wall_r.reparentTo(seg)
        wall_r.setScale(0.1, 1, 100)
        wall_r.setPos(0.55, 0, 50)
        wall_r.setTexture(self.tex_wall)
        wall_r.setColor(1, 1, 1, 1)
        wall_r.setTexScale(self.ts, 1, 1)

        # 3. Ceiling
        ceil = self.loader.loadModel("models/box")
        ceil.reparentTo(seg)
        ceil.setPos(0, 0, 100) 
        ceil.setTexture(self.tex_floor)
        ceil.setColor(1, 1, 1, 1)
        ceil.setTexScale(self.ts, 1, 1)
        
        self.segments.append(seg)
        
        # 4. Obstacles (Disabled for now)

        self.next_spawn_y += self.segment_length

    def get_obstacles(self):
        return self.obstacles
        
    def cleanup_obstacles(self, player_y):
        pass # Parenting handles cleanup
