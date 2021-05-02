import sys
import random
import moduleBase as mB
import auxFunctions as auxf
import owlready2

owlready2.JAVA_EXE = "C:\Program Files\Java\jdk-13.0.2\\bin\java.exe"

# creates a corrisponding ontological map
class ontoNet(mB.distNetwork):

    def __init__(self):
        mB.distNetwork.__init__(self)
        self.ontoArray = []
        self.cameraCnt = 0
        self.thrusterCnt = 0
        self.onto = owlready2.get_ontology("file://ontofilepls").load()

    def testFunct(self):
        i = 3
        j = 4
        name = f"camera{i}{j}"
        camMod = self.onto.SensorModule(name, namespace = self.onto, has_for_sensor = [self.onto.Camera])
        motMod = self.onto.ActuatorModule("thruster", namespace = self.onto, has_for_actuator = [self.onto.Thruster], has_for_direction = [self.onto.North])
        comMod = self.onto.CommunicationModule("comm", namespace = self.onto, is_communication = [True])
        # for i in self.onto.Module.instances(): print(i)
        
        print(comMod.is_communication)
        print(motMod.has_for_direction)
 
    # # displays the names of the array 
    def printNetwork(self):
        for i in range(self.arrayYSize):
            for j in range(self.arrayXSize):
                print(self.modArray[i][j].name, end = '  ')
            print()

    def createOntoMap(self):
        dirDictionary = {
            'N':self.onto.North,
            'E':self.onto.East,
            'S':self.onto.South,
            'W':self.onto.West,
            'U':self.onto.Up,
            'D':self.onto.Down
        }

        for i in range(self.arrayYSize):
            tempArray = []
            for j in range(self.arrayXSize):
                sensorVal = self.modArray[i][j].sensor
                if sensorVal != 'e':
                    directionVal = self.modArray[i][j].sensorDir
                    if sensorVal == 'p':# photo is the name of the sensor
                        name = f"camera{i}{j}"
                        tempArray.append(self.onto.SensorModule(name, namespace = self.onto, has_for_sensor = [self.onto.Camera], has_for_direction = [dirDictionary[directionVal]]))
                    elif sensorVal == 'c':# communication module so no direction
                        name = f"communication{i}{j}"
                        tempArray.append(self.onto.CommunicationModule(name, namespace = self.onto, is_communication = [True]))
                    elif sensorVal == 't':# thruster module where the direction of the thruster is stored
                        name = f"thruster{i}{j}"
                        tempArray.append(self.onto.ActuatorModule(name, namespace = self.onto, has_for_sensor = [self.onto.Camera], has_for_direction = [dirDictionary[directionVal]]))
                    else:
                        name = f"normal{i}{j}"
                        tempArray.append(self.onto.Module(name, namespace = self.onto))
                else:
                    tempArray.append(0) # this adds a zero to the place where there is an empty module
            self.ontoArray.append(tempArray)

    # displays the name and direction of elements in an ontology
    def displayOnto(self):
        for i in range(self.arrayYSize):
            for j in range(self.arrayXSize):
                print(self.ontoArray[i][j].name, end=" ")
                print(self.ontoArray[i][j].has_for_direction , end="   ")
            print()

    # Checks if the words are in the ontology
    def inputOntoCheck(self, inputStr):
        # this is a dictionary storing the misc direction values
        directionDic = {
                        "forward"   : "North",
                        "forwards"  : "North",
                        "backwards" : "South",
                        "backward"  : "South",
                        "back"      : "South",
                        "left"      : "West",
                        "right"     : "East"
        }
        # lists all of the classes in the ontology
        classFullList = list(self.onto.classes())

        # lists all of the direction classes
        dirClassList = list(self.onto.Direction.subclasses())

        # splits the inputted string into individual words
        arrayWords = inputStr.split()

        # finds which word from the inputted string matches to an object class
        for element in classFullList:
            if element.name.casefold() in arrayWords:
                # finds the element that is in there
                # print(element.name.casefold())
                modElement = element.name.casefold()
        
        # finds which directional instruction is in the command
        for testWord in arrayWords:
            for dirElement in dirClassList:
                # checking if direction was mentioned
                if testWord.casefold() == dirElement.name.casefold():
                    dirValue = testWord.casefold()
            if testWord in directionDic.keys():
                dirValue = directionDic[testWord]

        # returns the element and the direction of said element
        return [modElement, dirValue]

            
    # Removes the ontofilepls. part of the classes to allow for cheacking
    def removeFormatOnto(self):
        classFullList = list(self.onto.classes())
        lengthList = len(classFullList)
        # tempArray = []

        #goes through each element in classFullList and seperates each value at the '.'
        for element in classFullList:
            print(element.name.casefold())
            # tempvar = element.split(".",-1) # splits words at period

            # tempArray.append(tempvar[1])
            # print(tempvar)

    # Finds largest or smallest value depending on the input input map
    def findDirValueIndex(self, arrayIn, direction):
        # if it is north or up find the smallest Y value
        if direction == "North" or direction == "South" :
            # finds the y values of array
            yValues = auxf.listXorYVal(arrayIn, "y")
            if direction == "South":
                indexVal = yValues.index(max(yValues))
            else:
                indexVal = yValues.index(min(yValues))
                
            return arrayIn[indexVal]
        # this is for east and west
        elif direction == "East" or direction == "West":
            xValues = auxf.listXorYVal(arrayIn, "x")
            if direction == "East":
                indexVal = xValues.index(max(xValues))
            else:
                indexVal = xValues.index(min(xValues))

            return arrayIn[indexVal]
        # for Up and Down 
        else:
            return random.choice(arrayIn)


    # Finds the module position best suited for the command
    def findModEndPos(self, module, direction):
        # finds the positions of all of the modules of a type
        positionArray =  self.findComponentPos(module)
        # returns the x and y values of the nearest to desired value
        curYVal, curXVal = self.findDirValueIndex(positionArray, direction)
        finYVal, finXVal = curYVal, curXVal
        # sets the directional value to the appropriate one
        if direction == 'North':
            finYVal = 0
        elif direction == 'East':
            finXVal = self.arrayXSize - 1
        elif direction == 'South':
            finYVal = self.arrayYSize - 1
        elif direction == 'West':
            finXVal = 0

        return curYVal, curXVal, finYVal, finXVal

    # changes the direction values of the module that is stored
    def changeDir(self, yPos, xPos, direction):
        dirDictionary = {
            'N':self.onto.North,
            'E':self.onto.East,
            'S':self.onto.South,
            'W':self.onto.West,
            'U':self.onto.Up,
            'D':self.onto.Down
        }

        # change direction for the onotology
        self.ontoArray[yPos][xPos].has_for_direction.clear()
        self.ontoArray[yPos][xPos].has_for_direction.append(dirDictionary[direction[0]])

        # change the direction in the module array
        self.modArray[yPos][xPos].sensorDir = direction[0]
        # print(self.ontoArray[yPos][xPos].get_properties())

    # changes the modules positions in the array
    def changeModPos(self, currentPos, finPos):
        if currentPos != finPos:
            yCur, xCur = currentPos
            yFin, xFin = finPos

            self.modArray[yCur][xCur], self.modArray[yFin][xFin] = self.modArray[yFin][xFin], self.modArray[yCur][xCur]
            self.ontoArray[yCur][xCur], self.ontoArray[yFin][xFin] = self.ontoArray[yFin][xFin], self.ontoArray[yCur][xCur]

    def changeModAndDir(self, moduleType, direction):
        currentY, currentX, finalY, finalX = self.findModEndPos(moduleType, direction)
        self.changeDir(currentY, currentX, direction)
        self.changeModPos((currentY, currentX), (finalY, finalX))
        return currentY, currentX, finalY, finalX

networkMap = ontoNet()
networkMap.createNetwork()
networkMap.createOntoMap()
networkMap.changeModAndDir('camera', 'West')
# print(networkMap.inputOntoCheck("Point the thruster back"))
# print(networkMap.findComponentPos('camera'))
# networkMap.removeFormatOnto()