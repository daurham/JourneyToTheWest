#
# This program is a simple game.
#

import random
import curses
import time

# Define the grid boundaries
GRID_MIN = -10
GRID_MAX = 10

# Initialize the player and temple's starting position
player_icon = 'o'
destination_icon = 'T'

player_x = GRID_MAX - 1
player_y = GRID_MAX - 1

destination_x = 0
destination_y = 0

decoy_destination1_x = 0
decoy_destination1_y = 0

decoy_destination2_x = 0
decoy_destination2_y = 0

# Initialize game stats
hp = 10
gold = 0
total_moves = 0
game_started = False
random_event_percentage = 0.2

# Generate a random coordinate on the map
def random_coord():
  return random.randint(GRID_MIN, GRID_MAX) # random num [min-max] (inclusive)

# Generate a random coordinate on the left of the map
def random_west_coord():
  return random.randint(GRID_MIN, 0) # random num [min-max] (inclusive)

# Generate coordinates for all the destinations
def generate_destination_positions():
  global  destination_x, destination_y, decoy_destination1_x, decoy_destination1_y, decoy_destination2_x, decoy_destination2_y
  destination_x = random_west_coord()
  destination_y = random_coord()
  decoy_destination1_x = random_west_coord()
  decoy_destination1_y = random_coord()
  decoy_destination2_x = random_west_coord()
  decoy_destination2_y = random_coord()
generate_destination_positions()

# Define possible directions
DIRECTIONS = {
    curses.KEY_UP: (0, 1),      # Up (North)
    curses.KEY_DOWN: (0, -1),   # Down (South)
    curses.KEY_LEFT: (-1, 0),   # Left (West)
    curses.KEY_RIGHT: (1, 0),   # Right (East)
    ord('w'): (0, 1),           # Alternative keys
    ord('s'): (0, -1),
    ord('a'): (-1, 0),
    ord('d'): (1, 0),
}

# Function to print the in-game player stats
def print_player_stats(stdscr, player_x, player_y):
    stdscr.addstr(f"[Coord: ({player_x}, {player_y}) - HP: {hp}/10 - Gold: {gold}]\n")

# Function to print the in-game UI
def print_UI(stdscr, player_x, player_y, msg = None):
    stdscr.clear()
    print_player_stats(stdscr, player_x, player_y)
    for y in range(GRID_MAX, GRID_MIN - 1, -1):  # Top to bottom
        for x in range(GRID_MIN, GRID_MAX + 1):  # Left to right
            if x == player_x and y == player_y:
                stdscr.addstr(f"{player_icon} ")  # Player's position
            elif x == destination_x and y == destination_y:
                stdscr.addstr(f"{destination_icon} ")  # True destination's position
            elif x == decoy_destination1_x and y == decoy_destination1_y:
                stdscr.addstr(f"{destination_icon} ")  # Decoy destination's position
            elif x == decoy_destination2_x and y == decoy_destination2_y:
                stdscr.addstr(f"{destination_icon} ")  # Decoy destination's position
            else:
                stdscr.addstr(f". ")  # Empty space
        stdscr.addstr("\n")  # New line after each row
    if msg:
      stdscr.addstr(f"{msg}")
    stdscr.refresh()  # Refresh the screen to show changes

# Function to handle random events
def random_event(stdscr):
    global gold, hp, player_x, player_y
    sec = 2

    events = [
        "treasure",
        "bear",
        "rain",
        "ankle",
        "twister",
        "what?",
        "merchant",
    ]
    event = random.choice(events)
    if total_moves == 0:
        return
      
    if (event == "what?"):
      if (total_moves % 2 != 0):
        event = random.choice(events)
    
    if event == "treasure":
        gold += 1
        event = "\nA come across treasure!  +1 gold added"
    if event == "bear":
        hp -= 4
        event = "\nA bear appears and takes a slash at you!" \
        "\nYou nearly escape with your life!  -4 hp"
    if event == "rain":
        hp -= 1
        event = "\nA cold heavy rain occurs.  -1 hp"
    if event == "ankle":
        hp -= 1
        event = "\nYou twist your ankle walking over a rock!  -1 hp"
    if event == "twister":
        player_x = random_coord()
        player_y = random_coord()
        event = "\nA twister appears and sweeps you across the map!" \
        "\nYou land somewhere randomly!"
    if event == "what?":
        player_x = random_coord()
        player_y = random_coord()
        generate_destination_positions()
        event = "\nA mysterious feeling comes over you.." \
        "\n..You pass out!" \
        "\n" \
        "\nYou wake up looking around and" \
        "\n..feel completely disoriented!" \
        "\n\nOff in the distance, you hear a laugh..?"
        sec = 5
    if event == "merchant":
        event = "\nYou stumble across an old merchant." \
        "\nWould you like to purchase some bread for 2 gold pieces?" \
        "[y] / [n]"
        stdscr.addstr(f"{event}\n")
        stdscr.refresh()
        time.sleep(2)
        # Get the key pressed
        while True:
          key = stdscr.getch()
          if (key == ord('y')):
            if (gold >= 2):
              gold -= 2
              hp += 5
              event = "\n*Gulp*" \
                      "\nYou feel better."
              break
            else:
              event = "\nYou don't have enough gold."
              break
          elif (key == ord('n')):
            event = "\nYou leave"
            break

    stdscr.addstr(f"{event}\n")
    stdscr.refresh()
    time.sleep(sec)

