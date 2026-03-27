import sys
print(f"Python: {sys.version}")
try:
    import torch
    print(f"Torch imported: {torch.__version__}")
    from ultralytics import YOLO
    print("Ultralytics imported successfully!")
    model = YOLO("yolov8n-pose.pt")
    print("Model loaded successfully!")
except ImportError as e:
    print(f"ImportError: {e}")
except OSError as e:
    print(f"OSError: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")
