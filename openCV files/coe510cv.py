import cv2 as cv
import numpy as np
from generalpurposecv import CVMainTopics
import time

general=CVMainTopics()




############################################
#for image only
imagePath="C:\\Users\\ICTC\\Desktop\\1.jpg"
#for camera only
camera=1
cameraResolution=(640,480) #My resolution is width=640px hight=480px    
#settings for image and camera
colorsDetect=[['Blue',(78,100,80),(138,255,255)],['Red',(0,70,80),(20,255,255)],['White (Assume Motion)',(0,0,200),(255,50,255)]]
#settings for image, camera and Motion Detection
ySegments=10
xSegments=10
areaFraction=0.1
showFrames=True
blur=1 #put an odd number. if you put an even number you will get an error
frameSize=(640,480)
segmentsLinesColor=(255,0,0)
segmentsLinesThickness=2
waitKey=100
##settings for Motion Detection
threshold=10
dilateIterations=3
gaussianBlurKernel=(5,5)
############################################

def cameraColorDetection(camera=camera,ySegments=ySegments,xSegments=xSegments,
colorsDetect=colorsDetect,areaFraction=areaFraction,showFrames=showFrames,
blur=blur,cameraResolution=cameraResolution,frameSize=frameSize,
segmentsLinesColor=segmentsLinesColor,segmentsLinesThickness=segmentsLinesThickness,
waitKey=waitKey
):
    while True:
        cap=cv.VideoCapture(camera)
        if (cap.isOpened()==True):
            break

        if (cap.isOpened()==False and camera>0):
            camera=camera-1
        if (cap.isOpened()==False and camera<0):
            camera=camera+1

    cap.set(3,cameraResolution[0])
    cap.set(4,cameraResolution[1])

    while (cap.isOpened()):
        ret,frame=cap.read()


        
        frame=cv.resize(frame,(frameSize[0],frameSize[1]))
        
        
        for i in range(len(colorsDetect)):

            blackAndWhiteFrame=general.colorDetect(frame,colorsDetect[i][1],colorsDetect[i][2],blur)

            colorsResults=general.getPlace(blackAndWhiteFrame,ySegments,xSegments,areaFraction,colorsDetect[i][0])
            if showFrames==True:
                cv.imshow(str(colorsDetect[i][0]),blackAndWhiteFrame)

            yield colorsResults
            #print(colorsResults)

        
        

        frame=general.drawSegments(frame,ySegments,xSegments,segmentsLinesColor,segmentsLinesThickness)
        
        if showFrames==True:
            cv.imshow("Real Frame ",frame)


        #If you put in the waitKey(0) it might not work and you may get a frozen image
        key=cv.waitKey(waitKey)
        
        if key==27:
            break



    cv.destroyAllWindows()
    cap.release()

def imageColorDetection(imagePath,ySegments=ySegments,xSegments=xSegments,
colorsDetect=colorsDetect,areaFraction=areaFraction,showFrames=True,
blur=blur,frameSize=frameSize,segmentsLinesColor=segmentsLinesColor,
segmentsLinesThickness=segmentsLinesThickness
):


    image=cv.imread(imagePath)
    imageDetection=[]

    for i in range(len(colorsDetect)):

            blackAndWhiteFrame=general.colorDetect(image,colorsDetect[i][1],colorsDetect[i][2],blur)

            imageDetection.append(blackAndWhiteFrame)

            colorsResults=general.getPlace(blackAndWhiteFrame,ySegments,xSegments,areaFraction,colorsDetect[i][0])
            if showFrames==True:
                cv.imshow(str(colorsDetect[i][0]),blackAndWhiteFrame)

            yield colorsResults
            #print(colorsResults)


    while True:

        

        image=general.drawSegments(image,ySegments,xSegments,segmentsLinesColor,segmentsLinesThickness)
        if showFrames==True:
            cv.imshow("Real Image",image)

        for i in range(len(colorsDetect)):
            if showFrames==True:
                cv.imshow(colorsDetect[i][0],imageDetection[i])

        key=cv.waitKey(55)
        if key ==27:
            break

    
    cv.destroyAllWindows()



#https://www.youtube.com/watch?v=MkcUgPhOlP8
def motionDetection(camera=camera,ySegments=ySegments,xSegments=xSegments,
showFrames=showFrames,blur=blur,cameraResolution=cameraResolution,frameSize=frameSize,
segmentsLinesColor=segmentsLinesColor,segmentsLinesThickness=segmentsLinesThickness,
waitKey=waitKey
):

    while True:
        cap=cv.VideoCapture(camera)
        if (cap.isOpened()==True):
            break

        if (cap.isOpened()==False and camera>0):
            camera=camera-1
        if (cap.isOpened()==False and camera<0):
            camera=camera+1

    cap.set(3,cameraResolution[0])
    cap.set(4,cameraResolution[1])

    ret1,frame1=cap.read()

    ret2,frame2=cap.read()
    

    while (cap.isOpened()):

        frame1=cv.resize(frame1,(frameSize[0],frameSize[1]))
        frame2=cv.resize(frame2,(frameSize[0],frameSize[1]))

        diff=cv.absdiff(frame1,frame2)
        diffMBlur=cv.medianBlur(diff,blur)
        diffGray=cv.cvtColor(diff,cv.COLOR_BGR2GRAY)
        diffGBlur=cv.GaussianBlur(diffGray,gaussianBlurKernel,0)
        _,thresh=cv.threshold(diffGBlur,threshold,255,cv.THRESH_BINARY)
        dilated=cv.dilate(thresh,None,iterations=dilateIterations)

        
        
        



        results=general.getPlace(dilated,ySegments,xSegments,areaFraction,"Motion Detection")


        yield results
        #print(results)



        

        frame1=frame2
        ret2,frame2=cap.read()

        frame1draw=general.drawSegments(frame1,ySegments,xSegments,segmentsLinesColor,segmentsLinesThickness)

        key=cv.waitKey(waitKey)
        if showFrames == True:
            cv.imshow("Realframe",frame1draw)
            cv.imshow("Motion",dilated)

        if key==27:
            break

    
    cv.destroyAllWindows()
    cap.release()










if __name__=="__main__":

    pass