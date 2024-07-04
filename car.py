import serial
import torch
import cv2
import numpy as np
import os
import time

# List of classes for cars
car_list = ['car', 'truck', 'bus']

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, etc.

# Open webcam
cap = cv2.VideoCapture(0)

# Serial port configuration
arduino_port = "COM3"  # Specify the COM port of your Arduino
ser = serial.Serial(arduino_port, 9600)  # Adjust baud rate as per your Arduino sketch

car_detected = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Detect objects in the frame
    results = model(frame)

    # Process detection results
    if results.pred[0].size(0) > 0:
        for detection in results.pred[0]:
            class_name = model.names[int(detection[5])]
            confidence = detection[4]
            # Check if the detected object is a car with confidence > 50%
            if class_name in car_list and confidence > 0.50:
                car_detected = True
                break

    # Send signal to Arduino
    if car_detected:
        print("Car detected! Opening garage door...")
        ser.write(b'1')  # Send '1' to Arduino to indicate car detection
        time.sleep(6)  # Wait for 6 seconds (door open duration)
        ser.write(b'0')  # Send '0' to Arduino to close the garage door
        car_detected = False  # Reset car detection flag

    # Break the loop if 'q' is pressed
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
