# This program lets you exchange an amount of money from one currency to another
# A csv is imported that holds the data of the currencies that you choose from
import csv

# Open the exchange rate file
file = open("GBPexchangeRate.csv")

# Create a CVS reader for the file
csv_file = csv.reader(file)

# Create an empty list to hold lines from the csv file
GBPexchangeRate = []

# Loop over lines in the CSV file
for row in csv_file:
    # Add the current csv line to the exchange rate list
    GBPexchangeRate.append(row)
    
# This function presents the user a question and asks the user to choose one
# of the currencies listed in the CSV file
# The chosen currency code is returned
def chooseCurrency(question):
    # Present the user with the question
    print (question)
    # Display a list of currencies to choose from
    for currency in GBPexchangeRate:
        print ("   " + currency[0] + ": " + currency[2] + " (" + currency[1] + ")")

    valid = False # Sets valid input flag to False
    while valid == False: # Loop until we have a valid input
        # Prompt for currency code
        choice = input("Enter a currency from the selection: ")
        # Convert to upper case
        choice = choice.upper()
        # Remove any leading and trailing spaces
        choice = choice.strip()
        # Look for the entered currency in the exchange rate list
        for currency in GBPexchangeRate:
            if choice == currency[0]:
                # Found the entered currency - set valid flag to True
                valid = True 
        
        if valid:
            # Display the chosen currency code
            print ("You have chosen", choice)
        else:
            # Tell the user the entered currency code is invalid
            print ("That currency is not valid")

    # Returns the chosen currency code                    
    return choice

# This function asks the user to enter a currency amount
# The input has to be a float in case pennies are involved
# Returns the amount as a float
def getAmount():
    valid = False # Sets valid input flag to False
    while valid == False: # Loop until we have a valid input
        # Prompts for float but is returned as string
        valstring = input("Enter the amount you want to exchange with decimal point: ")
        if isFloat(valstring): # Tests string is valid float
            # Valid float - set valid flag to True
            valid = True
            value = float(valstring) # Convert string to float
        else:
            # Tell the user the input is inavalid
            print("Enter a float.")
    # Return the float
    return value

# This function converts a currency amount for a given currency code in to GBP
# Returns the GBP value
def convertCurrencyToGBP(amount, fromCurrency):
    # Look for the currency code in the exchange rate list
    for currency in GBPexchangeRate:
        if fromCurrency == currency[0]:
            # Convert the currency value to GBP by dividing by the exchange rate
            result = amount / float(currency[3])
            break # This breaks out of the 'for' loop
    # Return the result
    return result

# This function converts a GBP amount to the given currency
# Returns the amount in the target currency
def convertGBPToCurrency(amount, toCurrency):
    # Look for the currency code in the exchange rate list
    for currency in GBPexchangeRate:
        if toCurrency == currency[0]:
            # Convert the GBP value to currency by multiplying by the exchange rate
            result = amount * float(currency[3])
            break # This breaks out of the 'for' loop
    # Return the result
    return result

# This function checks if an input is a float
# Returns True if the input string can be converted to a float, False otherwise
def isFloat(value):
    try:
        # If the input is a float return True
        float(value)
        return True
    except ValueError:
        # A ValueError returns False
        return False

# Ask the user which currency they want to convert from
fromCurrency = chooseCurrency("Which currency do you have?")
# Ask the user which currency they want to convert to
toCurrency = chooseCurrency("Which currency do you want?")
# Ask the user how much currency they want to convert
amount = getAmount()
# Convert the currency amount to GBP
amountInGBP = convertCurrencyToGBP(amount, fromCurrency)
# Converts the GBP amount to the target currency
toCurrencyAmount = convertGBPToCurrency(amountInGBP, toCurrency)

# Display the results
print(str(amount) + " in " + fromCurrency + " = " + str(toCurrencyAmount) + " in " +
      toCurrency)
