import ontoload as oL

# appends to a file the initial network map
def writeMap(fileString, networkMap):
    # opens the file object to append
    f = open(fileString, "a")
    for i in range(networkMap.arrayYSize):
        for j in range(networkMap.arrayXSize):
            f.write(networkMap.modArray[i][j].name)
            f.write(" Dir: ")
            if networkMap.modArray[i][j].sensor == 'e':
                f.write(" ")
            else:
                f.write(networkMap.modArray[i][j].sensorDir)            
            f.write("   ")
        f.write("\n")
    f.write("\n")
    f.close()

#gets the text input for the rearrangment
def inputRead():
    # for testing pourposes the input file will be in .txt file
    fileName = "inputFile.txt"
    f = open(fileName, "r")
    # reads the input
    response = f.read()
    # print(response)
    return response

# opens the text file and writes down the title
def writeMain(networkMap, fileStr):
    f = open(fileStr, "w+")
    f.write("This is the current map of the network;\n\n")
    f.close()

    writeMap(fileStr, networkMap)

# writes the introduction and changes the elements
def writeUpdated(fileStr, networkMap, response):
    element, direction = networkMap.inputOntoCheck(response)
    currentY, currentX, finalY, finalX = networkMap.changeModAndDir(element, direction)
    introText = f"This is the updated map of the network, the {element} was requested to point {direction};\n"
    modulePosText = f"The module was originally at ({currentX}, {currentY}) and was moved to ({finalX}, {finalY})\n\n"
    
    f = open(fileStr, "a")
    f.write(introText)
    f.write(modulePosText)
    f.close()
    writeMap(fileStr, networkMap)

networkMap = oL.ontoNet()
networkMap.createNetwork()
networkMap.createOntoMap()

fileStr = "outputFile.txt" 
writeMain(networkMap, fileStr)
response = inputRead()
writeUpdated(fileStr, networkMap, response)
