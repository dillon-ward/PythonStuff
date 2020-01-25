def directionFunc(directions):
    x = 0
    y = 0
    dist = 0
    coordinates = []
    for item in directions:
        instruction = item[0]
        length = int(item[1:])
        if instruction == 'R':
            x += length
        elif instruction == 'L':
            x -= length
        elif instruction == 'U':
            y += length
        else:
            y -= length
        dist += length
        coordinates.append([x, y, dist])
    return coordinates


def findIntersection(c1, c2, c3, c4):
    if c1[0] == c2[0]:
        # Vertical line
        if c3[0] != c4[0]:
            # Other is horizontal - do they intersect?
            x1h = min(c3[0], c4[0])
            x2h = max(c3[0], c4[0])
            y1v = min(c1[1], c2[1])
            y2v = max(c1[1], c2[1])
            x = c1[0]
            y = c3[1]
            if x1h <= x and x <= x2h and y1v <= y and y <= y2v:
                return [x, y]
    else:
        # Horizontal line
        if c3[1] != c4[1]:
            # Other is vertical - do they intersect?
            x1h = min(c1[0], c2[0])
            x2h = max(c1[0], c2[0])
            y1v = min(c3[1], c4[1])
            y2v = max(c3[1], c4[1])
            x = c3[0]
            y = c1[1]
            if x1h <= x and x <= x2h and y1v <= y and y <= y2v:
                return [x, y]
    return None

def intersectDist(intersect, coordinates):
    return abs(intersect[0] - coordinates[0]) + abs(intersect[1] - coordinates[1])

file1 = open("Pathway1.txt", "r")

for item in file1:
    firstDirections = item.rstrip().split(",")

firstWireCoordinates = directionFunc(firstDirections)

file2 = open("Pathway2.txt", "r")

for item in file2:
    secondDirections = item.rstrip().split(",")

secondWireCoordinates = directionFunc(secondDirections)

lowest = -1
lastFirst = [0, 0, 0]
for first in firstWireCoordinates:
    lastSecond = [0, 0, 0]
    for second in secondWireCoordinates:
        intersect = findIntersection(lastFirst, first, lastSecond, second)
        if intersect != None:
            print(intersect, lastFirst, lastSecond)
            intersectDist1 = intersectDist(intersect, lastFirst)
            intersectDist2 = intersectDist(intersect, lastSecond)
            totDist = abs(intersectDist1) + abs(intersectDist2) + lastFirst[2] + lastSecond[2]
            print (totDist)
            if lowest == -1 or totDist < lowest:
                lowest = totDist
        lastSecond = second
    lastFirst = first

print(lowest)
