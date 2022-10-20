import math

class Snowplow:
    def __init__(self, unsortedStreet):
        if 0 not in unsortedStreet:
            unsortedStreet.append(0)
        
        self.snowplow = 0
        self.route = []
        self.street = sorted(unsortedStreet)

        startIndex = self.street.index(0)
        leftSublist = self.street[:startIndex]
        rightSublist = self.street[startIndex:]
        leftSublist.sort(reverse=True)
        rightSublist.remove(0)
        self.street.remove(0)

        streetLen = 0
        if leftSublist:
            streetLen += leftSublist[-1]*-1
        if rightSublist:
            streetLen += rightSublist[-1]
        maxDistance = math.ceil(streetLen * 0.01)
        
        self.rightClusters = []
        self.rightPriority = []
        if rightSublist:
            self.rightClusters = self.__clusterSides(rightSublist, maxDistance, False)
            self.rightPriority = sorted(self.rightClusters, key=len, reverse=True)

        self.leftClusters = []
        self.leftPriority = []
        if leftSublist:
            self.leftClusters = self.__clusterSides(leftSublist, maxDistance, True)
            self.leftPriority = sorted(self.leftClusters, key=len, reverse=True)

        self.totalClusterNum = len(self.rightClusters) + len(self.rightClusters)

    def __clusterSides(self, subList, maxDistance, left):
        cluster = []
        for house in subList:
            if not cluster:
                cluster.append([house])
            elif(left == False and (cluster[-1][-1] + maxDistance) >= house
                or left == True and (cluster[-1][-1] - maxDistance) <= house):
                cluster[-1].append(house)
            else:
                cluster.append([house])
        return cluster
    
    def __turnRight(self):
        self.snowplow = self.rightPriority[0][-1]
        passedIndex = self.rightClusters.index(self.rightPriority[0])
        for x in range(0, passedIndex+1):
            for y in self.rightClusters[0]:
                self.street.remove(y)
                self.route.append(y)
            del self.rightPriority[self.rightPriority.index(self.rightClusters[0])]
            del self.rightClusters[0]

    def __turnLeft(self):
        self.snowplow = self.leftPriority[0][-1]
        passedIndex = self.leftClusters.index(self.leftPriority[0])
        for x in range(0, passedIndex+1):
            for y in self.leftClusters[0]:
                self.street.remove(y)
                self.route.append(y)
            del self.leftPriority[self.leftPriority.index(self.leftClusters[0])]
            del self.leftClusters[0]
    
    def calculateDirection(self):
        distanceRight = self.rightPriority[0][0]
        distanceLeft = self.leftPriority[0][0]*-1

        if self.snowplow < 0:
            distanceRight += self.snowplow * -1
            distanceLeft -= self.snowplow * -1
        if self.snowplow >= 0:
            distanceRight -= self.snowplow
            distanceLeft += self.snowplow
        
        # 22
        # check distance to priority Block
        if distanceLeft < distanceRight:
            self.__turnLeft()
        elif distanceRight < distanceLeft:
            self.__turnRight()
        else:

            # check total size of blocks left on each side
            if len(self.leftPriority) > len(self.rightPriority):
                self.__turnLeft()
            elif len(self.rightPriority) > len(self.leftPriority):
                self.__turnRight()
            else:

                # check which side has the nearest house
                if self.street[0]*-1 < self.street[-1]:
                    self.__turnLeft()
                elif self.street[-1] < self.street[0]*-1:
                    self.__turnRight()
                else:

                    # check for previous direction
                    if self.snowplow < 0:
                        self.__turnLeft()
                    elif self.snowplow > 0:
                        self.__turnRight()
                    else:
                        self.__turnRight()
            


    def createRoute(self):
        for index in range(0, self.totalClusterNum):
            if not self.rightPriority and not self.leftPriority:
                break

            elif self.rightPriority and self.leftPriority:
                if len(self.leftPriority[0]) > len(self.rightPriority[0]):
                    self.__turnLeft()
                elif len(self.leftPriority[0]) < len(self.rightPriority[0]):
                    self.__turnRight()
                else:
                    self.calculateDirection()

            elif not self.rightPriority:
                self.__turnLeft()
            elif self.leftPriority:
                self.__turnRight()

    def getRoute(self):
        return self.route

def parcous(street):
    programm = Snowplow(street)
    programm.createRoute()
    return programm.getRoute()

# start env ".\..\tutorial-env\Scripts\activate.bat"