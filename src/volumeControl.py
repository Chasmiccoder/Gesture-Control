import cv2
import mediapipe as mp
from handDetectionModule import HandDetector
import numpy as np


from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


detector = HandDetector()

mpHands = mp.solutions.hands()
hands = mpHands.Hands()
drawTools = mp.solutions.drawing_utils

# If 0 doesn't work, try 1 (to choose the webcam)
capture = cv2.VideoCapture(0)

while True:
    success, img = capture.read()

    lmlist, img = detector.lmlist(img)


    


    cv2.imshow("Video Feed", img)

    key = cv2.waitKey(1)

    if key == 27:
        break


capture.release()
cv2.destroyAllWindows()






