import time

class CalibrationManager:
    def __init__(self, recognizer):
        self.recognizer = recognizer
        self.state = "START" # START, CALIBRATING, DONE
        self.steps = ["STAND_STILL", "WAVE_TO_START"]
        self.current_step_idx = 0
        self.msg = "Welcome! Stand back to start."
        self.timer = 0
        self.needed_time = 2.0 # Seconds to hold pose
        self.hold_start = None

    def update(self, landmarks, actions):
        if self.state == "DONE":
            return True

        if self.state == "START":
            self.msg = "Stand still to Calibrate."
            # Check if user is visible (landmarks present)
            if landmarks:
                 # Auto-calibrate neutral after 2 seconds of stability?
                 # For now, just instant calibrate if visible
                 if self.recognizer.calibrate(landmarks):
                     self.state = "TUTORIAL"
                     self.current_step_idx = 1 # Skip STAND_STILL
                     self.msg = "Calibration Done!"
                     time.sleep(1)
            else:
                self.msg = "Please stand in front of camera."

        elif self.state == "TUTORIAL":
            step = self.steps[self.current_step_idx]
            
            if step == "WAVE_TO_START":
                self.msg = "RAISE ONE HAND (Say Hi) to Start!"
                if actions.get("hi"):
                    self.next_step()
                    
        return False # Not done yet

    def next_step(self):
        self.current_step_idx += 1
        if self.current_step_idx >= len(self.steps):
            self.state = "DONE"
            self.msg = "TUTORIAL COMPLETE! GAME STARTING..."
        else:
            # Small delay or feedback?
            pass

    def get_message(self):
        return self.msg
