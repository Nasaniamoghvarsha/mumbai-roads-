print("Testing: import panda3d -> import torch")
try:
    from direct.showbase.ShowBase import ShowBase
    print("Panda3D ShowBase imported")
    import torch
    print("Torch imported")
    from ultralytics import YOLO
    print("Ultralytics imported")
except ImportError as e:
    print(f"ImportError: {e}")
except OSError as e:
    print(f"OSError: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")
