monthlyPayment = 0
Month = 1
print ("How much would you like to add for this month?")
for Month in range(1,13):
    Money = (int(input(monthlyPayment)))
    monthlyPayment += Money
    
print ("In 12 months you have made" + (str(monthlyPayment)))


