# Scroll function with fist closed (scroll down), open palm (scroll up)
# Only works for the right hand
"""

Execute:
.\venv\Scripts\activate.ps1 

write note on how coordinates work in opencv

Add folder with python files to individual features.
Turn the python files of the current folder into "XYZ Control" Modules
Use these modules to implement all features in main.py
Release as .exe

For volume control add condition
if fingers[-3:] == [0,0,0]:
    then do volume control (we want volume control when only the thumb and index are up, and the rest
    of the fingers have been clenched)


implement drag and drop

With pyautogui, 
Use something like
pyautogui.press('esc')
To press key combination: Alt + Tab
to implement Hand swipe for changing the window / app


Convert to python app,
release it as a single .exe for ez usage


Fix what parameter draw does

"""

import cv2
import mediapipe as mp
import GestureRecognition


recog = GestureRecognition.GestureRecog()
capture = cv2.VideoCapture(0)

# For OpenCV window
window_width = 640
window_height = 480

while True:

    success, img = capture.read()
    lmlist, img = recog.lmlist(img, draw = False)

    img = cv2.resize(img, (window_width, window_height)) # Original is (640 by 480)

    if lmlist:
        handIsThere, is_left_hand = recog.isLeftHand(img)
        fingers, img = recog.fingerUp(img,lmlist,is_left_hand)

        recog.scrollControl(fingers,scrollSpeed = 100)

        if handIsThere == True and is_left_hand == False:
            recog.mouseControl(img, lmlist,fingers,draw=False)

            # Volume control works only when index, thumb, and pinky finger are up and the middle and ring fingers are down
            # Kind of like spiderman's web shooting thingy
            if fingers == [1,1,0,0,1]:
                recog.volumeControl(img, lmlist, draw = True)
        
        if is_left_hand and fingers == [1,1,0,0,1]:
            recog.brightnessControl(img,lmlist,draw=True)



    cv2.imshow("Video Feed:",img)


    key = cv2.waitKey(1)
    if key == 27: # escape
        break

capture.release()
cv2.destroyAllWindows()