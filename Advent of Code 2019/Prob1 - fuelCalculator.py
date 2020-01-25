import csv
moduleFuel = []
totalFuel = 0

file = open("moduleMass.csv")
for row in file:
    count = int(int(row) / 3) - 2
    fuelNeeded = 0
    while count > 0:
        fuelNeeded += count
        count = int(count / 3) - 2
    moduleFuel.append(fuelNeeded)

for x in range (len(moduleFuel)):
    totalFuel += moduleFuel[x]

print (totalFuel)
         

