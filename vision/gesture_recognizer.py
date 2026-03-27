import numpy as np

class GestureRecognizer:
    def __init__(self):
        self.state = {
            "jump": False,
            "slide": False,
            "left": False,
            "right": False,
            "antigravity": False,
            "hi": False
        }
        self.neutral_x = None
        self.calibrated = False
        self.debug_info = {} 
        self.prev_landmarks = {} # For smoothing
        self.alpha = 0.5 # Smoothing factor (0.5 = 50% new, 50% old)

    def calibrate(self, landmarks):
        if not landmarks:
            return False
        # Assume player is standing still in center
        try:
            if 23 in landmarks: # MP
                 l_hip = landmarks[23]
                 r_hip = landmarks[24]
            else: # YOLO
                 l_hip = landmarks[11]
                 r_hip = landmarks[12]
        except KeyError:
             print("Calibration Failed: Missing Keypoints")
             return False

        self.neutral_x = (l_hip['x'] + r_hip['x']) / 2
        self.neutral_y = (l_hip['y'] + r_hip['y']) / 2
        self.calibrated = True
        print(f"Calibrated Neutral X: {self.neutral_x}, Y: {self.neutral_y}")
        return True

    def process(self, landmarks):
        if not landmarks:
            return self.state
            
        # Smooth landmarks
        smoothed = {}
        for k, v in landmarks.items():
            if k in self.prev_landmarks:
                smoothed[k] = {
                    'x': self.prev_landmarks[k]['x'] * (1 - self.alpha) + v['x'] * self.alpha,
                    'y': self.prev_landmarks[k]['y'] * (1 - self.alpha) + v['y'] * self.alpha,
                    'visibility': v['visibility']
                }
            else:
                smoothed[k] = v
        
        self.prev_landmarks = smoothed
        landmarks = smoothed # Use smoothed for calculations
        
        if not self.calibrated:
            return self.state

        # Reset transient states
        self.state["jump"] = False
        self.state["slide"] = False
        self.state["left"] = False
        self.state["right"] = False
        
        # Mapping for YOLO (COCO) vs MediaPipe
        # We'll use local variables for clarity
        try:
            # Check if using MP (id 23 exists) or YOLO (id 11=Hip)
            if 23 in landmarks: # MediaPipe
                nose = landmarks[0]
                l_shoulder = landmarks[11]
                r_shoulder = landmarks[12]
                l_hip = landmarks[23]
                r_hip = landmarks[24]
                l_wrist = landmarks[15]
                r_wrist = landmarks[16]
            else: # YOLO (COCO)
                nose = landmarks[0]
                l_shoulder = landmarks[5]
                r_shoulder = landmarks[6]
                l_hip = landmarks[11]
                r_hip = landmarks[12]
                l_wrist = landmarks[9]
                r_wrist = landmarks[10]
        except KeyError:
             # Missing keypoints
             return self.state

        # 1. Lateral Movement
        current_hip_center_x = (l_hip['x'] + r_hip['x']) / 2
        diff_x = current_hip_center_x - self.neutral_x
        
        shoulder_width = abs(l_shoulder['x'] - r_shoulder['x'])
        relative_diff = diff_x / (shoulder_width + 1e-6)

        if relative_diff < -0.15: # Moved Left (Easier)
            self.state["left"] = True
        elif relative_diff > 0.15: # Moved Right (Easier)
            self.state["right"] = True
            
        # 2. Jump & Slide (Vertical Movement)
        # We need neutral_y for this.
        # Heuristic: If hips move UP by > 10% of screen height (or relative to body size) -> Jump
        # If hips move DOWN -> Slide
        
        current_hip_y = (l_hip['y'] + r_hip['y']) / 2
        
        if self.neutral_y:
            # Normalized diff (assuming y is standard pixel or normalized)
            # If pixels, we need a scale. Let's use shoulder_width as a scale unit if possible.
            # But shoulder width varies with turn. Height is better.
            # Let's use raw pixel difference threshold for now or relative to calibration.
            
            diff_y = current_hip_y - self.neutral_y
            # Note: Y increases downwards.
            # Jump: current < neutral (negative diff)
            # Slide: current > neutral (positive diff)
            
            # Threshold: 20% of calibration hip-to-shoulder distance?
            # Let's use a fixed relative check vs shoulder width (approx body scale)
            
            thresh = shoulder_width * 0.15 # Reduced from 0.3 to 0.15 for better responsiveness
            
            # Save for visualization
            self.debug_info['neutral_y'] = self.neutral_y
            self.debug_info['current_y'] = current_hip_y
            self.debug_info['thresh'] = thresh
            self.debug_info['neutral_x'] = self.neutral_x
            self.debug_info['current_x'] = current_hip_center_x

            if diff_y < -thresh:
                self.state["jump"] = True
            elif diff_y > thresh:
                 self.state["slide"] = True

        # 4. Antigravity (Hands above head)
        # 4. Antigravity (Hands above head)
        # In image coords, Y=0 is top. So lower Y means higher up.
        hands_up_l = l_wrist['y'] < nose['y']
        hands_up_r = r_wrist['y'] < nose['y']
        
        if hands_up_l and hands_up_r:
             self.state["antigravity"] = True
             self.state["hi"] = False 
        else:
             self.state["antigravity"] = False
             # Check for "Hi" (One hand up)
             if hands_up_l or hands_up_r:
                 self.state["hi"] = True
             else:
                 self.state["hi"] = False

        return self.state
