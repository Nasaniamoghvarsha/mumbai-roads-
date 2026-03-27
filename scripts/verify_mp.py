import mediapipe as mp
print(f"MediaPipe Path: {mp.__file__}")
try:
    print(f"Solutions: {mp.solutions}")
    print("SUCCESS: mp.solutions exists")
except AttributeError:
    print("FAILURE: mp.solutions NOT found")
    print(f"Dir(mp): {dir(mp)}")
    
    # Try solution import
    try:
        import mediapipe.solutions
        print("SUCCESS: 'import mediapipe.solutions' worked!")
        import mediapipe.solutions.pose as mp_pose
        print(f"Pose Module: {mp_pose}")
    except ImportError as e:
        print(f"Solution Import Failed: {e}")
