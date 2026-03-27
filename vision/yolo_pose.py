import cv2
import mediapipe as mp

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        print("MediaPipe Pose Loaded Successfully")

    def detect(self, img):
        # Convert to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img_rgb)
        
        landmarks = {}
        if results.pose_landmarks:
            for i, lm in enumerate(results.pose_landmarks.landmark):
                # MediaPipe returns normalized coordinates (0.0 - 1.0)
                landmarks[i] = {
                    'x': lm.x,
                    'y': lm.y,
                    'visibility': lm.visibility
                }
        return landmarks

