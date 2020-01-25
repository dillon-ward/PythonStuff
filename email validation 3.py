import string # Using 'import string' will import the constants that aren't built in
import csv


def validateEmail(email): # Using a function can use the code for later purposes
    emailok = False
    message = ''

    # Count the number of '@' characters in the email address. It should only contain 1
    atcount = 0 # Initialise atcount
    for character in email: # Look at each character in email in turn, store in 'character'
        if (character == '@'): # Is this character an '@'?
            atcount += 1 # Yes, add one to atcount
        
    if atcount == 0:
        message="Failed presence check, '@' needs to be included"
    elif atcount > 1:
        message="Failed presence check, no more than one '@'"
    else:
        name, domain = email.split('@') # This just splits the text at the one '@'

        if name == '':
            message = "Failed format check, name must not be blank"
        elif domain == '':
            message = "Failed format check, domain must not be blank"
        elif "." not in domain:
            message = "Failed format check, domain must have a '.'"
        elif domain[0] == '.':
            message = "Failed presence check, no '.' at the start of domain"
        elif (domain[len(domain)-1]) == ".": # This will pick out the last character of the string 
            message = "Failed presence check, no '.' at the end of domain"
        elif name[0] == '.':
            message = "Failed presence check, no '.' at the start of name"
        elif (name[len(name)-1]) == ".":
            message = "Failed presence check, no '.' at the end of name"
        elif ".." in email:
            message = "Failed presence check, no '..' in email"
        else:
            emailok = True
            message = "ok"

    return emailok, message

def validatePassword(password):
    passwordok = False
    message = ''

    if len(password) < 6:
        message="Failed length check, password needs at least six characters"

    else:
        digits = 0
        upper = 0
        lower = 0
        punctuation = 0
        doubles = 0
        # The characters are counted and classed
        for index, character in enumerate(password):   
            if(character.isdigit()):
                digits += 1
            elif character in string.punctuation:
                punctuation += 1
            elif character.isupper():
                upper += 1
            elif character.islower():
                lower += 1
            if index > 0 and password[index - 1] == character:
                doubles += 1
        # If any of the variables equal 0 then none of them have been entered in the password
        if digits == 0:
            message = "Failed presence check, no digits included"
        elif upper == 0:
            message = "Failed presence check, no uppercase letters included"
        elif lower == 0:
            messge = "Failed presence check, no lowercase letters included"
        elif punctuation == 0:
            message = "Failed presence check, no punctuation included"
        # If there is more than one type of character then the password is not accepted
        elif doubles != 0:
            message = "Failed presence check, no double characters allowed"
        else:
            passwordok = True
            message = "ok"

    return passwordok, message


file = open("password.csv")
csv_file = csv.reader(file)

for row in csv_file:
    #The functions are used to validate the emails and passwords
    print(row[0], validateEmail(row[0]))  
    print(row[1], validatePassword(row[1]))


