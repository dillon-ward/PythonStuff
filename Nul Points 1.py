import random

def RanNum():
    return random.randint(0,5) + 1

Score=[]

Points = {
    0: 0,
    1: 0,
    2: 10,
    3: 20,
    4: 40,
    5: 80,
    6: 150
    }
Penalty = 100
NumberOfGoes = 10
NumberOfDice = 5

print ("""
'Nul Points' is a  multiplayer dice game where you get points by finding pairs of 6 numbers.
However, for how many you get 0, that will be taken off your score at the end (where 0 equals -1 point).
A pair of 2 equals 20 points, pair of 3 equals 30 etc. The game ends after """ + str(NumberOfGoes) + " rolls.")

for Value in Points:
    if Points[Value] != 0:
        print(str(Value) + " of a kind scores " + str(Points[Value]))

print()
Players = int(input("How many players are there? "))

for Value in range(0,Players):
    Score.append(0)

for Go in range(NumberOfGoes):
    for Player in range(Players):
        print()
        input("Player " + str(Player + 1) + ", it's your turn. Press Return to roll!")

        Dice = []
        for Die in range(0, NumberOfDice):
            Dice.append(RanNum())
            print(str(Dice[Die]) + " ", end="")
        print()

        Count = []
        for Value in range(0, 6):
            Count.append(0)
            
        for Die in range(0, NumberOfDice):
            Value = Dice[Die] - 1
            Count[Value] = Count[Value] + 1

        AddedPoints = 0
        for Value in range(0, 6):
            DicePoints = Points[Count[Value]]
            if DicePoints > 0:
                print("You scored " + str(DicePoints) + " points for " + str(Count[Value]) + " " + str(Value+1) + "s")
                AddedPoints = AddedPoints + DicePoints

        if AddedPoints == 0:
            print("NUL POINTS! You lose " + str(Penalty) + " points for no score!")
            Score[Player] = Score[Player] - Penalty
        else:
            Score[Player] = Score[Player] + AddedPoints

        print("Your score is now " + str(Score[Player]))

HighestScore = max(Score)
Winners = []
print()
print("Final scores are:")
for Player in range(Players):
    print("Player " + str(Player +1) + " has " + str(Score[Player]) + ".")
    if Score[Player] == HighestScore:
        Winners.append(Player)

if len(Winners) == 1:
    print("Player " + str(Winners[0] + 1) + " has won!")
else:
    print("The game is tied with the following players: ", end="")
    for Winner in Winners:
          print(str(Winner + 1) + " ", end="")
    print()

