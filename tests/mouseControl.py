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

x_threshold = 10
y_threshold = 10

# Employ different smoothening tactic! using difference in position. If difference is not too large, don't execute
# Do this: Left click == when point 8 goes below 7, but above 6. Right click == when point 8 is below 6

detector = HandDetector()

capture = cv2.VideoCapture(0)

window_width = 640
window_height = 480

# BOUNDING RECTANGLE
# To create a boundary for detection. (Keeping the openvc window does not work for edges)
frameR_x = 70 # Keeping distance of 100 from each edge
frameR_y = 50

frame_width = 400
frame_height = 250

# NO-MOVEMENT ZONE (NMZ)
top_left_x = frameR_x + 125
top_left_y = frameR_y + 70

NMZ_width = 150
NMZ_height = 100

while True:
    success, img = capture.read()
    img = cv2.resize(img, (window_width, window_height)) # Original is (640 by 480)

    lmlist, img = detector.lmlist(img)

    handIsThere, is_left_hand = detector.isLeftHand(img)

    if lmlist and handIsThere == True and is_left_hand == False:

        fingers, img = detector.fingerUp(img,lmlist,draw=False)

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


            #NOT USED
            index_tip_x,index_tip_y = lmlist[8][1:]
            index_groove_x, index_groove_y = lmlist[7][1:]
            # While left clicking, point 8 goes below 7 and 6, so while that is happening, don't move the mouse
            
            if x1 >= top_left_x + NMZ_width and x1 <= frameR_x + frame_width:
                pyautogui.move(-relative_factor_x, 0) # move mouse to the left
            
            elif x1 <= top_left_x and x1 >= frameR_x:
                pyautogui.move(relative_factor_x, 0)  # move mouse to the right

            elif y1 <= top_left_y and y1 >= frameR_y:
                pyautogui.move(0, -relative_factor_y)  # move mouse downwards
                
            
            elif y1 <= frameR_y + frame_height and y1 >= top_left_y + NMZ_height:
                pyautogui.move(0, relative_factor_y)  # move mouse upwards
                
            
        


            """
            
            posX = np.interp(x1,(frameR_x,frameR_x + frame_width), (0,1920))
            posY = np.interp(y1,(frameR_y,frameR_y + frame_height),(0,1080))


            relative_pos_x = np.interp(x1,(frameR_x,frameR_x + frame_width), (-relative_factor,relative_factor))
            relative_pos_y = np.interp(y1,(frameR_y,frameR_y + frame_height),(-relative_factor,relative_factor))

            # relative_factor = 150

            # clocX = plocX + (posX - plocX) / smoothening
            # clocY = plocY + (posY - plocY) / smoothening
            clocX = posX
            clocY = posY

            


            # new smoothening metric
            if abs(plocX - clocX) >= x_threshold and abs(plocY - clocY) >= y_threshold and index_tip_x > index_groove_x:

            
                # Moves the mouse pointer to these coords
                # pyautogui.moveTo(1920-clocX,clocY)
                # pyautogui.moveTo(1920-clocX, clocY, 0, pyautogui.easeInBounce)
                # pyautogui.move(-relative_pos_x, relative_pos_y,0 ,pyautogui.easeInQuad)
                pyautogui.move(-relative_factor_x, relative_factor_y)

                # pyautogui.moveTo(posX,posY)

            """

            plocX = clocX
            plocY = clocY

            # elif fingers == [0,1,1,0,0]:
            # distance, img = detector.findDistance(8,12,img,lmlist)

            # index_tip_x,index_tip_y = lmlist[8][1:]
            # index_groove_x, index_groove_y = lmlist[7][1:]

            # # If the index and middle finger are up, and they close together, left click
            # if index_tip_x < index_groove_x:
            #     pyautogui.click()
            #     print("LEFT CLICK!")
        
        if fingers == [1,1,0,0,0]:
            pyautogui.click()
            print("LEFT CLICK!")

    cv2.imshow("Video Feed",img)

    key = cv2.waitKey(1)
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()