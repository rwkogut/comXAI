def twoWayFilter(oneWayFile, twoWayFile, filterFile):
    oneWay = open(oneWayFile, "r")
    twoWay = open(twoWayFile, "r")
    filter = open(filterFile, "w")

    for line in twoWay:
        parts = line.split(",")
        flag = 0
        for line1 in oneWay:
            parts1 = line1.split(",")
            if parts1[0] == "0" and (parts[2] == parts1[2] or parts[3] == parts1[2]):
                flag = 1

        if flag == 0:
            filter.write(line)


def threeWayFilter(twoWayFile, threeWayFile, filterFile):
    threeWay = open(threeWayFile, "r")
    filter = open(filterFile, "w")

    for line in threeWay:
        parts = line.split(",")
        flag = 0
        twoWay = open(twoWayFile, "r")
        for line1 in twoWay:
            parts1 = line1.split(",")
            if parts1[0] == "0" and ((parts1[2] == parts[2] or parts1[2] == parts[3] or parts1[2] == parts[4]) and (parts1[3] == parts[2] or parts1[3] == parts[3] or parts1[3] == parts[4])):
                flag = 1

        if flag == 0:
            filter.write(line)

def fourWayFilter(twoWayFile, threeWayFile, filterFile):
    threeWay = open(threeWayFile, "r")
    filter = open(filterFile, "w")

    for line in threeWay:
        parts = line.split(",")
        flag = 0
        twoWay = open(twoWayFile, "r")
        for line1 in twoWay:
            parts1 = line1.split(",")
            if parts1[0] == "0" and ((parts1[2] == parts[2] or parts1[2] == parts[3] or parts1[2] == parts[4] or parts1[2] == parts[5]) and (parts1[3] == parts[2] or parts1[3] == parts[3] or parts1[3] == parts[4] or parts1[3] == parts[5]) and (parts1[4] == parts[2] or parts1[4] == parts[3] or parts1[4] == parts[4] or parts1[4] == parts[5])):
                flag = 1

        if flag == 0:
            filter.write(line)

def fiveWayFilter(twoWayFile, threeWayFile, filterFile):
    threeWay = open(threeWayFile, "r")
    filter = open(filterFile, "w")

    for line in threeWay:
        parts = line.split(",")
        flag = 0
        twoWay = open(twoWayFile, "r")
        for line1 in twoWay:
            parts1 = line1.split(",")
            if parts1[0] == "0" and ((parts1[2] == parts[2] or parts1[2] == parts[3] or parts1[2] == parts[4] or parts1[2] == parts[5] or parts1[2] == parts[6]) and (parts1[3] == parts[2] or parts1[3] == parts[3] or parts1[3] == parts[4] or parts1[3] == parts[5] or parts1[3] == parts[6]) and (parts1[4] == parts[2] or parts1[4] == parts[3] or parts1[4] == parts[4] or parts1[4] == parts[5] or parts1[4] == parts[6]) and (parts1[5] == parts[2] or parts1[5] == parts[3] or parts1[5] == parts[4] or parts1[5] == parts[5] or parts1[5] == parts[6])):
                flag = 1

        if flag == 0:
            filter.write(line)

#twoWayFilter("1WayresultsChimp.csv", "2WayresultsChimp.csv", "TestFilter.csv")
#threeWayFilter("2WayresultsChimp.csv", "3WayresultsChimp.csv", "TestFilter.csv")
fourWayFilter("ThreeWayChimpFilter.csv", "4WayresultsChimp.csv", "TestFilter.csv")