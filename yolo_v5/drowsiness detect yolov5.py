import torch
import numpy as np
import cv2
import serial
#15: L_open  16: R_open  17: L_close  18: R_close

ser = serial.Serial('COM5', 9600)

model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Users/kcw01/Downloads/best (1).pt', force_reload=True)

cap = cv2.VideoCapture(0)
count = 0

while cap.isOpened():
    ret, frame = cap.read()
    
    results = model(frame)
    
    detected_class = []
    if len(results.pandas().xyxy[0]) >= 2:
        for detection in results.xyxy[0]:
            detected_class.append(int(detection[5].item()))
        if 17 in detected_class or 18 in detected_class: #양쪽눈감김 동시 인식
            count += 1

            if count >= 25:
                ser.write(b'R')
        else:
            count = 0

    print(count)
    cv2.putText(frame, f"Count: {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('monitor', np.squeeze(results.render()))

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
