from ursina import *
import random

class LevelGenerator(Entity):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.segments = []
        
        # Pre-load textures
        self.tex_floor = load_texture('assets/floor.png')
        self.tex_wall = load_texture('assets/wall.png')
        self.tex_obstacle = load_texture('assets/obstacle.png')
        self.tex_coin = load_texture('assets/coin.png')
        
        self.floor_parent = Entity()
        self.next_z = 0
        self.segment_length = 12 
        
        # Spawn initial track segments to fill the view
        for i in range(10):
            self.spawn_segment(self.next_z)
            self.next_z += self.segment_length

    def update(self):
        # Check if we need to spawn new segments or clean up old ones
        if self.player.z + 100 > self.next_z:
            self.spawn_segment(self.next_z)
            self.next_z += self.segment_length
            
        self.cleanup_segments()

    def spawn_segment(self, z_pos):
        # 1. Floor Segment
        floor = Entity(
            model='cube',
            scale=(12, 1, self.segment_length),
            position=(0, 0, z_pos),
            texture=self.tex_floor,
            texture_scale=(1, 1),
            collider='box',
            parent=self.floor_parent
        )
        self.segments.append(floor)
        
        # 2. Walls
        wall_l = Entity(
            model='cube', 
            scale=(1, 10, self.segment_length), 
            position=(-6.5, 5, z_pos), 
            texture=self.tex_wall, 
            texture_scale=(1, 1), 
            parent=self.floor_parent
        )
        wall_r = Entity(
            model='cube', 
            scale=(1, 10, self.segment_length), 
            position=(6.5, 5, z_pos), 
            texture=self.tex_wall, 
            texture_scale=(1, 1), 
            parent=self.floor_parent
        )
        self.segments.append(wall_l)
        self.segments.append(wall_r)
        
        # 3. Obstacles & Coins
        obstacle_lane = -999
        
        if random.random() < 0.35: 
            obstacle_lane = random.choice([-2, 0, 2])
            obstacle = Entity(
                model='quad',
                texture=self.tex_obstacle,
                scale=(1.8, 1.8, 1),
                position=(obstacle_lane, 0.9, z_pos),
                collider='box',
                parent=self.floor_parent
            )
            obstacle.tag = 'obstacle'
            self.segments.append(obstacle)

        # Coins
        if random.random() < 0.5:
            available_lanes = [l for l in [-2, 0, 2] if l != obstacle_lane]
            if available_lanes:
                coin_lane = random.choice(available_lanes)
                coin = Entity(
                    model='quad',
                    texture=self.tex_coin,
                    scale=(0.8, 0.8, 1),
                    position=(coin_lane, 1.5, z_pos), 
                    collider='box', 
                    parent=self.floor_parent
                )
                coin.tag = 'coin'
                coin.animate_rotation_y(360, duration=2, loop=True)
                self.segments.append(coin)
            
    def cleanup_segments(self):
        # Safely remove segments that are too far behind the player to save memory
        alive_segments = []
        for seg in self.segments:
            try:
                # Keep segments that are still in front or close behind the player
                if seg.enabled and seg.z >= self.player.z - 30:
                    alive_segments.append(seg)
                elif seg.enabled:
                    # Too far behind, destroy the entity
                    destroy(seg)
            except Exception:
                # Entity might have been already destroyed (e.g., collected coin)
                pass
                
        self.segments = alive_segments
