#!/usr/bin/env python3
"""
Cross-platform sound utilities for the AI-based exam proctoring system.
Replaces Windows-specific winsound module.
"""

import platform
import time

def play_beep(frequency=2500, duration=1000):
    """
    Play a beep sound across different platforms.
    
    Args:
        frequency (int): Frequency of the beep in Hz (default: 2500)
        duration (int): Duration of the beep in milliseconds (default: 1000)
    """
    system = platform.system()
    
    try:
        if system == "Windows":
            import winsound
            winsound.Beep(frequency, duration)
        elif system == "Darwin":  # macOS
            import os
            # Use macOS say command to make a beep sound
            os.system(f"afplay /System/Library/Sounds/Ping.aiff")
        elif system == "Linux":
            import os
            # Use Linux beep command if available, otherwise use aplay
            try:
                os.system(f"beep -f {frequency} -l {duration}")
            except:
                # Fallback to aplay if beep is not available
                os.system("aplay /usr/share/sounds/alsa/Front_Left.wav 2>/dev/null || echo -e '\a'")
        else:
            # Fallback for other systems
            print(f"\a")  # ASCII bell character
            time.sleep(duration / 1000.0)
            
    except Exception as e:
        # Fallback if all sound methods fail
        print(f"Sound alert! (Error: {e})")
        time.sleep(duration / 1000.0)

def play_alert():
    """Play a standard alert sound."""
    play_beep(2500, 1000)

def play_warning():
    """Play a warning sound."""
    play_beep(2000, 500)

def play_error():
    """Play an error sound."""
    play_beep(1500, 2000) 