emailok = False

while(not emailok):
    email = input("Input your email:")

    if "@" not in email:
        print ("Failed presence check, '@' needs to be included")
    elif "." in email[0]:
        print ("Failed presence check, no '.' at start")
    elif (email[len(email)-1]) == ("."):
        print ("Failed presence check, no '.' at end")
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
    else:
        passwordok = True

print ("Password accepted")
