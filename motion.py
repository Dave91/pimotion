import io
import os
import random
import picamera
import datetime as dt

# Mock motion detection randomly
def motion_detected():
    return random.randint(0, 5) == 0

# How many seconds after motion detection to record for
record_post_duration = 10

# How many seconds BEFORE motion detection to record
buffer_duration = 20

# Init camera and stream with 20 second buffer
camera = picamera.PiCamera()
stream = picamera.PiCameraCircularIO(camera, seconds=buffer_duration)

# Setup timestamp annotation
camera.annotate_background = picamera.Color('black')
camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Start recording (preview for debugging)
camera.start_preview()
camera.start_recording(stream, format='h264')

try:
    while True:
        # Update the annotation timestamp every second
        camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        camera.wait_recording(1)

        if motion_detected():
            print("Motion detected at "+dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            
            # Start a thread blocking loop so we can update the timestamp overlay every second
            # This will eventually be changed to keep going until there's no motion in the scene
            for i in range(record_post_duration):
                if(i == record_post_duration - 1):
                    # Got what we need, wrap everything up
                    print("Finished recording...")
                    stream.copy_to('footage/motion_'+dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'.h264')

                    # Exit cleanly for now
                    os._exit(1)
                else:
                    # Update the timestamp overlay
                    print("Updating timestamp "+dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    camera.wait_recording(1)
finally:
    os._exit(1)