import string

emailok = False

while(not emailok):
    email = input("Input your email:")

    atcount = 0
    for character in email:
        if (character == '@'):
            atcount += 1
        
    if atcount ==0:
        print ("Failed presence check, '@' needs to be included")
        continue
    elif atcount > 1:
        print ("Failed presence check, no more than one '@'")
        continue

    name, domain = email.split('@')

    if "." not in domain:
        print ("Failed format check, domain must have a '.'")
    elif domain[0] == '.':
        print ("Failed presence check, no '.' at the start of domain")
    elif (domain[len(domain)-1]) == ".":
        print ("Failed presence check, no '.' at the end of domain")
    elif name[0] == '.':
        print ("Failed presence check, no '.' at the start of name")
    elif (name[len(name)-1]) == ".":
          print ("Failed presence check, no '.' at the end of name") 
    elif ".." in email:
        print ("Failed presence check, no '..' in email")
    else:
        emailok = True
    
print ("Email accepted")

passwordok = False
while(not passwordok):
    password = input("Enter a password:")

    if len(password) < 6:
        print("Failed length check, password needs at least six characters")
        continue

    digits = 0
    upper = 0
    lower = 0
    punctuation = 0
    doubles = 0
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

    if digits == 0:
        print ("Failed presence check, no digits included")
    elif upper == 0:
        print ("Failed presence check, no uppercase letters included")
    elif lower == 0:
        print ("Failed presence check, no lowercase letters included")
    elif punctuation == 0:
        print ("Failed presence check, no punctuation included")
    elif doubles != 0:
        print ("Failed presence check, no double characters allowed")
    else:
        passwordok = True

print ("Password accepted")
