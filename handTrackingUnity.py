from HandTrackingModule import handDetector
import cv2
import socket

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
# success, img = cap.read()
# h, w, _ = img.shape
detector = handDetector(detectionCon=0.8, maxHands=2)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

while True:
    # Get image frame
    success, img_original = cap.read()
    img = cv2.flip(img_original,1)

    h, w, d = img.shape

    # Find the hand and its landmarks
    detector.findHands(img,True)  # with draw

    result = detector.results

    data = []
    if result.multi_hand_landmarks:
        for landmark in result.multi_hand_landmarks:
            for id, lm in enumerate(landmark.landmark):

                cx, cy, cz = int(lm.x * w), int(lm.y * h), int(lm.z * 100)
                #print(cx, cy, cz)
                data.extend([w-cx, h-cy,cz])

        #print(data)        
        sock.sendto(str.encode(str(data)), serverAddressPort)

    # hands = detector.findHands(img, draw=False)  # without draw
  
    # Display
    # cv2.imshow("Image", img)
    # cv2.waitKey(1)