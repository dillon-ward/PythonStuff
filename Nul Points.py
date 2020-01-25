# Import the random library so we can generate random integers with randint()
import random

# This function will return a random integer from 1 to 6
def RanNum():
    return random.randint(0,5) + 1

# List of player scores
Score = []

# List of player names
Names = []

# Table of number of same value dice to points
Points = {
    0: 0,
    1: 0,
    2: 10,
    3: 20,
    4: 40,
    5: 80,
    6: 150
    }

# How many points will be taken away when you get no dice the same value
Penalty = 100

# How many goes each player is going to take
NumberOfGoes = 10

# How many die are rolled in a go
NumberOfDice = 5

# Prints the instructions on how to play
print ("""
'Nul Points' is a  multiplayer dice game where you get points by finding pairs of """ + str(NumberOfDice) + """numbers.
However, if you get no points on a go, """ + str(Penalty) + """
will be taken off your score. The game ends after """ + str(NumberOfGoes) + " rolls.")

# Shows how many points each kind of pair is worth
for Value in Points:
    if Points[Value] != 0:
        print(str(Value) + " of a kind scores " + str(Points[Value]))

# Ask how many players are going to play the game. Put the number of players in the 'Players' variable
print()
Players = int(input("How many players are there? "))

# Get the player's names and zero their scores
for Value in range(0,Players):
    Names.append(input("What is your name player " + str(Value + 1) + "? "))
    Score.append(0)

# Loops for the number of goes
for Go in range(NumberOfGoes):
    # Loops for each player
    for Player in range(Players):
        # Get the player to press return to roll the dice
        print()
        input(Names[Player] + ", it's your turn. Press Return to roll!")

        # Random numbers are generated for how many dice there are and print out the numbers
        Dice = []
        for Die in range(0, NumberOfDice):
            Dice.append(RanNum())
            print(str(Dice[Die]) + " ", end="")
        print()

        # Fill the Count array with zeroes
        Count = []
        for Value in range(0, 6):
            Count.append(0)

        # Counts up the number of dice with each value and puts the number in the Count array  
        for Die in range(0, NumberOfDice):
            Value = Dice[Die] - 1
            Count[Value] = Count[Value] + 1

        # Adds up the points scored on this go
        AddedPoints = 0
        for Value in range(0, 6):
            DicePoints = Points[Count[Value]]
            if DicePoints > 0:
                # Displays the number of points earned for the dice value
                print("You scored " + str(DicePoints) + " points for " + str(Count[Value]) + " " + str(Value+1) + "s")
                AddedPoints = AddedPoints + DicePoints

        # Check if the player earned any points this go
        if AddedPoints == 0:
            # No points earned - impose the penalty
            print("NUL POINTS! You lose " + str(Penalty) + " points for no score!")
            Score[Player] = Score[Player] - Penalty
        else:
            # Add the points to the player's score
            Score[Player] = Score[Player] + AddedPoints

        # Shows the player's overall score
        print("Your score is now " + str(Score[Player]))

# Works out the highest score of all players
HighestScore = max(Score)

# Create an array to hold the winning players
Winners = []

# Shows the final scores
print()
print("Final scores are:")

# Loop for each player
for Player in range(Players):
    # Prints the player's score
    print(Names[Player] + " has " + str(Score[Player]) + ".")
    # If this player has the highest score, add to the winners array
    if Score[Player] == HighestScore:
        Winners.append(Player)

# Do we have only one winner?
if len(Winners) == 1:
    # Yes - display the winning player
    print(Names[Winners[0]] + " has won!")
else:
    # No - more than one winner (a tie)
    print("The game is tied with the following players: ", end="")
    # Shows the players that won if they drew
    for Winner in Winners:
          print(Names[Winner] + " ", end="")
    print()
