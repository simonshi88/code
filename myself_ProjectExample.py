import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm


pTime = 0
cTime = 0

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.mediapipe.python.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils


while True:
    success, img = cap.read()
    img_flip = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img_flip, cv2.COLOR_BGR2RGB)
   
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                if id == 0:
                    cv2.circle(img_flip, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            mpDraw.draw_landmarks(img_flip, handLms, mpHands.HAND_CONNECTIONS)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img_flip, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
               (255, 0, 255), 3)
    cv2.imshow("Image", img_flip)
    cv2.waitKey(1)