def increasingNumbers(number):
    count = 0
    highest = 0
    for x in str(number):
        if int(x) >= highest:
            highest = int(x)
        else:
            count += 1
    if count == 0:
        return number

def doubleOccurrences(increasingNumber):
    for y in str(increasingNumber):
        double = y + y
        triple = y + y + y
        if double in str(increasingNumber) and triple not in str(increasingNumber):
            return increasingNumber
        
nextStep = []
possiblePasswords = []

for n in range (156218, 652527):
    firstPass = increasingNumbers(n)
    if firstPass:
        nextStep.append(firstPass)

for i in nextStep:
    secondPass = doubleOccurrences(i)
    if secondPass:
        possiblePasswords.append(secondPass)

print(len(possiblePasswords))


