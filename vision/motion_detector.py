import cv2
import numpy as np

class MotionDetector:
    def __init__(self):
        self.prev_frame = None
        self.min_area = 500 # Minimum movement area to register
        self.frame_width = 0
        self.center_zone_width = 0.15 # Reduced from 0.3 for higher sensitivity
        
        # State
        self.action = "CENTER"
        self.centroid = None

    def process(self, frame):
        # 1. Resize and apply Grayscale/Blur to reduce noise
        small_frame = cv2.resize(frame, (320, 240))
        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        self.frame_width = small_frame.shape[1]
        
        if self.prev_frame is None:
            # Initialize the previous frame on the first run
            self.prev_frame = gray
            return "CENTER", small_frame
            
        delta = cv2.absdiff(self.prev_frame, gray)
        thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # 3. Find Contours (Movement Blobs)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        largest_area = 0
        largest_rect = None
        
        for c in contours:
            if cv2.contourArea(c) < self.min_area:
                continue
            
            # Find largest moving object
            if cv2.contourArea(c) > largest_area:
                largest_area = cv2.contourArea(c)
                largest_rect = cv2.boundingRect(c)
        
        # 4. Determine Action
        self.action = "CENTER"
        self.centroid = None
        
        debug_frame = small_frame.copy()
        
        if largest_rect:
            (x, y, w, h) = largest_rect
            cx = x + w // 2
            cy = y + h // 2
            self.centroid = (cx, cy)
            
            # Draw box
            cv2.rectangle(debug_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(debug_frame, (cx, cy), 5, (0, 0, 255), -1)
            
            # Logic: Left / Right based on screen zones
            # Frame is 240px high. Width is 320px.
            
            w_total = self.frame_width
            zone_margin = w_total * ((1.0 - self.center_zone_width) / 2.0)
            
            left_threshold = zone_margin
            right_threshold = w_total - zone_margin
            
            # Draw Zones
            cv2.line(debug_frame, (int(left_threshold), 0), (int(left_threshold), 240), (255, 0, 0), 1)
            cv2.line(debug_frame, (int(right_threshold), 0), (int(right_threshold), 240), (255, 0, 0), 1)
            
            # Jump Threshold (Top 40% of screen)
            # If the user jumps, their motion centroid moves UP.
            jump_threshold = 240 * 0.4 
            cv2.line(debug_frame, (0, int(jump_threshold)), (320, int(jump_threshold)), (0, 255, 255), 1)
            
            if cy < jump_threshold:
                 # Movement detected in the top portion of the screen
                 self.action = "JUMP"
            elif cx < left_threshold:
                # Movement detected in the left zone (mirrored to RIGHT action)
                self.action = "RIGHT" # Camera is mirrored
            elif cx > right_threshold:
                # Movement detected in the right zone (mirrored to LEFT action)
                self.action = "LEFT"
            else:
                self.action = "CENTER"
            
        self.prev_frame = gray
        return self.action, debug_frame
