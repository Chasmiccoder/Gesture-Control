"""
Use getmaster volume function and put some threshold for change (4 levels for example),
to make the volume control smooth

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume.GetMute()
volume.GetMasterVolumeLevel()
volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-20.0, None)

"""

import cv2
import mediapipe as mp
from handDetectionModule import HandDetector
import numpy as np

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL, IID
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


detector = HandDetector()

mpHands = mp.solutions.hands
hands = mpHands.Hands()
drawTools = mp.solutions.drawing_utils

# If 0 doesn't work, try 1 (to choose the webcam)
capture = cv2.VideoCapture(0)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange() 
print( "Volume Range: ", volRange ) # (-65.25, 0.0, 0.03125) Changes depending on audio device
# In this case, -65.25 corresponds to 0 and 0.0 corresponds to 100 in our system

minVol = volRange[0]
maxVol = volRange[1]

# Distance between thumb and index ranges from 30 to 200. *
# For normal laptop speakers, the volume levels range from -65.25 to 0 **
# We need to convert the distance obtained * into this scale **


while True:
    success, img = capture.read()

    lmlist, img = detector.lmlist(img)


    if lmlist:

        fingers, img = detector.fingerUp(img,lmlist)

        # Volume control works only when index, thumb are 'up' and when the other 3 fingers are clenched
        if fingers[-3:] == [0,0,0]:

            length = detector.findDistance(4,8,img,lmlist,draw=True) # We want point 8 (tip of the index) and 4 (tip of the thumb)
            # print(length)

            new_vol = np.interp(length, (30,200), (minVol,maxVol) )

            volume_percent = np.interp(length, (30,200), (0,100) )

            volume_bar = np.interp(length, (30,200), (270,120))

            cv2.putText(img,str(int(volume_percent))+"%", (50,100), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3)
            
            cv2.rectangle(img,(50,120),(80,270), (255,0,0), 3) # Starting coordinate at 50,120. 
            # Ending coordinate (diagonally opp) at 80,270

            cv2.rectangle(img,(50,int(volume_bar)),(80,270), (255,0,0), cv2.FILLED)

            


            volume.SetMasterVolumeLevel(new_vol, None)



    


    cv2.imshow("Video Feed", img)

    key = cv2.waitKey(1)

    if key == 27:
        break


capture.release()
cv2.destroyAllWindows()