# Determines when player is at destination
def arrived_at_destination():
    return player_x == destination_x and player_y == destination_y

# Determines when player is at decoy destination
def arrived_at_decoy_destination(stdscr):
    stdscr.addstr("running")
    return (player_x == decoy_destination1_x and player_y == decoy_destination1_y) or (player_x == decoy_destination2_x and player_y == decoy_destination2_y)

# Determines when player dies
def player_died():
    return hp <= 0

# Prints title
def print_title(stdscr):
   stdscr.addstr("" \
        "###############################"
      "\n_-_-_ Journey To The West _-_-_\n"
        "###############################"
   )

# Prints winning message
def print_win(stdscr):
   stdscr.addstr("" \
        "###############################"
      "\n_-_-_-_-_-_ You Won _-_-_-_-_-_\n"
        "###############################"
   )

# Prints losing message
def print_loss(stdscr):
   stdscr.addstr("" \
        "###############################"
      "\n_-_-_-_-_-_ D E A D _-_-_-_-_-_\n"
        "###############################"
   )


# Main game loop
def game_loop(stdscr):
    global player_x, player_y, total_moves, game_started

    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(100)  # Refresh every 100ms

    # Initial instructions
    print_title(stdscr)
    stdscr.addstr("\n\n"
      "Controls:\n"
      "  - Arrow keys or w/a/s/d to move.\n"
      "  - 'q' to quit.\n"
      "  - 'y' for yes.\n"
      "  - 'n' for no.\n")
    stdscr.refresh()
    time.sleep(5)

    # Initial story
    stdscr.clear()
    print_title(stdscr)
    stdscr.addstr("\n\n" \
      "G: \"Wake up my son..\n\n" \
      
      f"I need you '{player_icon}' to find the sacred scriptures..\n" \
      f" ..in one of these '{destination_icon}' temples.\n\n" \
      
      
      "But be careful.. There are false temples to choose from..\n" \
      " ..and plenty of threats out there.\n\n\n" \
      
      "Are you ready to embark on your.." \
      "\n                 Journey to the West?\"\n\n" \
    
      "[y] / [n] ") 

    stdscr.refresh()
    while (True):
        if arrived_at_destination() or player_died(): # End the game
            break
        key = stdscr.getch()
        if game_started == False:
           if key == ord('y'):  # Start the game
              stdscr.clear()
              print_UI(stdscr, player_x, player_y)
              game_started = True
           elif key == ord('n') or key == ord('q'):  # Quit the game
              stdscr.addstr("\nThanks for playing!\n")
              stdscr.refresh()
              break
        elif key == ord('q'):  # Quit the game
            stdscr.addstr("\nThanks for playing!\n")
            stdscr.refresh()
            break
        elif key in DIRECTIONS:  # Move the player
            dx, dy = DIRECTIONS[key]
            new_x = player_x + dx
            new_y = player_y + dy

            # Check if the new position is within the map boundaries
            if GRID_MIN <= new_x <= GRID_MAX and GRID_MIN <= new_y <= GRID_MAX:
                player_x, player_y = new_x, new_y
                msg = None
                # Check for a random event (20% chance)
                if random.random() < random_event_percentage:
                    random_event(stdscr)
                if (arrived_at_decoy_destination(stdscr)):
                  msg = "Wrong temple!"


                total_moves += 1
                print_UI(stdscr, player_x, player_y, msg)
            else:
                stdscr.addstr("You can't go that way!\n")
            stdscr.refresh()


    # Outro 
    stdscr.clear()
    if (arrived_at_destination()): # When player beats the game
      print_win(stdscr)
      stdscr.addstr("\n\n\n\ngg")
      stdscr.refresh()
      time.sleep(2)
    if (player_died()): # When player loses the game
      print_loss(stdscr)
      stdscr.addstr("\n\n\n\ngg")
      stdscr.refresh()
      time.sleep(2)

# Start the game
curses.wrapper(game_loop)