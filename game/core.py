from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, AmbientLight, DirectionalLight, Vec4, Vec3
import sys

# from game.player import Player
from game.level_gen import LevelGenerator
# from game.ui_manager import UIManager
# from game.calibration import CalibrationManager
# from vision.gesture_recognizer import GestureRecognizer

class GameCore(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Window properties
        props = WindowProperties()
        props.setTitle("Antigravity Runner V2")
        props.setOrigin(0, 0)
        self.win.requestProperties(props)
        
        # Disable default mouse camera control
        self.disableMouse()
        
        # Camera Setup
        self.camera.setPos(0, -20, 5)
        self.camera.lookAt(0, 0, 0)
        
        # Lighting
        # Lighting (DISABLED)
        # alight = AmbientLight('alight')
        # alight.setColor(Vec4(0.4, 0.4, 0.5, 1)) # Slightly Blue ambient
        # alnp = self.render.attachNewNode(alight)
        # self.render.setLight(alnp)

        # dlight = DirectionalLight('dlight')
        # dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
        # dnp = self.render.attachNewNode(dlight)
        # dnp.setHpr(0, -60, 0)
        # self.render.setLight(dnp)
        
        # Fog (DISABLED)
        # from panda3d.core import Fog
        # self.fog = Fog("SceneFog")
        # self.fog.setColor(0.1, 0.1, 0.15) # Dark Blue/Grey
        # self.fog.setExpDensity(0.01)
        # self.render.setFog(self.fog)
        # self.setBackgroundColor(0.1, 0.1, 0.15)
        
        # Placeholder Environment (DISABLED)
        # self.environ = self.loader.loadModel("models/environment")
        # self.environ.reparentTo(self.render)
        # self.environ.setScale(0.25, 0.25, 0.25)
        # self.environ.setPos(-8, 42, 0)
        
        # Subsystems (DISABLED)
        # self.ui = UIManager()
        # self.player = Player(self.render, self.loader)
        
        # ONLY LEVEL GEN (The one thing we are testing)
        self.level_gen = LevelGenerator(self.render, self.loader)
        
        # Setup initial segment
        self.level_gen.spawn_segment()
        
        # State Management
        self.state = "PLAYING" # START, CALIBRATING, PLAYING, GAMEOVER
        
        # Helper for gesture logic sharing (DISABLED)
        # self.recognizer_for_calib = GestureRecognizer() # Helper copy or we need the main one?
        # Ideally we use the one from vision thread, but we can't share obj easily.
        # CalibrationManager needs to call recognizer.calibrate().
        # We can create a local recognizer just for holding calibration state/logic if needed,
        # but calibration actually happens in the vision thread usually?
        # Wait, the recognizer in vision thread holds 'neutral_x'.
        # If we calibrate in GameCore, we are not affecting the VisionThread's recognizer!
        
        # CRITICAL FIX: Calibration must run in Vision Thread or we must share state.
        # Option A: Move Calibration Logic to Vision Thread.
        # Option B: Pass 'calibrate' command to Vision Thread.
        
        # Let's go with Option A: GestureRecognizer handles calibration.
        # CalibrationManager in GameCore just displays UI based on state passed from Vision?
        # Or...
        
        # Simpler: GameCore has CalibrationManager.
        # update() calls calibration_mgr.update(landmarks, actions).
        # calibration_mgr.update() calls recognizer.calibrate()? 
        # But recognizer is not here.
        
        # Re-think: The Vision Thread does recognition (Left/Right/Jump).
        # It needs 'neutral' values. 
        # So Vision Thread MUST own Calibration.
        
        # OK, change plan:
        # main.py Vision Thread handles "Calibration Mode".
        # It passes 'calibration_status' to GameCore.
        # GameCore just shows UI.
        
        self.score = 0
        self.calib_msg = "Waiting for Vision..."
        self.input_state = {}
        self.raw_landmarks = {}

        # Update Task (DISABLED - STATC SCENE)
        # self.taskMgr.add(self.update, "UpdateTask")
        print("Game Core Initialized (MINIMAL DEBUG MODE)")



    def on_key(self, action, value):
        self.input_state[action] = value

    def skip_calibration(self):
        if self.state == "CALIBRATING":
            self.state = "PLAYING"
            self.ui.show_message("Debug Skip!", 1)

    def set_vision_data(self, actions, msg, is_calibrated):
        # Merge vision actions with keyboard actions (priority to vision if active)
        # Actually simpler to just update keys that are present
        for k, v in actions.items():
            if v: 
                self.input_state[k] = v
        
        self.calib_msg = msg
        if is_calibrated and self.state == "CALIBRATING":
            # Transition only if we are in calibration
            self.state = "PLAYING"
            self.ui.show_message("GO!", 1)

    def update(self, task):
        dt = globalClock.getDt()
        
        if self.state == "CALIBRATING":
            self.ui.show_message(self.calib_msg)
                    
        elif self.state == "PLAYING":
            # Update Components
            self.player.update(dt, self.input_state)
            self.level_gen.update(self.player.get_pos())
            self.score += self.player.speed * dt * 0.1
            self.ui.update_score(self.score)
            self.ui.hide_message()
            
            # Debug Feedback
            active_actions = [k.upper() for k, v in self.input_state.items() if v]
            if active_actions:
                self.ui.update_debug(f"Action: {', '.join(active_actions)}")
            else:
                self.ui.update_debug("")

            # Collision
            if self.player.check_collision(self.level_gen.get_obstacles()):
                self.state = "GAMEOVER"
                self.ui.show_message("GAME OVER\nJump to Retry")
            
            # Camera Follow
            player_pos = self.player.get_pos()
            target_cam_pos = player_pos + Vec3(0, -10, 3)
            # Smooth camera follow
            current_cam_pos = self.camera.getPos()
            self.camera.setPos(current_cam_pos + (target_cam_pos - current_cam_pos) * 5 * dt)
            self.camera.lookAt(player_pos)
            
        elif self.state == "GAMEOVER":
            if self.input_state.get('jump', False):
                self.reset_game()
                
        return task.cont

    def reset_game(self):
        self.state = "PLAYING"
        self.score = 0
        self.player.node.setPos(0,0,1)
        self.player.vertical_velocity = 0
        self.player.lane = 0
        # Reset Level? LevelGen needs reset method or just move player back?
        # Moving player back is tricky with infinite gen.
        # easier to despawn all and reset.
        self.level_gen.cleanup_obstacles(999999) # force clean
        self.level_gen.next_spawn_y = 0
        self.player.node.setPos(0,0,1)
        self.camera.setPos(0, -20, 5)

if __name__ == "__main__":
    game = GameCore()
    game.run()
