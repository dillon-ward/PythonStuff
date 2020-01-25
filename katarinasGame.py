import csv

def logUsersIn():
        users = ['', '']

        print("Player 1 log in")
        users[0] = logIn()
        print()
        print("Authorised login!")
        print()

        # As I didn't write the player's name in the procedure: I can use it for both
        print("Player 2 log in")
        users[1] = logIn()

        loggedIn2 = False # Verification
        while loggedIn2 == False:
                # This makes sure player 2 doesn't input the same login as player 1
                if users[1] == users[0]:
                        # If it's the same, they will have to enter a login again
                        print (users[0], " is already logged in!")
                        users[1] = logIn()
                else:
                        loggedIn2 = True
                        print ("Authorised login!")

        return users

def logIn():
        # This csv file cointains the usernames and passwords
        file = open("logins.csv")
        csv_file = csv.reader(file)
        logins = [] # A list is created to put the comma seperated values in
        # This will add the usernames with their passwords to the end of the list
        for row in csv_file:
                logins.append(row)

        loggedIn = False # Validation
        while loggedIn == False:
                username = input("Enter your username:")
                password = input("Enter your password:")
                # The code below will check if the logins exist (in the csv file)
                for login in logins: # Steps through each array in the array
                    # This checks if the username entered fits with its password
                        if username == login[0] and password == login[1]:
                                loggedIn = True
                                break # Loop is broken so it doesn't step through again
                if loggedIn == False:
                        print("Login FAILED!")
                        
        return username

asciiDice = [
[
"oooooooooooo",
"o          o",
"o          o",
"o    #     o",
"o          o",
"o          o",
"oooooooooooo"],
[
"oooooooooooo",
"o #        o",
"o          o",
"o          o",
"o          o",
"o        # o",
"oooooooooooo"],
[
"oooooooooooo",
"o #        o",
"o          o",
"o    #     o",
"o          o",
"o        # o",
"oooooooooooo"],
[
"oooooooooooo",
"o #      # o",
"o          o",
"o          o",
"o          o",
"o #      # o",
"oooooooooooo"],
[
"oooooooooooo",
"o #      # o",
"o          o",
"o    #     o",
"o          o",
"o #      # o",
"oooooooooooo"],
[
"oooooooooooo",
"o #      # o",
"o          o",
"o #      # o",
"o          o",
"o #      # o",
"oooooooooooo"]
]
     
# This is the menu screen the player gets when they log in
def menu():
    print()
    print("""               Menu
            1. Play Game
            2. View Highscores
            3. Quit""")
    print()

def anyKeyToContinue():
        print()
        print("Press any key to continue...")
        import msvcrt as m
        m.getch()
        print()

def dice():
    from random import randint
    roll = randint(1,6)# This shows a roll from a six sided dice
    return roll

def printDice(number):
        for line in range(7):
                print (asciiDice[number - 1][line])

def printTwoDice(number1, number2):
        for line in range(7):
                print (asciiDice[number1 - 1][line] + "     " + asciiDice[number2 - 1][line])        
          
def playerRoll(playerNum, playerName):
        print ("Player ", playerNum, " ", playerName, " roll!")

        anyKeyToContinue()
        
        # This uses the dice procedure to roll 2 dice for the player
        dice1 = dice()
        dice2 = dice()
        printTwoDice(dice1, dice2)

        total = dice1 + dice2

        if total % 2 == 0:
                print ("Bonus Points: +10!")
                total = total + 10
        else:
                print ("Odd! Lose 5 points!")
                total = total - 5

        if dice1 == dice2:
                print ("Double bonus roll!")
                anyKeyToContinue()
                dice3 = dice()
                printDice(dice3)
                total = total + dice3

        return total

def game(users):
        # Initialise the player points array
        playerPoints = [0,0]

        print()
        print("Game start!")

        # Players have 5 goes each
        for go in range(5):
                for player in range(2):
                        # goScore is the amount of points a player got that round
                        goScore = playerRoll(player + 1, users[player])
                        # This makes sure a player's score doesn't go below zero
                        playerPoints[player] = max(0, playerPoints[player] + goScore)
                        # This prints the total the player got that round and their score overall
                        print(users[player], "got", goScore, "points on that go and now has", playerPoints[player], "points in total")

        for player in range(2):
                # This prints the resulting scores of both players
                print("Player", player + 1, "has", playerPoints[player], "points")
        # The winner is the player with the highest score, if it's a draw then they roll until one gets higher
        winner = -1
        if playerPoints[0] > playerPoints[1]:
                winner = 0
                winScore = playerPoints[0]
        elif playerPoints[1] > playerPoints[0]:
                winner = 1
                winScore = playerPoints[1]
        else:
                # This will loop round until a player has a higher result 
                print ("Sudden Death!")
                while winner == -1:
                        tieScore = [0, 0]
                        for player in range(2):
                                print ("Player", player," ", users[player]," roll!")
                                anyKeyToContinue()
                                tieScore[player] = dice()
                        if tieScore[0] > tieScore[1]:
                                winner = 0
                                winScore = tieScore[0]
                        elif tieScore[1] > tieScore[0]:
                                winner = 1
                                winScore = tieScore[1]
        # This prints the winner of the game
        print (users[winner], "wins!")
        # This uploads the winner's name and score to a seperate file
        import csv
        winDetails = []
        file = open("Scores.csv", "a", newline="")
        csv_file = csv.writer(file)
        winDetails.append(users[winner])
        winDetails.append(winScore)
        csv_file.writerow(winDetails)
        file.close()
        print ("The winner's name and score have been uploaded to the score board")
        print ("Play again?")

def leaderboard():
        file = open("Scores.csv", "r")
        csv_file = csv.reader(file)
        sortedScores = sorted(csv_file, key = lambda row : int(row[1]), reverse = True)
        file.close()
        for row in sortedScores:
                print(row[0], row[1])
        
# Code in action
print("Katarina's Game!")
print()

users = logUsersIn()

quitMenu = False # Validation
while quitMenu == False:
    menu()
    choice = input("Select an option:")
    if choice == "1":
        game(users) # Option 1 will take you to the start of the game
    elif choice == "2": # Option 2 will take you to the highscores
        print()
        leaderboard()
        anyKeyToContinue()
    elif choice == "3": # Option 3 will quit the menu
        quitMenu = True
    else:
        print()
        print("That is not an option.")







