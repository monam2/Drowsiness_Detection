import cv2
import mediapipe as mp
import serial

mp_face_mesh = mp.solutions.face_mesh

ser = serial.Serial('COM3', 9600)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
    cap = cv2.VideoCapture(0)
    count = 0

    while cap.isOpened():
        ret, frame = cap.read()

        frame = cv2.flip(frame, 1)
        image_height, image_width, _ = frame.shape

        # 얼굴 검출
        results = face_mesh.process(frame)

        if results.multi_face_landmarks:
            for single_face_landmarks in results.multi_face_landmarks:

                # 1-입(위) / 2-입(아래)
                mouth_top = single_face_landmarks.landmark[12]
                x1 = mouth_top.x * image_width
                y1 = mouth_top.y * image_height

                mouth_bot = single_face_landmarks.landmark[15]
                x2 = mouth_bot.x * image_width
                y2 = mouth_bot.y * image_height

                #3-우(위) / 4-우(아래)
                R_eye_top = single_face_landmarks.landmark[385]
                x3 = R_eye_top.x * image_width
                y3 = R_eye_top.y * image_height

                R_eye_bot = single_face_landmarks.landmark[374]
                x4 = R_eye_bot.x * image_width
                y4 = R_eye_bot.y * image_height

                #5-좌(위) / 6-좌(아래)
                L_eye_top = single_face_landmarks.landmark[158]
                x5 = L_eye_top.x * image_width
                y5 = L_eye_top.y * image_height

                L_eye_bot = single_face_landmarks.landmark[145]
                x6 = L_eye_bot.x * image_width
                y6 = L_eye_bot.y * image_height

                # x, y 좌표 점으로 출력
                for i, j in [(x1,y1),(x2,y2),(x3,y3),(x4,y4),(x5,y5),(x6,y6)]:
                    cv2.circle(frame, (int(i), int(j)), 3, (0, 0, 255), -1)

                if y2-y1 >= 50 or (y4-y3 <= 5 and y6-y5 <= 5):
                    count += 1
                    if count >= 10:
                        cv2.putText(frame, "Warning!", (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
                        ser.write(b's')
                else:
                    count = 0

        cv2.putText(frame, f"Count:{count}", (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        data = ser.readline().decode().strip()
        if data.startswith('temp: '):
            temperature = data[6:]
            if int(temperature) >= 30:
                cv2.putText(frame, f"Temp: {temperature} Air OUT!", (10, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                cv2.putText(frame, f"Temp: {temperature}", (10, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            
        cv2.imshow("Cam", frame)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()
    cap.release()
