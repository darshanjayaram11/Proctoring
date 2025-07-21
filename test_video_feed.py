#!/usr/bin/env python3
"""
Test video feed generation
"""

import cv2
import time
from main import proctoringAlgo

def test_video_feed():
    """Test video feed generation"""
    print("Testing video feed generation...")
    
    # Get the video feed generator
    feed_generator = proctoringAlgo()
    
    # Test a few frames
    frame_count = 0
    start_time = time.time()
    
    try:
        for frame_data in feed_generator:
            frame_count += 1
            print(f"Generated frame {frame_count}")
            
            # Stop after 5 seconds or 10 frames
            if frame_count >= 10 or (time.time() - start_time) > 5:
                break
                
    except Exception as e:
        print(f"Error generating video feed: {e}")
        return False
    
    print(f"✓ Successfully generated {frame_count} frames")
    return True

if __name__ == "__main__":
    test_video_feed() 