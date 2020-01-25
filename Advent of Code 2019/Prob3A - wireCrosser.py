def directionFunc(directions):
    x = 0
    y = 0
    coordinates = []
    for item in directions:
        instruction = item[0]
        if instruction == 'R':
            x += int(item[1:])
        elif instruction == 'L':
            x -= int(item[1:])
        elif instruction == 'U':
            y += int(item[1:])
        else:
            y -= int(item[1:])
        coordinates.append([x, y])
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

file1 = open("Pathway1.txt", "r")

for item in file1:
    firstDirections = item.rstrip().split(",")

firstWireCoordinates = directionFunc(firstDirections)

file2 = open("Pathway2.txt", "r")

for item in file2:
    secondDirections = item.rstrip().split(",")

secondWireCoordinates = directionFunc(secondDirections)

intersectList = []

manhattanDistance = []
lastFirst = [0, 0]
for first in firstWireCoordinates:
    lastSecond = [0, 0]
    for second in secondWireCoordinates:
        intersect = findIntersection(lastFirst, first, lastSecond, second)
        if intersect != None:
            intersectList.append(intersect)
            if intersect[0] < 0:
                intersect[0] *= -1
            if intersect[1] < 0:
                intersect[1] *= -1
            manhattanDistance.append(intersect[0] + intersect[1])
        lastSecond = second
    lastFirst = first

smallest = manhattanDistance[-1]
for x in manhattanDistance:
    if x < smallest:
        smallest = x
print (smallest)


        



