#Written by Yousef Shaykholeslam
#18/3/2024
import sensor
import image
import time
import lcd

# Initialize the camera sensor
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(True)

lcd.rotation(1)

clock = time.clock()

# Define color thresholds in LAB color
white_threshold = (70, 100, -20, 20, -20, 20)
orange_threshold = (53, 99, -9, 80, 11, 70)
purple_threshold = (20, 60, 5, 40, -40, -10)

# Variables to store the detected blobs
orange_blobs = []
white_blobs = []
purple_blobs = []

while True:
    start_time = time.ticks_ms()  # Record the start time for each frame

    img = sensor.snapshot()

    # Find blobs for each color
    orange_blobs = img.find_blobs([orange_threshold], pixels_threshold=200, area_threshold=200, merge=True)
    white_blobs = img.find_blobs([white_threshold], pixels_threshold=200, area_threshold=200, merge=True)
    purple_blobs = img.find_blobs([purple_threshold], pixels_threshold=200, area_threshold=200, merge=True)

    # Draw rectangles around detected blobs and label them
    for blob in orange_blobs:
        img.draw_rectangle(blob.rect(), color=(0, 0, 0))
        img.draw_cross(blob.cx(), blob.cy(), color=(0, 0, 0))
        img.draw_string(blob.x(), blob.y(), "orange", color=(0, 0, 0), scale=2)

    for blob in white_blobs:
        img.draw_rectangle(blob.rect(), color=(0, 0, 0))
        img.draw_cross(blob.cx(), blob.cy(), color=(0, 0, 0))
        img.draw_string(blob.x(), blob.y(), "white", color=(0, 0, 0), scale=2)

    for blob in purple_blobs:
        img.draw_rectangle(blob.rect(), color=(0, 0, 0))
        img.draw_cross(blob.cx(), blob.cy(), color=(0, 0, 0))
        img.draw_string(blob.x(), blob.y(), "purple", color=(0, 0, 0), scale=2)

    # Count the number of blobs for each color
    orange_count = len(orange_blobs)
    white_count = len(white_blobs)
    purple_count = len(purple_blobs)

    # Display the counts at the bottom of the screen
    img.draw_string(2, 2, str(clock.fps()), color=(255, 255, 255))
    img.draw_string(2, 220, "Orange: " + str(orange_count), color=(255, 255, 255))
    img.draw_string(120, 220, "White: " + str(white_count), color=(255, 255, 255))
    img.draw_string(240, 220, "Purple: " + str(purple_count), color=(255, 255, 255))

    lcd.display(img)

    # Calculate the time taken for processing and delay accordingly to achieve the desired FPS
    processing_time = time.ticks_ms() - start_time
    if processing_time < 20:
        time.sleep_ms(20 - processing_time)
