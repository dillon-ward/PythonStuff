import csv
file = open("logins.csv")
csv_file = csv.reader(file)
logins = []
for row in csv_file:
    logins.append(row)
#logins = [['username1', 'password1'], ['username2', 'password2']]


loggedIn = False
while loggedIn == False:
    username = input("Enter your username:")
    password = input("Enter your password:")

    for login in logins:
        if username == login[0] and password == login[1]:
            print("Authorised login!")
            loggedIn = True
            break




