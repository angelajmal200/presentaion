import cv2
import os
from cvzone.HandTrackingModule import HandDetector

#variables
width,height=1280,720
folderpath="Presentation"
imgNumber=0
hs,ws=120,213
gestureThreshold=300
buttonPressed=False
buttonCounter=0
buttonDelay=10

#hand detector

detector=HandDetector(detectionCon=0.8,maxHands=1)

#camera setup
cap=cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

#get list of presentation images
pathImages=sorted(os.listdir(folderpath),key=len)
print(pathImages)
while True:
    #import images
    sucess,img=cap.read()
    img=cv2.flip(img,1)
    pathFullImage=os.path.join(folderpath,pathImages[imgNumber])
    imgCurrent=cv2.imread(pathFullImage)


    hands,img=detector.findHands(img)
    cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(0,255,0),10)

    if hands and buttonPressed is False:
        hand=hands[0]
        fingers=detector.fingersUp(hand)
        cx,cy=hand['center']
        print(fingers)
 

        #if hand is at the height of the face
        if cy<=gestureThreshold:
            if fingers == [1,0,0,0,0]:
                print("left")
                if imgNumber>0:
                    buttonPressed=True
                    imgNumber-=1

            if fingers == [0,0,0,0,1]:
                print("right")
                if imgNumber<len(pathImages)-1:
                    buttonPressed=True
                    imgNumber+=1

    #button pressed iteration
    if buttonPressed:
        buttonCounter+=1
        if buttonCounter > buttonDelay:
            buttonCounter=0
            buttonPressed=False


    #addding webcam image on slide
    imgsmall=cv2.resize(img,(ws,hs))
    h,w,_=imgCurrent.shape
    imgCurrent[0:hs,w-ws:w]=imgsmall

    cv2.imshow("Image",img)
    cv2.imshow("Slides",imgCurrent)


    key=cv2.waitKey(1)
    if key==ord('q'):
        break