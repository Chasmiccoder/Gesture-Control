"""
Control Volume with your fingers!

Works for the right hand. Clench all your fingers except for your index finger and thumb.
Change the distance between the tip of the index and the thumb to change the volume

If you're using the 
volume.SetMasterVolumeLevel() method,
then note that the range depends on the range of the speakers / audio device
For normal laptop speakers the range is from -65.25 to 0.00
By using volume.SetMasterVolumeLevelScalar() we can directly work within the range 0.0 and 1.0

"""

import cv2
import mediapipe as mp
import numpy as np

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from handDetectionModule import HandDetector

detector = HandDetector()

mpHands = mp.solutions.hands
hands = mpHands.Hands()

capture = cv2.VideoCapture(0)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

while True:
    success, img = capture.read()
    lmlist, img = detector.lmlist(img)

    handIsThere, is_left_hand = detector.isLeftHand(img)

    if lmlist and handIsThere == True and is_left_hand == False:

        fingers, img = detector.fingerUp(img,lmlist)

        # Volume control works only when index, thumb are 'up' and when the other 3 fingers are clenched
        if fingers[-3:] == [0,0,0]:

            # Taking the distance between landmarks 8 (tip of the index) and 4 (tip of the thumb)
            length, img = detector.findDistance(4,8,img,lmlist,draw=True)
            
            # The distance between the fingers ranges from 30 to 200
            new_vol = np.interp(length, (30,200), (0,1))
            
            currentVolume = volume.GetMasterVolumeLevelScalar()

            # For a volume change to be valid there should be at least 10% difference. Done to retain smooth functioning
            threshold = 0.1
            
            volume_percent = np.interp(currentVolume, (0,1), (0,100) )
            volume_bar = np.interp(currentVolume, (0,1), (0,200))

            # Visual Volume Bar
            cv2.putText(img,str(int(volume_percent))+"%", (50,100), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3)
            cv2.rectangle(img,(50,120),(80,320), (255,0,0), 3)
            cv2.rectangle(img,(50,320-int(volume_bar)),(80,320), (255,0,0), cv2.FILLED)

            # If the difference between the new volume and the old one is greater than the threshold, then change the volume
            if abs(currentVolume - new_vol) >= threshold:
                volume.SetMasterVolumeLevelScalar(new_vol, None)


    cv2.imshow("Video Feed", img)
    if cv2.waitKey(1) == 27: # escape button
        break

capture.release()
cv2.destroyAllWindows()