import cv2
import mediapipe as mp

import math
import numpy as np

import pyautogui

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import screen_brightness_control
 




class GestureRecog():
    def __init__(self):
        
        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands()

        self.drawTools = mp.solutions.drawing_utils

        # Volume Control
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))


    def lmlist(self,img, draw=False):
        lmlist = []
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handlms in results.multi_hand_landmarks:

                for id,lm in enumerate(handlms.landmark):
                    height, width, channels = img.shape

                    # Current x and y coordinates
                    cx, cy = int( lm.x * width ), int( lm.y * height )

                    lmlist.append([id,cx,cy])

                if draw:
                    self.drawTools.draw_landmarks(img,handlms, self.mpHands.HAND_CONNECTIONS)
        
        return lmlist, img


    def fingerUp(self,img,lmlist,isLeftHand, draw = False):
        """
        Returns a list of 5 elements. First finger is the thumb
        If 1, the finger is up. If it is 0, the finger is down 'has been clenched'
        Works for Right Hand (because of how the right thumb folds)
        """
        fingers = []
        tipIds = [8,12,16,20]
        count = 0

        # For the thumbs
        if isLeftHand == False:
            if lmlist[4][1] > lmlist[3][1]:
                count += 1
                fingers.append(1)
            else:
                fingers.append(0)
        else: # integrate left hand better
            if lmlist[4][1] < lmlist[3][1]:
                count += 1
                fingers.append(1)
            else:
                fingers.append(0)

        for id in tipIds:
            if lmlist[id][2] > lmlist[id-2][2]:
                fingers.append(0)
            
            else:
                fingers.append(1)
                count += 1
        
        if draw:
            cv2.putText(img, str(count), (50,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

        return fingers, img


    def findDistance(self, p1, p2, img, lmlist,draw=False ):
        x1,y1 = lmlist[p1][1:]
        x2,y2 = lmlist[p2][1:]

        length = math.hypot(x2-x1, y2-y1) # Euclidean distance

        if draw:                             # BGR
            cv2.line(img, (x1,y1),(x2,y2), (255,0,255), 3 )
            cv2.circle(img, (x1,y1),5,(255,0,0), cv2.FILLED)
            cv2.circle(img, (x2,y2),5,(255,0,0), cv2.FILLED)


        return length, img





    # Create is_left_hand function
    def isLeftHand(self, img):
        """
        First returned variable returns False if a hand is not detected, and True if
        a hand is detected.
        The second returned variable returns True if the hand is a Left hand
        and False if it is a Right hand
        """

        flipped_image = cv2.flip(img, 1)
        orientation_results = self.hands.process(cv2.cvtColor(flipped_image, cv2.COLOR_BGR2RGB))

        handType = orientation_results.multi_handedness
        whichHand = None

        if handType:
            whichHand = handType[0].classification[0].label
            if whichHand == "Left":
                return True, True
            else:
                return True, False

        else:
            return False, False

    def scrollControl(self ,fingers, scrollSpeed = 50, draw = False):
        
        if fingers == [0,0,0,0,0]:
            pyautogui.scroll(-scrollSpeed)
            print("Scrolling Down")
        elif fingers == [1,1,1,1,1]:
            pyautogui.scroll(scrollSpeed)
            print("Scrolling Up")


    def mouseControl(self, img, lmlist, fingers, draw = False):
        
        # Bounding Rectangle (Mouse Control Area)
        frameR_x = 70 # Keeping distance of 100 from each edge
        frameR_y = 50

        frame_width = 400
        frame_height = 250

        # No Movement Zone (NMZ)
        top_left_x = frameR_x + 125
        top_left_y = frameR_y + 70

        NMZ_width = 150
        NMZ_height = 100

        if fingers == [0,1,0,0,0]:


            # Coords of tip of index finger
            x1,y1 = lmlist[8][1:] # [1:] is for the x and y coordinates
            # lmlist[8] is like: (id, x, y)

            # cv2.rectangle(img,(frameR,frameR), (540,380), (255,0,255),3)
            

            relative_factor_x = 40
            relative_factor_y = 40            


            # cv2.rectangle(img,(frameR_x,frameR_y), (frameR_x + frame_width,frameR_y + frame_height), (255,0,255),3)
            
            # Mouse Control Bounding rectangle
            cv2.rectangle(img,(frameR_x,frameR_y), (frameR_x + frame_width,frameR_y + frame_height), (255,0,255),3)

            # No-Movement Zone
            cv2.rectangle(img,(top_left_x,top_left_y), (top_left_x + NMZ_width,top_left_y + NMZ_height), (255,0,0),3)


            cv2.circle(img,(x1,y1),10, (255,0,255), cv2.FILLED)


            if x1 >= top_left_x + NMZ_width and x1 <= frameR_x + frame_width:
                pyautogui.move(-relative_factor_x, 0) # move mouse to the left
                print("Mouse -> left")
            
            elif x1 <= top_left_x and x1 >= frameR_x:
                pyautogui.move(relative_factor_x, 0)  # move mouse to the right
                print("Mouse -> right")

            elif y1 <= top_left_y and y1 >= frameR_y:
                pyautogui.move(0, -relative_factor_y)  # move mouse downwards
                print("Mouse -> down")
                
            # LOGIC? HOW IS THIS WORKING?
            elif y1 <= frameR_y + frame_height and y1 >= top_left_y + NMZ_height:
                pyautogui.move(0, relative_factor_y)  # move mouse upwards
                print("Mouse -> up")
                
        # IF the index finger is up, and the thumb gets stretched out, do left click
        if fingers == [1,1,0,0,0]:
            pyautogui.click()
            print("LEFT CLICK!")


    def volumeControl(self, img, lmlist,draw=False):

        # Taking the distance between landmarks 8 (tip of the index) and 4 (tip of the thumb)
        length, img = self.findDistance(4,8,img,lmlist,draw=True)
        
        # The distance between the fingers ranges from 30 to 200
        new_vol = np.interp(length, (30,200), (0,1))
        
        currentVolume = self.volume.GetMasterVolumeLevelScalar()

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
            self.volume.SetMasterVolumeLevelScalar(new_vol, None)
            print("Volume Changed")

    def brightnessControl(self, img, lmlist, draw = False):

        # Taking the distance between landmarks 8 (tip of the index) and 4 (tip of the thumb)
        length, img = self.findDistance(4,8,img,lmlist,draw=True)
        
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
            print("Brightness Changed")
            
