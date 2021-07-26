# Scroll function with fist closed (scroll down), open palm (scroll up)
# Only works for the right hand
"""

Execute:
.\venv\Scripts\activate.ps1 
"""

import cv2
import mediapipe as mp
from handDetectionModule import HandDetector
import pyautogui

detector = HandDetector()
drawTools = mp.solutions.drawing_utils
capture = cv2.VideoCapture(0)


while True:

    success, img = capture.read()
    lmlist, img = detector.lmlist(img, True)

    if lmlist:
        fingers = detector.fingerUp(img,lmlist,True)

        if fingers == [0,0,0,0,0]:
            pyautogui.scroll(-50)
        elif fingers == [1,1,1,1,1]:
            pyautogui.scroll(50)


    cv2.imshow("Video Feed:",img)

    key = cv2.waitKey(1)

    if key == 27: # escape
        break

capture.release()
cv2.destroyAllWindows()