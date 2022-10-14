import math

class Snowplow:
    street = []
    route = []
    maxDistance = 0
    rightBlocks = []
    leftBlocks = []
    totalClusterNum = 0

    currentPosition = 0
    priorityRight = []
    priorityleft = []
    
    def __init__(self, neighborhood):
        if 0 not in neighborhood:
            neighborhood.append(0)
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

        self.maxDistance = math.ceil(totalStreetLength / 40)
        
        #print(self.street)
        if rightSide != []:
            self.rightBlocks = self.__clusterSides(rightSide, self.maxDistance, False)
            self.priorityRight = sorted(self.rightBlocks, key=len, reverse=True)
            self.totalClusterNum += len(self.rightBlocks)
        #print(self.rightBlocks)
        #print(self.priorityRight)

        if leftSide != []:
            self.leftBlocks = self.__clusterSides(leftSide, self.maxDistance, True)
            self.priorityleft = sorted(self.leftBlocks, key=len, reverse=True)
            self.totalClusterNum += len(self.leftBlocks)
        #print(self.leftBlocks)
        #print(self.priorityleft)
        pass

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
    
    def __turnRight(self, clusterIndex):
        self.snowplow = self.priorityRight[clusterIndex][-1]
        passedIndex = self.rightBlocks.index(self.priorityRight[clusterIndex])
        #print("passedIndex: ", passedIndex)
        for x in range(0, passedIndex+1):
            #print("\t\tx:", x)
            for y in self.rightBlocks[0]:
                #print("\t\t\ty:", y, ": ", self.rightBlocks[0])
                self.street.remove(y)
                self.route.append(y)
            del self.rightBlocks[0]
            del self.priorityRight[0]
        #print("\tnewCluster: ", self.rightBlocks)
        #print("\tnewStreet:", self.street)
        #print("\tnewPlow:", self.snowplow)

    def __turnLeft(self, clusterIndex):
        self.snowplow = self.priorityleft[clusterIndex][-1]
        passedIndex = self.leftBlocks.index(self.priorityleft[clusterIndex])
        #print("passedIndex: ", passedIndex)
        for x in range(0, passedIndex+1):
            #print("\t\tx:", x)
            for y in self.leftBlocks[0]:
                #print("\t\t\ty:", y, ": ", self.leftBlocks[0])
                self.street.remove(y)
                self.route.append(y)
            del self.leftBlocks[0]
            del self.priorityleft[0]
            #print("\tnewCluster: ", self.leftBlocks)
            #print("\tnewStreet:", self.street)
            #print("\tnewPlow:", self.snowplow)
    
    def calculateDirection(self, leftIndex, rightIndex):
        # if both are equal
        # check distance to both

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
            self.__turnLeft(leftIndex)
        elif distanceRight < distanceLeft:
            self.__turnRight(rightIndex)
        else:

            # check total size of blocks left on each side
            if len(self.priorityleft) > len(self.priorityRight):
                self.__turnLeft(leftIndex)
            elif len(self.priorityRight) > len(self.priorityleft):
                self.__turnRight(rightIndex)
            else:

                # check which side has the nearest house
                if self.street[0]*-1 < self.street[-1]:
                    self.__turnLeft(leftIndex)
                elif self.street[-1] < self.street[0]*-1:
                    self.__turnRight(rightIndex)
                else:
                    self.__turnRight(rightIndex)
            


    def createRoute(self):
        rightIndex = 0 if self.priorityRight else -1
        leftIndex = 0 if self.priorityleft else -1

        for index in range(0, self.totalClusterNum):
            if rightIndex == -1 and leftIndex == -1:
                break
            elif rightIndex != -1 and leftIndex != -1:
                if len(self.priorityleft[leftIndex]) > len(self.priorityRight[rightIndex]):
                    #print("left 1")
                    self.__turnLeft(leftIndex)
                    if not self.priorityleft:
                        leftIndex += -1
            
                elif len(self.priorityleft[leftIndex]) < len(self.priorityRight[rightIndex]):
                    #print("right 1")
                    self.__turnRight(rightIndex)
                    if not self.priorityRight:
                        rightIndex += -1

                else:
                    # scan for closeness to snowplow and decide based on that
                    #print("draw")
                    self.calculateDirection(leftIndex, rightIndex)
                    if not self.priorityRight:
                        rightIndex += -1
                    if not self.priorityleft:
                        leftIndex += -1
            elif rightIndex == -1:
                #print("left 2")
                self.__turnLeft(leftIndex)
                if not self.priorityleft:
                    leftIndex += -1
            elif leftIndex == -1:
                #print("right 2")
                self.__turnRight(rightIndex)
                if not self.priorityRight:
                    rightIndex += -1

    def getRoute(self):
        return self.route

def parcous(street):
    programm = Snowplow(street)
    programm.createRoute()
    #print(programm.getRoute())
    return programm.getRoute()

            
list_street = [-18, -16, -4, -2, 8, 12, 14, 16, 18]

def evaluateRoute(route):
    previousHouse = 0
    timeTaken = 0
    totalTime = 0

    for i in range(0, len(route)):
        if route[i] >= 0 and previousHouse >= 0:
            timeTaken += route[i] - previousHouse
        elif route[i] >= 0 and previousHouse < 0:
            timeTaken += (previousHouse*-1) + route[i]
        elif route[i] < 0 and previousHouse < 0:
            timeTaken += (route[i]*-1)  - (previousHouse*-1)
        elif route[i] < 0 and previousHouse >= 0:
            timeTaken += previousHouse + (route[i]*-1)
        previousHouse = route[i]
        totalTime += timeTaken
        #print(timeTaken)
    #print("totalTime: ", totalTime)
    print("algorythm: ", totalTime/len(route))


# start env ".\..\tutorial-env\Scripts\activate.bat"