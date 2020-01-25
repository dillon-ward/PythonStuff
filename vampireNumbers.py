import random
count = 0
while count < 10:
    number1 = random.randint(0,10)
    number2 = random.randint(0,10)
    number3 = random.randint(0,10)
    number4 = random.randint(0,10)
    strNumber1 = str(number1) + str(number2)
    strNumber2 = str(number3) + str(number4)
    multiply = int(strNumber1) * int(strNumber2)
    total1 = str(number1)+ str(number2) + str(number3) + str(number4)
    total2 = str(number3)+ str(number4) + str(number1) + str(number2)
    total3 = str(number2)+ str(number3) + str(number4) + str(number1)
    total4 = str(number4)+ str(number1) + str(number2) + str(number3)
    if multiply == total1 or total1 or total2 or total3 or total4:
        print (strNumber1, 'x', strNumber2)
        count = count + 1
    
