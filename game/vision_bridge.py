import threading
import time
from vision.motion_detector import MotionDetector
from vision.camera_feed import CameraFeed
import cv2

class VisionBridge:
    def __init__(self):
        self.detector = MotionDetector()
        self.feed = CameraFeed()
        
        self.running = False
        self.latest_action = "CENTER"
        self.thread = None
        self.processed_frame = None
        
    def start(self):
        # Initialize and start the camera feed and the background processing thread
        self.running = True
        self.feed.start()
        self.thread = threading.Thread(target=self._update_loop, daemon=True)
        self.thread.start()
        print("VisionBridge: Thread Started (Motion Mode)")
        
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        self.feed.stop()
            
    def _update_loop(self):
        # Continuous loop for vision processing, runs in a separate thread to avoid blocking the game
        while self.running:
            frame = self.feed.read()
            if frame is None:
                time.sleep(0.01)
                continue
                
            # Perform motion detection inference on the captured frame
            action, debug_frame = self.detector.process(frame)
            self.latest_action = action
            
            # Convert the debug frame to RGB for Ursina and mirror it for a natural display
            rgb_frame = cv2.cvtColor(debug_frame, cv2.COLOR_BGR2RGB)
            self.processed_frame = cv2.flip(rgb_frame, 1) # Mirror for UI feedback
            
            time.sleep(0.01)
            
    def get_action(self):
        return self.latest_action
        
    def get_debug_frame(self):
        if self.processed_frame is not None:
            return self.processed_frame
        return None
        
    def get_centroid(self):
        if hasattr(self.detector, 'centroid'):
            return self.detector.centroid
        return None
        
    def recalibrate(self):
        # Motion detector is stateless/auto-resetting, but we could reset history
        self.detector.prev_frame = None
        print("VisionBridge: Motion Detector Reset")

