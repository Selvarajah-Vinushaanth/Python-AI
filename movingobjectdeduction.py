import cv2
import time
import pygame
import imutils

# Initialize Pygame for sound
pygame.init()

# Load your sound file (replace 'path_to_your_sound_file.wav' with your actual sound file path)
sound_file = r'C:\Users\Vinushaanth\Downloads\security-alarm-80493.mp3'
sound = pygame.mixer.Sound(sound_file)

cam = cv2.VideoCapture(0)
time.sleep(1)

firstFrame = None
area = 50

while True:
    _, img = cam.read()
    text = "Normal"
    img = imutils.resize(img, width=1000)
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gaussianImg = cv2.GaussianBlur(grayImg, (21, 21), 0)
    
    if firstFrame is None:
        firstFrame = gaussianImg
        continue
    
    imgDiff = cv2.absdiff(firstFrame, gaussianImg)
    threshImg = cv2.threshold(imgDiff, 25, 255, cv2.THRESH_BINARY)[1]
    threshImg = cv2.dilate(threshImg, None, iterations=2)
    
    cnts = cv2.findContours(threshImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    for c in cnts:
        if cv2.contourArea(c) < area:
            continue
        
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Moving Object detected"
        
        # Play sound when moving object is detected
        if text=="Moving Object detected":
                sound.play()
    
    print(text)
    cv2.putText(img, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow("cameraFeed", img)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Release the camera and close all windowsq
cam.release()
cv2.destroyAllWindows()