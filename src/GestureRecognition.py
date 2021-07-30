import cv2
import mediapipe as mp

import math
import numpy as np
import time

import pyautogui

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import screen_brightness_control


class GestureRecog():
    def __init__(self):
        """
        Initialize the Hands() class along with the volume control object
        """
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.drawTools = mp.solutions.drawing_utils

        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))


    def getLandmarks(self, img, draw = False):
        """
        Returns the set of landmarks on the recognized hand, along with the processed image
        Mediapipe recognized 21 such landmarks (with IDs ranging from 0 to 20)
        """
        
        landmarks = []
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLandmarks in results.multi_hand_landmarks:

                for id,lm in enumerate(handLandmarks.landmark):
                    height, width, channels = img.shape

                    # Current x and y coordinates
                    cx, cy = int( lm.x * width ), int( lm.y * height )

                    landmarks.append([id,cx,cy])

                # draw landmark skeleton
                if draw:
                    self.drawTools.draw_landmarks(img,handLandmarks, self.mpHands.HAND_CONNECTIONS)
        
        return landmarks, img


    def fingerUp(self, img, landmarks, isLeftHand, draw = False):
        """
        Returns a list of 5 elements and the processed image
        List format - [thumb, index, middle, ring, pinky]

        If 1, the finger is up. If 0, the finger is down 'has been clenched'
        Works for both, Right and Left Hands
        """

        fingers = []
        tipIds = [8,12,16,20]       # Landmarks of the index, middle, ring and pinky finger
        count = 0

        # Left Hand Thumb
        if isLeftHand:
            if landmarks[4][1] < landmarks[3][1]:
                count += 1
                fingers.append(1)
            else:
                fingers.append(0)
        # Right Hand Thumb
        else:
            if landmarks[4][1] > landmarks[3][1]:
                count += 1
                fingers.append(1)
            else:
                fingers.append(0)

        # Other 4 fingers (orientation is the same for both left and right hands)
        # id-2 is the id for the respective finger's middle groove
        for id in tipIds:
            if landmarks[id][2] > landmarks[id-2][2]:
                fingers.append(0)
            
            else:
                fingers.append(1)
                count += 1
        
        # show number of fingers that are up
        if draw:
            cv2.putText(img, str(count), (50,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

        return fingers, img


    def findDistance(self, lm1, lm2, img, landmarks, draw = False ):
        """
        Returns the distance between 2 landmarks on the hand - lm1 and lm2, and the processed image
        """

        x1,y1 = landmarks[lm1][1:]
        x2,y2 = landmarks[lm2][1:]

        # Euclidean distance between 2 points
        length = math.hypot(x2-x1, y2-y1) 

        # Display line between the two landmarks
        if draw:
            cv2.line(img, (x1,y1),(x2,y2), (255,0,255), 3 )
            cv2.circle(img, (x1,y1),5,(255,0,0), cv2.FILLED)
            cv2.circle(img, (x2,y2),5,(255,0,0), cv2.FILLED)

        return length, img


    def isLeftHand(self, img):
        """
        First returned variable is False if a hand is not detected, and True if a hand is detected

        The second returned variable is True if the hand is a Left hand and False if it is a Right hand
        """
        
        # Mirror the current image
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


    def scrollControl(self ,fingers, scrollSpeed = 50):
        """
        Scroll up by clenching your fist and down by opening palm (Right hand)
        """
        
        if fingers == [0,0,0,0,0]:
            pyautogui.scroll(-scrollSpeed)
            print("Scrolling Down")
        elif fingers == [1,1,1,1,1]:
            pyautogui.scroll(scrollSpeed)
            print("Scrolling Up")


    def mouseControl(self, img, landmarks, fingers, draw = True):
        """
        Control the mouse with your right hand
        Clentch your fist and release your index finger
        If the tip is within the blue rectangle (Neutral Area), nothing happens
        Move the index around to control the mouse

        Extend thumb outward for left click
        """
        
        # Bounding Rectangle (Mouse Control Area)
        frameR_x = 70
        frameR_y = 50

        frame_width = 400
        frame_height = 250

        # Neutral Area
        inner_x = frameR_x + 125
        inner_y = frameR_y + 70

        inner_width = 150
        inner_height = 100

        if fingers == [0,1,0,0,0]:

            # Coords of tip of index finger
            x1,y1 = landmarks[8][1:]
            
            relative_x = 40
            relative_y = 40            
            
            # Better control if the boundaries are visible
            if draw:
                # Mouse Control Bounding rectangle
                cv2.rectangle(img, (frameR_x, frameR_y), (frameR_x + frame_width, frameR_y + frame_height), (255,0,255), 3)

                # No-Movement Zone / Neutral Area
                cv2.rectangle(img, (inner_x, inner_y), (inner_x + inner_width, inner_y + inner_height), (255,0,0), 3)

                cv2.circle(img,(x1,y1),10, (255,0,255), cv2.FILLED)

            # Move mouse to the left
            if x1 >= inner_x + inner_width and x1 <= frameR_x + frame_width:
                pyautogui.move(-relative_x, 0) 
                print("Mouse -> left")
            
            # Move mouse to the right
            elif x1 <= inner_x and x1 >= frameR_x:
                pyautogui.move(relative_x, 0)  
                print("Mouse -> right")

            # Move mouse downwards
            elif y1 <= inner_y and y1 >= frameR_y:
                pyautogui.move(0, -relative_y)  
                print("Mouse -> down")
                
            # Move mouse upwards
            elif y1 <= frameR_y + frame_height and y1 >= inner_y + inner_height:
                pyautogui.move(0, relative_y)  
                print("Mouse -> up")
                
        # If the index finger is up, and the thumb gets stretched out, do left click
        if fingers == [1,1,0,0,0]:
            pyautogui.click()
            print("Left Click!")


    def volumeControl(self, img, landmarks, draw = True):
        """
        Gesture (with Right Hand): 
        Clentch your fist, and then extend your index, thumb and little finger (like spiderman's thing)
        
        Control Volume by changing the distance between your index finger and thumb
        """

        # Taking the distance between landmarks 8 (tip of the index) and 4 (tip of the thumb)
        length, img = self.findDistance(4,8,img,landmarks,draw=True)
        
        # The distance between the fingers ranges from 30 to 200
        new_vol = np.interp(length, (30,200), (0,1))
        
        currentVolume = self.volume.GetMasterVolumeLevelScalar()

        # For a volume change to be valid there should be at least 10% difference. Done to retain smooth functioning
        threshold = 0.1
        
        volume_percent = np.interp(currentVolume, (0,1), (0,100) )
        volume_bar = np.interp(currentVolume, (0,1), (0,200))

        # Visual Volume Bar
        if draw:
            cv2.putText(img,str(int(volume_percent))+"%", (50,100), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3)
            cv2.rectangle(img,(50,120),(80,320), (255,0,0), 3)
            cv2.rectangle(img,(50,320-int(volume_bar)),(80,320), (255,0,0), cv2.FILLED)

        # If the difference between the new volume and the old one is greater than the threshold, then change the volume
        if abs(currentVolume - new_vol) >= threshold:
            self.volume.SetMasterVolumeLevelScalar(new_vol, None)
            print("Volume Changed")


    def brightnessControl(self, img, landmarks, draw = False):
        """
        Gesture (with Left Hand): 
        Clentch your fist, and then extend your index, thumb and little finger (like spiderman's thing)
        
        Control Brightness by changing the distance between your index finger and thumb
        """

        # Taking the distance between landmarks 8 (tip of the index) and 4 (tip of the thumb)
        length, img = self.findDistance(4,8,img,landmarks,draw=True)
        
        # The distance between the fingers ranges from 30 to 200
        new_brightness = np.interp(length, (30,200), (0,100))
        
        currentBrightness = screen_brightness_control.get_brightness()

        # For a brightness change to be valid there should be at least 10% difference. Done to retain smooth functioning
        threshold = 10
        
        brightness_percent = np.interp(currentBrightness, (0,100), (0,100) )
        brightness_bar = np.interp(currentBrightness, (0,100), (0,200))

        colorOrange = (102,178,255)

        # Visual Brightness Bar
        if draw:
            cv2.putText(img,str(int(brightness_percent))+"%", (50,100), cv2.FONT_HERSHEY_COMPLEX, 1, colorOrange, 3)
            cv2.rectangle(img,(50,120),(80,320), colorOrange, 3)
            cv2.rectangle(img,(50,320-int(brightness_bar)),(80,320), colorOrange, cv2.FILLED)

        # If the difference between the new brightness and the old one is greater than the threshold, then change the brightness
        if abs(currentBrightness - new_brightness) >= threshold:
            screen_brightness_control.set_brightness(new_brightness)
            print("Brightness Changed")


    def altTabChange(self, img, landmarks):
        """
        Gesture with Left Hand -
        Middle, Ring and Little Finger are up
        Index finger and Thumb make contact to simulate: Alt + Tab
        """
        
        length, img = self.findDistance(4,8,img,landmarks,draw=True)
        
        # Index and Thumb tips make contact
        if length < 40:
            pyautogui.keyDown('alt')
            time.sleep(.2)
            pyautogui.press('tab')
            time.sleep(.2)
            pyautogui.keyUp('alt')
