import ontoload as oL

# appends to a file the initial network map
def writeMap(fileString, networkMap):
    # opens the file object to append
    f = open(fileString, "a")
    for i in range(networkMap.arrayYSize):
        for j in range(networkMap.arrayXSize):
            f.write(networkMap.modArray[i][j].name)
            f.write("  ")
        f.write("\n")
    f.write("\n")
    f.close()

# opens the text file and writes down the title
def writeMain():
    fileStr = "outputFile.txt" 
    f = open(fileStr, "w+")
    f.write("This is the current map of the network;\n")
    f.close()

    networkMap = oL.ontoNet()
    networkMap.createNetwork()
    networkMap.createOntoMap()

    writeMap(fileStr, networkMap)
