"""
To test if OpenCV and Mediapipe have been installed correctly
When you show your hand to the camera, you should be able to see the 21 hand landmarks
"""

import cv2
import mediapipe as mp

mpHands = mp.solutions.hands

hands = mpHands.Hands()

# 42 for 2 hands (21 points each have been identified by Google)

drawTools = mp.solutions.drawing_utils

capture = cv2.VideoCapture(0)
while True:

    success, img = capture.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            drawTools.draw_landmarks(img,handlms,mpHands.HAND_CONNECTIONS)



    cv2.imshow("Video Feed:",img)


    key = cv2.waitKey(1)

    if key == 27: # escape button
        break

for handlms in results.multi_hand_landmarks:
    drawTools.draw_landmarks(img,handlms,mpHands.HAND_CONNECTIONS)
    
capture.release()
cv2.destroyAllWindows()