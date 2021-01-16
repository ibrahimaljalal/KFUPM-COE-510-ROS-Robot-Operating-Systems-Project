import cv2 as cv
import numpy as np
import time


class CVMainTopics:


    #This function is very important. It basically takes a frame image and returns 
    #small segments (the x and y segments are determined from the arguments)
    #The result will be in 5 or 4 diminsions (if input is black and white) 
    #the first two dimansions specify which segment in the numpy coordinate
    #The segment itself is like a frame which means it has  three or two diminsions (if input is black)
    def frameSegmentation(self,frame,ySegments,xSegments,inputType="uint8",outputType='uint8'):
        
        frame=np.array(frame,dtype=inputType)

        frameShape=frame.shape
        
        if (len(frameShape) == 2 or len(frameShape) ==3):
            yPixels=frameShape[0]
            xPixels=frameShape[1]
            

            xPixelsXSegment=xPixels//xSegments
            yPixelsYSegment=yPixels//ySegments

        else:
            print("Wrong frame format (frame should be either n*m gray or n*m*3 colored image matrix)")
            return None

        if len(frameShape)==2:
            allSegments=np.zeros((ySegments,xSegments,yPixelsYSegment,xPixelsXSegment),dtype=outputType)

        elif len(frameShape)==3:
            allSegments=np.zeros((ySegments,xSegments,yPixelsYSegment,xPixelsXSegment,3),dtype=outputType)
        
        

        for j in range(ySegments):
            for i in range(xSegments):
                allSegments[j,i]=frame[j*yPixelsYSegment:yPixelsYSegment*(j+1),i*xPixelsXSegment:xPixelsXSegment*(i+1)]

        return allSegments

    
    

    # This function takes a frame and returns the same frame with drawn segments
    def drawSegments(self,frame,ySegments,xSegments,bgrColor=(0,0,255),thickness=5,inputType="uint8"):
        
        frame=np.array(frame,dtype=inputType)

        frameShape=frame.shape
        
        if (len(frameShape) == 2 or len(frameShape) ==3):
            yPixels=frameShape[0]
            xPixels=frameShape[1]
            

            xPixelsXSegment=xPixels//xSegments
            yPixelsYSegment=yPixels//ySegments

        else:
            print("Wrong frame format (frame should be either n*m gray or n*m*3 colored image matrix)")
            return None

        yAxisLines=[i*xPixelsXSegment for i in range(1,xSegments)]
        xAxisLines=[i*yPixelsYSegment for i in range(1,ySegments)]


        for i in yAxisLines:
            frame=cv.line(frame,(i,0),(i,yPixels),bgrColor,thickness)

        for i in xAxisLines:
            frame=cv.line(frame,(0,i),(xPixels,i),bgrColor,thickness)


        return frame

    
   
    #This function convert numpy indexing to regular x and y indexing 
    #For example (4,1)=convertToXY(3,3,4,4)
    def convertToXY(self,row,col,ySegments,xSegments):
        if(col<xSegments and row<ySegments):
            x=col+1
            y=ySegments-row
            return x,y
        else:
            print("cordinats numbers out of range")
            return None

    
    
    #This function converts numpy indexing to only one number that describes the coordinates
    #This number starts from the bottom left and increses to the right. if it finishes the row
    #it will go up on and so on until it reaches to the upper right  
    #For example 8=convertToNumber(2,3,4,4)
    def convertToNumber(self,row,col,ySegments,xSegments):
        if (row <ySegments and col <xSegments):
            if row==ySegments-1:
                number=(col+1)
            else:
                number=(col+1)+(ySegments-row-1)*xSegments
            return number
        else:
            print("cordinats numbers out of range")
            return None

    #This function converts numpy indexing to be suitable with the pathfinding library
    #simply we switch between the columns and rows
    def convertToPathFinding(self,row,col,ySegments,xSegments):

        return (col,row)


    
    #Here is the opposite of convertToXY function which means it will take the x and y coordinates 
    #and convert them to numpy indexing
    def convertFromXY(self,x,y,ySegments,xSegments):
        
        if (x<=xSegments and y<=ySegments):
            row=ySegments-y
            col=x-1


        else:
            print("cordinats numbers out of range")
            return None

        return int(row),int(col)



    #Here is the opposite of convertToNumber function which means it will take a number 
    #and convert it to a numpy indexing    
    def convertFromOneNumber(self,number,ySegments,xSegments):
        pass
        if number%xSegments==0:
            row=ySegments-number/xSegments
            col=xSegments-1

        else:
            row=ySegments-number//xSegments-1
            col=number%xSegments-1

        return int(row), int(col)



    #same as the convertToXY function but takes a list and returns a list instead
    def convertToXYList(sef,listNumpy,ySegments,xSegments):
        
        thisClass=CVMainTopics()
        listResult=[]

        for i in range(len(listNumpy)):
            Result=thisClass.convertToXY(listNumpy[i][0],listNumpy[i][1],ySegments,xSegments)
            listResult.append(Result)

        return listResult



    #same as the convertToNumber function but takes a list and returns a list instead
    def convertToNumberList(sef,listNumpy,ySegments,xSegments):

        thisClass=CVMainTopics()
        listResult=[]

        for i in range(len(listNumpy)):
            Result=thisClass.convertToNumber(listNumpy[i][0],listNumpy[i][1],ySegments,xSegments)
            listResult.append(Result)

        return listResult

    
    #same as the convertToPathFinding function but takes a list and returns a list instead
    def convertToPathFindingList(sef,listNumpy,ySegments,xSegments):

        thisClass=CVMainTopics()
        listResult=[]

        for i in range(len(listNumpy)):
            Result=thisClass.convertToPathFinding(listNumpy[i][0],listNumpy[i][1],ySegments,xSegments)
            listResult.append(Result)

        return listResult

        



    def colorDetect(self,frame,hsvL,hsvU,blur=15):
        """
        frame= One frame image numpy matrix each element in the matrix contains
        three values from 0 to 255 in (b,g,r) (Note: in openCV it uses bgr insted of rgb)

        
        hsvL = lower HSV limit (h,s,v)
        hsvU = upper HSV limit (h,s,v)
        (h (Hue) from 0 to 360 which represint all the colors)
        (s (Saturation) from 0 to 100  percent (but in openCV it will be from 0 to 255)
        which represent the visibility or power of the color 0 persent not visible 
        (white if the v in (h,s,v) is not close to zero)
        100 persent is full color (if the v in (h,s,v) is not close to zero) )
        (v (Value) or brightness it is from 0 to 100 percent (but in openCV it will be from 0 to 255)
        (0 no brightness or black and 100 is bright) )

        mask= numpy matrix each element with only 0 and 255 values (0=black 255=white)
        """

        hsvFrame=cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        hsvFrame=cv.medianBlur(hsvFrame,blur)
        mask=cv.inRange(hsvFrame, hsvL, hsvU)
        return mask

    #Takes a black and white image and detects the parts of that image which are white in the segments
    #and then it will return the numpy indices that have a white color
    #Note: the detected white color depends on its area percentage of the segment  which could be specified by the 
    #parameter areaFraction
    #The last parameter is simply a description which will be assocciated with the output list
    #for example ["Some description", (3,3),(2,2),(0,0)]. this means that three white colors were detected
    #and their coordinates are like numpy coordinates for displaying a list 
    #(or simply a two dimensional list in python)
    #Note: this function is very important because basically in any image processing technic usually
    #one of the last results is to have a black and whit image 
    #for example in color detection, image detection or motion detections
    #the results will involve black and white
    def getPlace(self,bwframe,ySegments,xSegments,areaFraction=0.1,detectWhat="red"):
            segmintPixels=(bwframe.shape[0]//ySegments)*(bwframe.shape[1]//xSegments)

            indices=[detectWhat]

            allTheSegments=CVMainTopics.frameSegmentation(self,bwframe,ySegments,xSegments)
            for j in range(allTheSegments.shape[0]):
                for i in range(allTheSegments.shape[1]):
                 contours, hierarchy =  cv.findContours(allTheSegments[j,i],cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
                 for contour in  contours:
                     if cv.contourArea(contour)>areaFraction*segmintPixels:
                         indices.append([j,i])
                         break


            return indices


    
    





        


        


    



        

