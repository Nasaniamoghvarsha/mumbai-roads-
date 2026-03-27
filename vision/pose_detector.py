import cv2
import numpy as np

try:
    import mediapipe as mp
    HAS_MEDIAPIPE = True
except ImportError:
    print("Warning: MediaPipe not found. Vision features will be disabled.")
    HAS_MEDIAPIPE = False

class PoseDetector:
    def __init__(self, mode=False, complexity=1, smooth=True, segmentation=False, detection_con=0.5, track_con=0.5):
        self.results = None
        self.landmarks = {}
        
        if HAS_MEDIAPIPE:
            self.mp_drawing = mp.solutions.drawing_utils
            self.mp_pose = mp.solutions.pose
            
            self.pose = self.mp_pose.Pose(
                static_image_mode=mode,
                model_complexity=complexity,
                smooth_landmarks=smooth,
                enable_segmentation=segmentation,
                min_detection_confidence=detection_con,
                min_tracking_confidence=track_con
            )
        else:
            self.pose = None

    def find_pose(self, img, draw=True):
        if not HAS_MEDIAPIPE:
            return img
            
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img_rgb)
        
        if self.results.pose_landmarks and draw:
            self.mp_drawing.draw_landmarks(
                img, 
                self.results.pose_landmarks, 
                self.mp_pose.POSE_CONNECTIONS
            )
        return img

    def get_position(self, img):
        self.landmarks = {}
        if not HAS_MEDIAPIPE:
            return self.landmarks
            
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.landmarks[id] = {'id': id, 'x': cx, 'y': cy, 'vis': lm.visibility, 'raw_x': lm.x, 'raw_y': lm.y, 'z': lm.z}
        return self.landmarks

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    detector = PoseDetector()
    while True:
        success, img = cap.read()
        if not success:
            break
        
        img = detector.find_pose(img)
        lm_list = detector.get_position(img)
        
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
