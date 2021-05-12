# this is for the functions that dont belong in any particular class but are usefull to the system
import sys
import random
import numpy as np

# for testing the map
def dictUpdate(mapDict, xSize, ySize, modType):
    totalNum = xSize * ySize
    amountArray = np.array([1,2,2]) #values of each without empty and normal

    mapDict['communication'] = 1
    mapDict['thruster'] = 2
    mapDict['photo'] = 2

    if modType == 'normal':
        mapDict['normal'] = totalNum - amountArray.sum()
        mapDict['empty'] = 0
    elif modType == 'empty':
        mapDict['empty'] = totalNum - amountArray.sum()
        mapDict['normal'] = 0
    elif modType == 'random':
        maxNumber = totalNum - amountArray.sum()
        randEmpty = random.randint(0, maxNumber)
        randNormal = maxNumber - randEmpty
        mapDict['empty'] = randEmpty
        mapDict['normal'] = randNormal
    
    return mapDict

#creates a non random map of the modueles
def createMap(arrayYSize, arrayXSize):
    mapArray = np.empty([arrayYSize, arrayXSize], dtype=np.str_)

    for j in range(arrayXSize):
        mapArray[0,j] = 'n'
    mapArray[1,0] = 'n'
    mapArray[1,1] = 'p'
    mapArray[1,2] = 'c'
    commPos = (1,2)

    mapArray[2,0] = 't'
    mapArray[2,1] = 'p'
    mapArray[2,2] = 'e'

    mapArray[3,0] = 'n'
    mapArray[3,1] = 'e'
    mapArray[3,2] = 't'


    return (mapArray, commPos)

#creates a random map of all of the modules TODO #4 autimate so that it fits within the size of the array
def createRandMap(arrayYSize, arrayXSize):
    k = 0
    moduleinitLimit = {
                'communication':1,
                'normal':5,
                'thruster':2,
                'photo':2,
                'empty':4
                }

    # updates the moduleLimit dictionary so that it is the appropriate size
    moduleLimit = dictUpdate(moduleinitLimit, arrayYSize, arrayXSize, 'random')
    
    moduleCnt = {
                'communication':0,
                'normal':0,
                'thruster':0,
                'photo':0,
                'empty':0
                }

    mapArray = np.empty([arrayYSize, arrayXSize], dtype=np.str_)

    for i in range(arrayYSize):
        for j in range(arrayXSize):
            cnt = 0 # this is to stop the while loop form being infinate
            while(k == 0):
                sensor, curValue = random.choice(list(moduleCnt.items()))
                maxValue = moduleLimit[sensor] # retrives the max value of the sensors
                # to see if the maximum number has been selected
                if maxValue > curValue:
                    mapArray[i,j] = sensor[0]
                    moduleCnt[sensor] += 1
                    if sensor == 'communication':
                        commPos = (i,j)
                    k = 1
                # uber 2.0 employee_part time worker
                elif(cnt >= (arrayXSize*arrayYSize)):
                    sys.exit("The system took to long to create map")

                cnt += 1
            k = 0

    return (mapArray, commPos)

# creates a list of y or x values [y, x]
def listXorYVal(arrayOfPos, XorY):
    # sets the value to either the first or second value
    if XorY == 'x':
        varCheck = 1
    else:
        varCheck = 0

    arrayOfVal = []
    for positionVal in arrayOfPos:
        arrayOfVal.append(positionVal[varCheck])
    
    return arrayOfVal
