from ursina import *
import ursina
import time as sys_time

class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.model = 'quad' 
        self.texture = 'assets/player.png'
        self.scale = (2, 2, 1) 
        self.position = (0, 1, 0)
        
        self.collider = BoxCollider(self, center=(0,0,0), size=(0.8, 0.8, 0.5))
        self.billboard = True 

        self.shadow = Entity(
            parent=self,
            model='circle',
            color=color.rgba(0, 0, 0, 0.4),
            scale=(0.8, 0.5, 1),
            position=(0, -0.45, 0),
            rotation_x=90
        )

        self.speed = 20
        self.target_lane = 0 
        self.velocity_y = 0
        self.jumping = False
        self.vision_bridge = kwargs.get('vision_bridge')
        self.last_switch_time = 0
        
        self.score = 0
        self.visible = False
        
        self.game_over = False
        self.game_over_text = None
        self.ignore_paused = True 

    def update(self):
        # 1. Game Over
        if self.game_over:
            # Allow restarting with 'R' key when game is over
            if held_keys['r']:
                self.restart()
            return 

        # 2. Forward Movement
        # Explicitly use ursina.time to avoid confusion
        self.z += self.speed * ursina.time.dt
        
        # 3. Physics
        hit_info = self.intersects()
        grounded = False
        
        if self.y > 1:
            self.velocity_y -= 50 * ursina.time.dt
            grounded = False
        else:
            grounded = True
            
        # Handle falling and landing
        self.y += self.velocity_y * ursina.time.dt
        if self.y < 1:
            self.y = 1
            self.velocity_y = 0
            self.jumping = False

        # 4. Vision Input
        action = None
        if self.vision_bridge:
            action = self.vision_bridge.get_action()

        curr = sys_time.time()
        
        # Lane Cooldown
        if curr - self.last_switch_time > 0.4: 
            moved = False
            if action == "LEFT" and self.target_lane > -1:
                self.target_lane -= 1
                moved = True
            elif action == "RIGHT" and self.target_lane < 1:
                self.target_lane += 1
                moved = True
                
            if not moved:
                if held_keys['left arrow'] and self.target_lane > -1:
                    self.target_lane -= 1
                    moved = True
                elif held_keys['right arrow'] and self.target_lane < 1:
                    self.target_lane += 1
                    moved = True
            
            if moved:
                self.last_switch_time = curr
        
        if (action == "JUMP" or held_keys['up arrow']) and not self.jumping and grounded:
            self.jump()

        # 5. Lane Movement
        # Interpolate player's X position for smooth lane switching
        target_x = self.target_lane * 2
        self.x = lerp(self.x, target_x, ursina.time.dt * 10)
        
        # Keep camera locked to player position
        camera.position = (self.x, self.y + 1.2, self.z)
        
        # 6. Collision Logic: Check for hits and react accordingly
        if hit_info.hit:
            if hasattr(hit_info.entity, 'tag'):
                if hit_info.entity.tag == 'obstacle':
                    self.trigger_game_over()
                elif hit_info.entity.tag == 'coin':
                    self.score += 1
                    self.speed += 1.0 # Boost speed by 1.0 per coin
                    destroy(hit_info.entity) 
                    
        # Speed Increase
        # Use application.time_scale to check for pause
        if not self.game_over and application.time_scale > 0:
             # Gradually increase speed over time for progressive difficulty
             self.speed += 0.1 * ursina.time.dt

    def jump(self):
        self.velocity_y = 15
        self.jumping = True

    def trigger_game_over(self):
        print("Collision! Game Over.")
        self.game_over = True
        application.time_scale = 0 
        
        if not self.game_over_text:
            self.game_over_text = Text(
                text=f"GAME OVER\nScore: {self.score}\nPress 'R' to Restart",
                origin=(0, 0),
                scale=3,
                color=color.red,
                background=True
            )

    def restart(self):
        print("Restarting...")
        self.game_over = False
        application.time_scale = 1
        
        self.z += 5 
        self.target_lane = 0
        self.x = 0
        self.y = 1
        self.velocity_y = 0
        self.score = 0 
        self.speed = 20 
        
        if self.game_over_text:
            destroy(self.game_over_text)
            self.game_over_text = None
