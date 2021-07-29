# Scroll function with fist closed (scroll down), open palm (scroll up)
# Only works for the right hand
"""

Execute:
.\venv\Scripts\activate.ps1 

write note on how coordinates work in opencv

For volume control add condition
if fingers[-3:] == [0,0,0]:
    then do volume control (we want volume control when only the thumb and index are up, and the rest
    of the fingers have been clenched)


implement drag and drop

With pyautogui, 
Use something like
pyautogui.press('esc')
To press key combination: Alt + Tab
to implement Hand swipe for changing the window / app


Convert to python app,
release it as a single .exe for ez usage

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
        fingers, img = detector.fingerUp(img,lmlist,True)

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