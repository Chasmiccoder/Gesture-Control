import cv2
import mediapipe as mp
from handDetectionModule import HandDetector
import pyautogui
import numpy as np


# Checking the size of the screen (640 by 480) is the size of the window
print("Screen Size: ", pyautogui.size()) # Screen size is 1920 by 1080

# We need to convert motion of the finger in 640x480 and translate that to 1920x1080

smoothening = 10 # This just slows things down
clocX, clocY, plocX, plocY = 0,0,0,0
# Current and Previous X and Y positions

# Employ different smoothening tactic! using difference in position. If difference is not too large, don't execute
# Do this: Left click == when point 8 goes below 7, but above 6. Right click == when point 8 is below 6




detector = HandDetector()

capture = cv2.VideoCapture(0)


# To create a boundary for detection. (Keeping the openvc window does not work for edges)
frameR = 100 # Keeping distance of 100 from each edge


while True:
    success, img = capture.read()

    lmlist, img = detector.lmlist(img)

    if lmlist:

        fingers, img = detector.fingerUp(img,lmlist,draw=False)

        if fingers == [0,1,0,0,0]:


            # Coords of tip of index finger
            x1,y1 = lmlist[8][1:] # [1:] is for the x and y coordinates
            # lmlist[8] is like: (id, x, y)

            cv2.rectangle(img,(frameR,frameR), (540,380), (255,0,255),3)
            cv2.circle(img,(x1,y1),10, (255,0,255), cv2.FILLED)

            posX = np.interp(x1,(frameR,640-frameR), (0,1920))
            posY = np.interp(y1,(frameR,480-frameR),(0,1080))

            clocX = plocX + (posX - plocX) / smoothening
            clocY = plocY + (posY - plocY) / smoothening

            



            # Moves the mouse pointer to these coords
            pyautogui.moveTo(1920-clocX,clocY)
            # pyautogui.moveTo(posX,posY)



            plocX = clocX
            plocY = clocY

        elif fingers == [0,1,1,0,0]:
            distance, img = detector.findDistance(8,12,img,lmlist)

            # If the index and middle finger are up, and they close together, left click
            if distance < 30:
                pyautogui.click()
            

            

            


    cv2.imshow("Video Feed",img)
    # cv2.resizeWindow("Video Feed", 640, 480)

    key = cv2.waitKey(1)
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()