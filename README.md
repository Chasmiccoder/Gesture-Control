# Gesture-Control
Awesome OpenCV + Mediapipe project to change the volume/screen brightness, scroll, and control the mouse pointer - all with gestures!

<br>
Special thanks to <a href="https://github.com/vinamrak">Vinamra</a> bhaiya for the <a href="https://www.youtube.com/watch?v=SlqHa2R9RYg">foundation!</a>
<br>


<br>

### <u>Usage + Features!</u>

* Scroll with Right Hand
* Brightness Control with Left Hand
* Volume Control with Right Hand
* Mouse Control with Right Hand


<br>
<br>

### <u>Installation</u>

For Windows - (Tested with Python 3.9.5)

After cloning the repo, run these commands in command prompt

Install the virtual environments package

    pip install virtualenv

Create a virtual environment with the name venv

    virtualenv venv

Activate the created virtual environment (use one of the two commands)

    .\venv\Scripts\activate.bat
    .\venv\Scripts\activate.ps1

Install the required packages

    pip install -r requirements.txt

If you are using VSCode, configure settings.json as follows

    {
        "python.pythonPath": ".\\venv\\Scripts\\python"
    }



### <u>Common Issues</u>

(Create separate file for this section) <br>
1) Webcam <br>
If the webcam doesn't work, pass 1 instead of 0 in the lines using cv2.VideoCapture()
as follows:
    
    capture = cv2.VideoCapture(1)

<br>

2) Mediapipe's Left Hand / Right Hand Classifier is not always accurate, which might lead to some incoherence



Docs:

Check out -
https://google.github.io/mediapipe/solutions/hands.html

tests folder contains the old programs

src contains the main file with the GestureRecognition module



