import cv2
import mediapipe as mp
import numpy as np

from handDetectionModule import HandDetector
import screen_brightness_control

currentBrightness = screen_brightness_control.get_brightness()
# screen_brightness_control.set_brightness(50)

detector = HandDetector()

mpHands = mp.solutions.hands
hands = mpHands.Hands()

capture = cv2.VideoCapture(0)


while True:

    success, img = capture.read()
    lmlist, img = detector.lmlist(img)

    if lmlist:

        fingers, img = detector.fingerUp(img,lmlist)

        # Brightness control works only when index, thumb are 'up' and when the other 3 fingers are clenched
        if fingers[-3:] == [0,0,0]:

            # Taking the distance between landmarks 8 (tip of the index) and 4 (tip of the thumb)
            length, img = detector.findDistance(4,8,img,lmlist,draw=True)
            
            # The distance between the fingers ranges from 30 to 200
            new_brightness = np.interp(length, (30,200), (0,100))
            
            # currentVolume = volume.GetMasterVolumeLevelScalar()
            currentBrightness = screen_brightness_control.get_brightness()

            # For a volume change to be valid there should be at least 10% difference. Done to retain smooth functioning
            threshold = 10
            
            volume_percent = np.interp(currentBrightness, (0,100), (0,100) )
            volume_bar = np.interp(currentBrightness, (0,100), (0,200))

            # Visual Volume Bar
            cv2.putText(img,str(int(volume_percent))+"%", (50,100), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3)
            cv2.rectangle(img,(50,120),(80,320), (255,0,0), 3)
            cv2.rectangle(img,(50,320-int(volume_bar)),(80,320), (255,0,0), cv2.FILLED)

            # If the difference between the new volume and the old one is greater than the threshold, then change the volume
            if abs(currentBrightness - new_brightness) >= threshold:
                screen_brightness_control.set_brightness(new_brightness)
                # volume.SetMasterVolumeLevelScalar(new_brightness, None)


    cv2.imshow("Video Feed", img)
    if cv2.waitKey(1) == 27: # escape button
        break

capture.release()
cv2.destroyAllWindows()





