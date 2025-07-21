#!/usr/bin/env python3
"""
Simple camera test script to verify video capture and face detection
"""

import cv2
import time
from facial_detections import detectFace

def test_camera():
    """Test camera capture and face detection"""
    print("Testing camera and face detection...")
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return False
    
    print("✓ Camera opened successfully")
    
    # Test for a few seconds
    start_time = time.time()
    frame_count = 0
    
    while time.time() - start_time < 5:  # Test for 5 seconds
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame")
            break
        
        frame_count += 1
        
        # Test face detection
        try:
            faceCount, faces = detectFace(frame)
            print(f"Frame {frame_count}: {faceCount} face(s) detected")
        except Exception as e:
            print(f"Error in face detection: {e}")
        
        # Display frame
        cv2.imshow('Camera Test', frame)
        
        # Break on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    print(f"✓ Processed {frame_count} frames")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    return True

if __name__ == "__main__":
    test_camera() 