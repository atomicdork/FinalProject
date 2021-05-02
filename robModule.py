# here the basic information of a module is stored
class robModule:
    sidePairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    moduleinitLimit = {
            'communication':'c',
            'normal':'n',
            'thruster':'t',
            'photo':'p',
            'empty':'e'
            }

    def __init__(self, name, sensor):
        self.name = name
        self.sensor = sensor
        self.xPos = 0 # this is just for cleaner code not to be used to know where it is
        self.yPos = 0 # see above comment
        self.assumedPos = [0,0] # this gets updated as each neighbour is shifted y,x
        self.assumedSource = 'S' # this is for the tracing
        #TODO use the buffer to 
        self.trupleBuffer = [0,0] # used to pass truples
        self.isComms = False # is it the communications module
        self.distFromComms = 100 # this is the distance form the communications module
        self.dirToComms = 'S' # this points to the module from which it was sent
        self.sides = {'N': False, 'S': False, 'E': False, 'W': False} #if there is a module attached to the side
        self.sensorDir = 'N' # controlling the direction that the sensor is pointing

    # changes the variables based on sensor
    def comUpdate(self):
        if self.sensor == 'c':
            self.isComms = True
            self.distFromComms = 0

    # returns all of the sides
    def hasAllSides(self):
        return not any(self.sides.values())

    # creates a connection between sides
    def allowSideConnection(self, other, side):
        self.sides[side] = False
        other.sides[robModule.sidePairs[side]] = False
