import moduleBase as mB

class printNet(mB.distNetwork):

    # print the origional map
    def printMap(self):
        print(self.mapArray)

    # # displays the names of the array 
    def printNetwork(self):
        for i in range(self.arrayYSize):
            for j in range(self.arrayXSize):
                print(self.modArray[i][j].name, end = '  ')
            print()

    # displays the network with the sides
    def printNetworkSides(self):
        for i in range(self.arrayYSize):
            for j in range(self.arrayXSize):
                print(self.modArray[i][j].sides, end = '  ')
            print()

    def printDistValues(self):
        for i in range(self.arrayYSize):
            for j in range(self.arrayXSize):
                print(self.modArray[i][j].distFromComms, end = ',')
                print(self.modArray[i][j].dirToComms, end=',')
                print(self.modArray[i][j].sensor, end=' ')
            print()
    
    def printNumPy(self):
        print(self.mapArray)        

    def printNullVal(self):
        for i in range(self.arrayYSize):
            for j in range(self.arrayXSize):
                checkVar = self.modArray[i][j].sensor
                if checkVar == 'e':
                    print("  ", end = ' ')
                else:
                    print(checkVar, end="")
                    print(self.modArray[i][j].sensorDir, end=" ")
            print()
