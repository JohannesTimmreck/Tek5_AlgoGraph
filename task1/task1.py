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

        totalStreetLength = 0
        if leftSide != []:
            totalStreetLength += leftSide[-1]*-1
        if rightSide != []:
            totalStreetLength += rightSide[-1]

        self.maxDistance = math.ceil(totalStreetLength / 10)
        
        print(self.street)
        if rightSide != []:
            self.rightBlocks = self.__clusterSides(rightSide, self.maxDistance, False)
            self.priorityRight = sorted(self.rightBlocks, key=len, reverse=True)
            self.totalClusterNum += len(self.rightBlocks)
        print(self.rightBlocks)
        print(self.priorityRight)

        if leftSide != []:
            self.leftBlocks = self.__clusterSides(leftSide, self.maxDistance, True)
            self.priorityleft = sorted(self.leftBlocks, key=len, reverse=True)
            self.totalClusterNum += len(self.leftBlocks)
        print(self.leftBlocks)
        print(self.priorityleft)
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
        print("passedIndex: ", passedIndex)
        for x in range(0, passedIndex+1):
            print("\t\tx:", x)
            for y in self.rightBlocks[0]:
                print("\t\t\ty:", y, ": ", self.rightBlocks[0])
                self.street.remove(y)
                self.route.append(y)
            del self.rightBlocks[0]
            del self.priorityRight[0]
        print("\tnewCluster: ", self.rightBlocks)
        print("\tnewStreet:", self.street)
        print("\tnewPlow:", self.snowplow)

    def __turnLeft(self, clusterIndex):
        self.snowplow = self.priorityleft[clusterIndex][-1]
        passedIndex = self.leftBlocks.index(self.priorityleft[clusterIndex])
        print("passedIndex: ", passedIndex)
        for x in range(0, passedIndex+1):
            print("\t\tx:", x)
            for y in self.leftBlocks[0]:
                print("\t\t\ty:", y, ": ", self.leftBlocks[0])
                self.street.remove(y)
                self.route.append(y)
            del self.leftBlocks[0]
            del self.priorityleft[0]
            print("\tnewCluster: ", self.leftBlocks)
            print("\tnewStreet:", self.street)
            print("\tnewPlow:", self.snowplow)

    def createRoute(self):
        rightIndex = 0
        leftIndex = 0
        for index in range(0, self.totalClusterNum):
            if rightIndex == -1 and leftIndex == -1:
                break
            elif rightIndex != -1 and leftIndex != -1:
                if len(self.priorityleft[leftIndex]) > len(self.priorityRight[rightIndex]):
                    print("left 1")
                    self.__turnLeft(leftIndex)
                    if not self.priorityleft:
                        leftIndex += -1
            
                elif len(self.priorityleft[leftIndex]) < len(self.priorityRight[rightIndex]):
                    print("right 1")
                    self.__turnRight(rightIndex)
                    if not self.priorityRight:
                        rightIndex += -1

                else:
                    # scan for closeness to snowplow and decide based on that
                    print("draw")
            elif rightIndex == -1:
                print("left 2")
                self.__turnLeft(leftIndex)
                if not self.priorityleft:
                    leftIndex += -1
            elif leftIndex == -1:
                print("right 2")
                self.__turnRight(rightIndex)
                if not self.priorityRight:
                    rightIndex += -1

    def getRoute(self):
        return self.route

def parcous(street):
    programm = Snowplow(street)
    programm.createRoute()
    print(programm.getRoute())
    return

            
list_street = [1, 5, 8, 10, -2, -9]

parcous(list_street)


# start env ".\..\tutorial-env\Scripts\activate.bat"