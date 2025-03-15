# choice = input("Which direction do you choose [North, West, South, East]? ")

# print("They chose: ", choice)

import os
import random
import time


# constants



CONSTANTS = {
  "exit": -1,
  "invalid": 10,
  "confirm": 1,
  "deny": 0,
  "xBounds": 20,
  "yBounds": 20,
  "help": 911,
  "map": 101,
  "coord": 202,
  "north": "n",
  "west": "w",
  "south": "s",
  "east": "e",
}

# variables
northCoord = 0
westCoord = 0
southCoord = 0
eastCoord = 10

xCoord = 10
yCoord = 4

destinationXCoord = 8
destinationYCoord = 5

totalMoves = 0

def won():
  return xCoord == destinationXCoord and yCoord == destinationYCoord



# starting: (10,2)
# Goal:     (-15,-5)
def getCoordinates():
  return f"({xCoord}, {yCoord})"

def printMap():
  print('''
              |             
              |             
              |             
              |             
              |             
  --------------------o-----
              |             
        x     |             
              |             
              |             
              |             
  ''', getCoordinates())

# methods
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# def generateEvent():

def test():
  print("in test")

def generateNorthernMove():
  global yCoord
  yCoord += 1
  if (yCoord == abs(CONSTANTS["yBounds"])):
    yCoord = -19
  print("You head North")
def generateWesternMove():
  global xCoord
  xCoord -= 1
  if (xCoord == abs(CONSTANTS["xBounds"])):
    xCoord = 19
  print("You head West")
def generateSouthernMove():
  global yCoord
  yCoord -= 1
  if (yCoord == abs(CONSTANTS["yBounds"])):
    yCoord = 19
  print("You head South")
def generateEasternMove():
  global xCoord
  xCoord += 1
  if (xCoord == abs(CONSTANTS["xBounds"])):
    xCoord = -19
  print("You head East")

def validChoice(choice):
  if choice == CONSTANTS["exit"]:
    # end program
    print("thanks for playing")
    return False
  elif choice == CONSTANTS["invalid"]:
    # loop back to og question
    print("try again")
  elif choice == CONSTANTS["confirm"]:
    print("proceed")


def readResponse(resp):
  if (resp.lower() == "exit" or resp.lower() == "end" or resp.lower() == "stop"):
    return CONSTANTS["exit"] # end
  if (resp.lower() == "help" or resp.lower() == "/help" or resp.lower() == "h" or resp.lower() == "/h"):
    return CONSTANTS["help"]
  if (resp.lower() == "yes" or resp.lower() == "y"):
    return CONSTANTS["confirm"]
  if (resp.lower() == "no"):
    return CONSTANTS["deny"]
  if (resp.lower() == "map"):
    return CONSTANTS["map"]
  if (resp.lower() == "north" or resp.lower() == "n"):
    return CONSTANTS["north"]
  if (resp.lower() == "west" or resp.lower() == "w"):
    return CONSTANTS["west"]
  if (resp.lower() == "south" or resp.lower() == "s"):
    return CONSTANTS["south"]
  if (resp.lower() == "east" or resp.lower() == "e"):
    return CONSTANTS["east"]



def move_direction(direction):
  if direction.lower() == "n" or direction.lower() == "north":
    generateNorthernMove()
    return 1
  elif direction.lower() == "w" or direction.lower() == "west":
    generateWesternMove()
    return 1
  elif direction.lower() == "s" or direction.lower() == "south":
    generateSouthernMove()
    return 1
  elif direction.lower() == "e" or direction.lower() == "east":
    if totalMoves == 0:
      # Find friends
      print("You see your friends! They decide to tag along the journey with you.")
      return 1
    else:
      generateEasternMove()
      return 1
  elif direction.lower() == "exit":
    return -1
  else:
    print("Invalid direction")
    return 0
  



def d10():
  return random.randint(1, 10) # random num [1-10] (inclusive)
def d20(): 
  return random.randint(1,20) # random num [1-20] (inclusive)


def generateRandomPrompt():
  # Roll a d20
  if (d20() > 20):
    return "Woah! You just got sucked up in a tornado and landed somewhere completely random!"

def checkCompass():
  print(f"Your location is showing:\n  North:{northCoord}, West:{westCoord}, South:{southCoord}, East:{eastCoord}, \n({westCoord-eastCoord},{northCoord-southCoord})")

# Look into how I can print this accurately.
def checkMap():
  mapCoords = '''
            |          N  
            |        W + E
            |          S  
            |             
            |             
--------------------o-----
            |             
      x     |             
            |             
            |             
            |             
'''
  print(mapCoords)





clear_console()

# Start:
# clear console
intro = "G: Wake up, Trip..\n" \
"   Are you there?\n" \
"   Brother.. I have an urgent task for you...\n" \
"   I need you to retrieve something of great importance..\n\n" \
"" \
"You: What do you need, Master?\n\n" \
"" \
"G: I need my voice..\n\n\n\n" \
"" \
"***********\n\n\n\n" \
"From this moment on, Trip stood up out of a deep meditation and embarked on his great journey.. To the west.. hopefully.\n\n\n\n"


def main():
  print(intro)
  global totalMoves

  # time.sleep(5)
  startGame = input("[Start] [Exit] ")

  if (startGame.lower() == "s" or startGame.lower() == "start"):
    clear_console()

    # choice = input("Which direction do you choose [(N)orth, (W)est, (S)outh or (E)ast]? ")
    # if validChoice(choice):
    #   print("\nTrip Looked to the sun, grinned and decided to head ", choice)
    
    choice = 0
    prompt = ""

    prompt = generatePrompt()
    while (choice != CONSTANTS["exit"]):
      resp = input(prompt)
      choice = readResponse(resp)
      if (choice == CONSTANTS["invalid"]):
        print("Invalid response, try again")
        continue
      elif (choice == CONSTANTS["exit"]):
        # printHelp()
        continue
      elif (choice == CONSTANTS["help"]):
        printHelp()
        continue
      elif (choice == CONSTANTS["map"]):
        printMap()
        continue
      else:
        move_direction(choice)
        totalMoves += 1
      if (won()):
        print("Congrats!! You arrived at your destination!!")
        break

    print("Thanks for playing! You ended up at: ", getCoordinates())


def generatePrompt():
  return "Which direction do you choose [(N)orth, (W)est, (S)outh or (E)ast]? "
def printHelp():
  print("At anytime you can type:\nhelp - exit - map.")

  # while choice != CONSTANTS["exit"]:
    # response = input(generateRandomPrompt())

main()

'''
How it works:

while response isnt -1

  Prompt user,
    validate prompt response
      end if player exits
      re-prompt if response is invalid 
    result of response given.
      generate chance for a random event
  re-loop.

Game Over when west - east >= 10 or east > 50

'''