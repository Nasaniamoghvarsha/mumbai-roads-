from ursina import *
from game.player import Player
from game.level import LevelGenerator
import cv2
print("OpenCV Imported Successfully")

app = Ursina()

# Window Setup
window.title = "Antigravity Runner V2 (Vision Probe)"
window.borderless = False
window.exit_button.visible = False
window.fps_counter.enabled = True

# Lighting
AmbientLight(color=color.rgba(100, 100, 100, 100))
DirectionalLight(color=color.white, rotation=(45, -45, 45))

# Game Objects
player = Player()
level_gen = LevelGenerator(player)

# Simple Quit
def update():
    if held_keys['escape']:
        application.quit()

app.run()
