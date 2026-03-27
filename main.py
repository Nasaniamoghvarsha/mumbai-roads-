from ursina import *
from game.player import Player
from game.level import LevelGenerator
from game.vision_bridge import VisionBridge
from PIL import Image

# Initialize Ursina app
app = Ursina()

# Set up the window title and hide the default exit button
window.title = "Antigravity Runner V2"
window.borderless = False
window.exit_button.visible = False
window.fps_counter.enabled = True

# Set up basic lighting and atmospheric fog
AmbientLight(color=color.rgba(100, 100, 100, 100))
DirectionalLight(color=color.white, rotation=(45, -45, 45))
Sky()
scene.fog_density = 0.02
scene.fog_color = color.gray

# Initialize and start the vision processing system
vision_bridge = VisionBridge()
vision_bridge.start()

# --- Cockpit UI ---
# Dashboard
dashboard = Entity(
    parent=camera.ui,
    model='quad',
    texture='assets/dashboard.png',
    scale=(2.2, 1.2), 
    position=(0, -0.2), 
    color=color.white,
    z=5 # Background
)

# Helper: Camera HUD (Rear View Mirror Style)
camera_border = Entity(
    parent=camera.ui,
    model='quad',
    scale=(0.52, 0.27),
    position=(0.62, -0.37), 
    color=color.rgba(0, 0, 0, 0.8), 
    z=0 # Middle
)
camera_hud = Entity(
    parent=camera.ui,
    model='quad', 
    scale=(0.5, 0.25), 
    position=(0.62, -0.37), 
    z=-1, # Front
    texture='white_cube' 
)

# Score Text (Digital Style)
score_bg = Entity(parent=camera.ui, model='quad', scale=(0.35, 0.12), position=(-0.58, -0.42), color=color.rgba(0,0,0,0.6), z=0)
score_text = Text(
    text='COINS: 0', 
    position=(-0.58, -0.41), # Centered deeper in screen
    origin=(0, 0),
    scale=2, 
    color=color.gold,
    font='VeraMono.ttf',
    z=-2 # Top Priority
)

# Speed Text (Minimalist)
# speed_bg removed as requested
speed_text = Text(
    text='0 km/h',
    position=(0, -0.28), # Center Bottom (Lowered)
    origin=(0, 0),
    scale=3,
    color=color.white,
    font='VeraMono.ttf',
    z=-2 # Top Layer (Text)
)

# Motion Bar (Top Center)
motion_bar_bg = Entity(parent=camera.ui, model='quad', scale=(0.3, 0.02), position=(0, 0.42), color=color.gray)
motion_bar = Entity(parent=camera.ui, model='quad', scale=(0.02, 0.04), position=(0, 0.42), color=color.green)

# Create the player and level generator
player = Player(vision_bridge=vision_bridge)
level_gen = LevelGenerator(player)

def update():
    # 1. Update Score
    score_text.text = f'Coins: {player.score}'
    
    # 2. Update Speed 
    speed_text.text = f'{int(player.speed)} km/h'
    
    # 3. Cockpit Vibration
    vib_mag = 0.0005 + (player.speed * 0.0001)
    dashboard.x = 0 + random.uniform(-vib_mag, vib_mag)
    dashboard.y = -0.15 + random.uniform(-vib_mag, vib_mag)
    
    # 4. Vision Feedback (Motion Bar)
    centroid = vision_bridge.get_centroid()
    if centroid:
         cx = centroid[0] / 320.0
         # Mirror correction: cx=1 (Left on screen) -> -0.15
         offset = (0.5 - cx) * 0.3
         motion_bar.x = offset

    # 5. Webcam Feed Update
    frame = vision_bridge.get_debug_frame()
    if frame is not None:
        camera_hud.texture = Texture(Image.fromarray(frame))

    # 6. Quit
    if held_keys['escape']:
        vision_bridge.stop()
        application.quit()
    if held_keys['c']:
        vision_bridge.recalibrate()
        
    # 7. Level Generation Update (spawning/cleaning segments)
    level_gen.update()

try:
    app.run()
finally:
    vision_bridge.stop()
