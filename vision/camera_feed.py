import cv2
import threading
import time

class CameraFeed:
    def __init__(self, src=0, width=1280, height=720):
        self.width = width
        self.height = height
        self.src = src
        # Use DirectShow on Windows to avoid MSMF errors (Error -1072875772)
        if hasattr(cv2, 'CAP_DSHOW'):
            self.cap = cv2.VideoCapture(self.src, cv2.CAP_DSHOW)
        else:
            self.cap = cv2.VideoCapture(self.src)
            
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.read_lock = threading.Lock()

    def start(self):
        if self.started:
            print("Camera already started")
            return None
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        # Continue reading frames from the camera in a loop
        while self.started:
            grabbed, frame = self.cap.read()
            with self.read_lock:
                # Safely update the shared frame object using a thread lock
                self.grabbed = grabbed
                self.frame = frame
            time.sleep(0.01) # Small sleep to prevent high CPU usage

    def read(self):
        # Safely retrieve the latest captured frame
        with self.read_lock:
            if not self.grabbed:
                return None
            frame = self.frame.copy()
        return frame

    def stop(self):
        self.started = False
        if self.thread.is_alive():
            self.thread.join()
        self.cap.release()

if __name__ == "__main__":
    cam = CameraFeed().start()
    while True:
        frame = cam.read()
        if frame is not None:
            cv2.imshow("Camera", frame)
            if cv2.waitKey(1) == ord('q'):
                break
    cam.stop()
    cv2.destroyAllWindows()
