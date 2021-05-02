import random
import numpy as np
import robModule as robm
import auxFunctions as auxf
# to start Ctrl+Shift+' venv terminal
# this class stores all of the modules as a map
class distNetwork:
    delta = {
        'W': (-1,0), 
        'E': (1,0),
        'S': (0,1),
        'N': (0,-1)
    }

    # array of modules
    def __init__(self):
        self.arrayXSize = 3
        self.arrayYSize = 4
        self.commPos = (0, 0) # y , x
        self.modArray = []
        # np arrays are y then x
        self.mapArray = np.empty([self.arrayYSize, self.arrayXSize], dtype=np.str_)

    # returns the module at position x,y
    def modAt(self, y, x):
        return self.modArray[y][x]
    
    # this is to have each node check if it has neighbors 
    def findValidNeighbours(self, curMod):
        neighbors = []

        # goes throught the list above and returns the values to change the shift by
        for direction, (dx,dy) in self.delta.items():
            neighborX, neighborY = curMod.xPos + dx, curMod.yPos + dy
            # makes sure that the module is in the range
            if (0 <= neighborX < self.arrayXSize) and (0 <= neighborY < self.arrayYSize):
                neighbor = self.modAt(neighborY, neighborX)
                # if neighbor.hasAllSides():
                neighbors.append((direction, neighbor))
        # this is working
        return neighbors

    # set up communications between modules
    def createConnectionsModule(self, curModule):
        # gets the neibouring modules and directions
        neighbours = self.findValidNeighbours(curModule)

        # checks if sensor is not set to empty
        if curModule.sensor != 'e':
            # checks if it is the communications module if it is set its distance to 0
            if curModule.sensor == 'c':
                curModule.distFromComms = 0
            
            for i in range(len(neighbours)):
                direction, neighbour = neighbours[i]
                # skips if the neighbor sensor is empty
                if neighbour.sensor != 'e':
                    neighbour.sides[robm.robModule.sidePairs[direction]] = True
                    curModule.sides[direction] = True

    # create network of connections
    def setUpNetworkComs(self):
        for i in range(self.arrayYSize):
            for j in range(self.arrayXSize):
                tempModule = self.modAt(i, j)
                self.createConnectionsModule(tempModule)

    #reads through the input map array and creates the appropriate module object
    # def createNetwork(self, inputMap):
    def createNetwork(self):
        directionList = ['N', 'E', 'S', 'W', 'U', 'D']
        # creates map and assigns it to the array and communication position
        # self.mapArray, self.commPos = auxf.createRandMap(self.arrayYSize, self.arrayXSize)
        self.mapArray, self.commPos = auxf.createMap(self.arrayYSize, self.arrayXSize)
        for i in range(self.arrayYSize):
            tempArray = []
            for j in range(self.arrayXSize):
                # gets the module in the position
                modVal = self.mapArray[i,j]
                tempMod = self.createModule(i,j,modVal)
                tempMod.yPos, tempMod.xPos = i, j # changes the x and y positions
                tempMod.distFromComms = self.arrayXSize * self.arrayYSize + 1
                tempMod.sensorDir = random.choice(directionList)
                tempArray.append(tempMod) 
            self.modArray.append(tempArray)
        self.setUpNetworkComs()
        self.mapUpdate()

    # creates a module and returns the created module
    def createModule(self, yInput, xInput, storedVal):
        # name is in the form x_y_sensorval
        name = str(xInput) + "_" + str(yInput) + "_" + str(storedVal)
        tempModule = robm.robModule(name, storedVal)
        tempModule.comUpdate()
        
        return tempModule

    # this updates the discance from every module
    def mapUpdate(self):
        # delta is a dictionary storing the direction and the corisponding direction change

        comY, comX = self.commPos
        stack = [] # this stores all of the modules that need to be checked
        stack.append(self.modAt(comY,comX))
        while len(stack) != 0:
            currentMod = stack.pop()
            numberOfSteps = currentMod.distFromComms + 1

            for direction, (dx, dy) in self.delta.items():
                #checks if there is a connection at this module
                if currentMod.sides[direction] == True:
                    yValue = currentMod.yPos + dy
                    xValue = currentMod.xPos + dx
                    nextMod = self.modAt(yValue, xValue)
                    if nextMod.distFromComms > numberOfSteps:
                        nextMod.distFromComms = numberOfSteps
                        nextMod.dirToComms = nextMod.sidePairs[direction]
                        stack.append(nextMod)
                    # TODO add to stack and find way to stop infinate loop

    # finds the position or all the modules of a given type
    def findComponentPos(self, component):
        # outputs this as a 2d array storing the position
        posArray = []
        for i in range(self.arrayYSize):
            for j in range(self.arrayXSize):
                # y and x
                tempArray = []
                sensor = self.modArray[i][j].sensor.casefold()

                # makes sure that camera and communication don't get confused
                if sensor == component[0] and component.casefold() != 'camera':
                    tempArray.append(i)
                    tempArray.append(j)
                    posArray.append(tempArray)
                elif component == 'camera':
                    if sensor == 'p':
                        tempArray.append(i)
                        tempArray.append(j)
                        posArray.append(tempArray)
        return posArray

