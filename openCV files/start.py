import coe510cv as c

ySegments=c.ySegments
xSegments=c.xSegments

path=input("Image full path (Note: put \\\ insted of \\) : ")

result2=c.imageColorDetection(path)

result1=c.motionDetection()

result3=c.cameraColorDetection()




#https://www.youtube.com/watch?v=jTYiNjvnHZY




while True:

    try:
        numpyList = next(result2)


        resultXY=[]
        resultXY.append(numpyList[0])

        
        resultXY.append(c.general.convertToXYList(numpyList[1:],ySegments,xSegments))


        print(resultXY)

    except StopIteration:
        break


while True:

    try:
        numpyList = next(result1)


        resultXY=[]
        resultXY.append(numpyList[0])

        
        resultXY.append(c.general.convertToXYList(numpyList[1:],ySegments,xSegments))


        print(resultXY)

    except StopIteration:
        break



while True:

    try:
        numpyList = next(result3)


        resultXY=[]
        resultXY.append(numpyList[0])

        
        resultXY.append(c.general.convertToXYList(numpyList[1:],ySegments,xSegments))


        print(resultXY)

    except StopIteration:
        break

