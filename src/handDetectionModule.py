import cv2
import mediapipe as mp

mpHands = mp.solutions.hands

hands = mpHands.Hands()

drawTools = mp.solutions.drawing_utils

class HandDetector():
    # returns the landmark list and image object
    # The landmark list is a list of 5 integers. 1 if the finger is up, and 0 if it is down
    def lmlist(self,img, draw=True):
        lmlist = []
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handlms in results.multi_hand_landmarks:

                for id,lm in enumerate(handlms.landmark):
                    height, width, channels = img.shape

                    # Current x and y coordinates
                    cx, cy = int( lm.x * width ), int( lm.y * height )

                    lmlist.append([id,cx,cy])

                if draw:
                    drawTools.draw_landmarks(img,handlms, mpHands.HAND_CONNECTIONS)
        
        return lmlist, img


    def fingerUp(self,img,lmlist, draw = True):
        """
        Returns a list of 5 elements. First finger is the thumb
        If 1, the finger is up. If it is 0, the finger is down 'has been clenched'
        Works for Right Hand (because of how the right thumb folds)
        """
        fingers = []
        tipIds = [8,12,16,20]
        count = 0

        # For the thumbs
        if lmlist[4][1] > lmlist[3][1]:
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

        return fingers


    def findDistance(self, p1, p2, img, lmlist,draw=False ):
        x1,y1 = lmlist[p1][1:]
        x2,y2 = lmlist[p2][1:]



