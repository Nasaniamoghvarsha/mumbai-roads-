
print("Testing: import cv2 -> import torch")
try:
    import cv2
    print("cv2 imported")
    import torch
    print("torch imported")
    from ultralytics import YOLO
    print("ultralytics imported")
except ImportError as e:
    print(f"ImportError: {e}")
except OSError as e:
    print(f"OSError: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")
