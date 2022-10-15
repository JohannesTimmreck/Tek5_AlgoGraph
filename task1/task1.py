import math

class Snowplow:
    street = []
    route = []

    maxDistance = 0
    rightBlocks = []
    leftBlocks = []
    totalClusterNum = 0

    priorityRight = []
    priorityleft = []
    
    def __init__(self, neighborhood):
        if 0 not in neighborhood:
            neighborhood.append(0)
        self.route = []
        self.rightBlocks = []
        self.leftBlocks = []
        self.priorityRight = []
        self.priorityleft = []
        self.street = sorted(neighborhood)
        self.snowplow = self.street.index(0)

        leftSide = [ x for x in self.street[:self.snowplow]]
        leftSide.sort(reverse=True)
        rightSide = self.street[self.snowplow:]
        rightSide.remove(0)
        self.street.remove(0)
        self.snowplow = 0

        totalStreetLength = 0
        if leftSide != []:
            totalStreetLength += leftSide[-1]*-1
        if rightSide != []:
            totalStreetLength += rightSide[-1]

        self.maxDistance = math.ceil(totalStreetLength * 0.01)
        
        if rightSide != []:
            self.rightBlocks = self.__clusterSides(rightSide, self.maxDistance, False)
            self.priorityRight = sorted(self.rightBlocks, key=len, reverse=True)
            self.totalClusterNum += len(self.rightBlocks)

        if leftSide != []:
            self.leftBlocks = self.__clusterSides(leftSide, self.maxDistance, True)
            self.priorityleft = sorted(self.leftBlocks, key=len, reverse=True)
            self.totalClusterNum += len(self.leftBlocks)

    def __clusterSides(self, side, maxDistance, left):
        neighborhood = []
        for house in side:
            if not neighborhood:
                neighborhood.append([house])
            elif(left == False and (neighborhood[-1][-1] + maxDistance) >= house
                or left == True and (neighborhood[-1][-1] - maxDistance) <= house):
                neighborhood[-1].append(house)
            else:
                neighborhood.append([house])
        return neighborhood
    
    def __turnRight(self):
        self.snowplow = self.priorityRight[0][-1]
        passedIndex = self.rightBlocks.index(self.priorityRight[0])
        for x in range(0, passedIndex+1):
            for y in self.rightBlocks[0]:
                self.street.remove(y)
                self.route.append(y)
            del self.priorityRight[self.priorityRight.index(self.rightBlocks[0])]
            del self.rightBlocks[0]

    def __turnLeft(self):
        self.snowplow = self.priorityleft[0][-1]
        passedIndex = self.leftBlocks.index(self.priorityleft[0])
        for x in range(0, passedIndex+1):
            for y in self.leftBlocks[0]:
                self.street.remove(y)
                self.route.append(y)
            del self.priorityleft[self.priorityleft.index(self.leftBlocks[0])]
            del self.leftBlocks[0]
    
    def calculateDirection(self):
        distanceRight = self.priorityRight[0][0]
        distanceLeft = self.priorityleft[0][0]*-1

        if self.snowplow < 0:
            distanceRight += self.snowplow * -1
            distanceLeft -= self.snowplow * -1
        if self.snowplow >= 0:
            distanceRight -= self.snowplow
            distanceLeft += self.snowplow
        
        # check distance to priority Block
        if distanceLeft < distanceRight:
            self.__turnLeft()
        elif distanceRight < distanceLeft:
            self.__turnRight()
        else:

            # check total size of blocks left on each side
            if len(self.priorityleft) > len(self.priorityRight):
                self.__turnLeft()
            elif len(self.priorityRight) > len(self.priorityleft):
                self.__turnRight()
            else:

                # check which side has the nearest house
                if self.street[0]*-1 < self.street[-1]:
                    self.__turnLeft()
                elif self.street[-1] < self.street[0]*-1:
                    self.__turnRight()
                else:
                    self.__turnRight()
            


    def createRoute(self):
        areHousesRight = True if self.priorityRight else False
        areHousesLeft = True if self.priorityleft else False

        for index in range(0, self.totalClusterNum):
            if areHousesRight == False and areHousesLeft == False:
                break
            elif areHousesRight == True and areHousesLeft == True:
                if len(self.priorityleft[0]) > len(self.priorityRight[0]):
                    self.__turnLeft()
                    if not self.priorityleft:
                        areHousesLeft = False
            
                elif len(self.priorityleft[0]) < len(self.priorityRight[0]):
                    self.__turnRight()
                    if not self.priorityRight:
                        areHousesRight = False

                else:
                    self.calculateDirection()
                    if not self.priorityleft:
                        areHousesLeft = False
                    if not self.priorityRight:
                        areHousesRight = False
            elif areHousesRight == False:
                self.__turnLeft()
                if not self.priorityleft:
                    areHousesLeft = False
            elif areHousesLeft == False:
                self.__turnRight()
                if not self.priorityRight:
                    areHousesRight = False

    def getRoute(self):
        return self.route

def parcous(street):
    programm = Snowplow(street)
    programm.createRoute()
    return programm.getRoute()

# start env ".\..\tutorial-env\Scripts\activate.bat"