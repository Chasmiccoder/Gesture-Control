import cv2
import mediapipe as mp
import numpy as np

from handDetectionModule import HandDetector
import screen_brightness_control

currentBrightness = screen_brightness_control.get_brightness()

detector = HandDetector()

mpHands = mp.solutions.hands
hands = mpHands.Hands()

capture = cv2.VideoCapture(0)

while True:

    success, img = capture.read()
    lmlist, img = detector.lmlist(img)

    handIsThere, is_left_hand = detector.isLeftHand(img)

    if lmlist and is_left_hand:

        fingers, img = detector.fingerUp(img,lmlist)

        # Brightness control works only when index, thumb are 'up' and when the other 3 fingers are clenched
        if fingers[-3:] == [0,0,0]:

            # Taking the distance between landmarks 8 (tip of the index) and 4 (tip of the thumb)
            length, img = detector.findDistance(4,8,img,lmlist,draw=True)
            
            # The distance between the fingers ranges from 30 to 200
            new_brightness = np.interp(length, (30,200), (0,100))
            
            currentBrightness = screen_brightness_control.get_brightness()

            # For a brightness change to be valid there should be at least 10% difference. Done to retain smooth functioning
            threshold = 10
            
            brightness_percent = np.interp(currentBrightness, (0,100), (0,100) )
            brightness_bar = np.interp(currentBrightness, (0,100), (0,200))

            colorOrange = (102,178,255)

            # Visual Brightness Bar
            cv2.putText(img,str(int(brightness_percent))+"%", (50,100), cv2.FONT_HERSHEY_COMPLEX, 1, colorOrange, 3)
            cv2.rectangle(img,(50,120),(80,320), colorOrange, 3)
            cv2.rectangle(img,(50,320-int(brightness_bar)),(80,320), colorOrange, cv2.FILLED)

            # If the difference between the new brightness and the old one is greater than the threshold, then change the brightness
            if abs(currentBrightness - new_brightness) >= threshold:
                screen_brightness_control.set_brightness(new_brightness)
                


    cv2.imshow("Video Feed", img)
    if cv2.waitKey(1) == 27: # escape button
        break

capture.release()
cv2.destroyAllWindows()