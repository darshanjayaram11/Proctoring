#!/usr/bin/env python3
"""
Detailed face detection test script
"""

import cv2
import dlib
import numpy as np
from imutils import face_utils
import os

def test_face_detection():
    """Test face detection with different methods"""
    print("Testing face detection...")
    
    # Check if model file exists
    model_path = 'shape_predictor_model/shape_predictor_68_face_landmarks.dat'
    if not os.path.exists(model_path):
        print(f"✗ Model file not found: {model_path}")
        return False
    
    print(f"✓ Model file found: {model_path}")
    
    # Test dlib face detector
    try:
        detector = dlib.get_frontal_face_detector()
        print("✓ Dlib face detector loaded")
    except Exception as e:
        print(f"✗ Error loading dlib detector: {e}")
        return False
    
    # Test shape predictor
    try:
        predictor = dlib.shape_predictor(model_path)
        print("✓ Shape predictor loaded")
    except Exception as e:
        print(f"✗ Error loading shape predictor: {e}")
        return False
    
    # Test camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("✗ Could not open camera")
        return False
    
    print("✓ Camera opened")
    
    # Test multiple camera indices
    for camera_index in [0, 1, 2]:
        print(f"\nTesting camera index {camera_index}...")
        cap.release()
        cap = cv2.VideoCapture(camera_index)
        
        if cap.isOpened():
            print(f"✓ Camera {camera_index} opened successfully")
            
            # Read a few frames
            for i in range(10):
                ret, frame = cap.read()
                if ret:
                    # Convert to grayscale
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    
                    # Detect faces with dlib
                    faces = detector(gray, 0)
                    print(f"  Frame {i+1}: {len(faces)} face(s) detected")
                    
                    # Draw rectangles around detected faces
                    for face in faces:
                        x, y, w, h = face.left(), face.top(), face.width(), face.height()
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                    # Display frame
                    cv2.imshow(f'Camera {camera_index}', frame)
                    cv2.waitKey(100)
                else:
                    print(f"  Frame {i+1}: Could not read frame")
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            
            if len(faces) > 0:
                print(f"✓ Face detection working with camera {camera_index}")
                return True
        else:
            print(f"✗ Camera {camera_index} not available")
    
    print("✗ No faces detected with any camera")
    return False

if __name__ == "__main__":
    test_face_detection() 