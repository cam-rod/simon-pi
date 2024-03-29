# Cameron Rodriguez
# June 17, 2019
# This game allows a user to play Simon on a Raspberry Pi.

"""
Data Dictionary

all_leds: list: contains the numbers of all the GPIO pins that power the LEDs
all_buttons: list: contains the numbers of all the GPIO pins that take input from the butttons
sequence: list: a randomly generated list of LED pins for the user to match with the buttons
led_delay: float: the amount of time between LED flashes during the "teaching" stage
level: int: the user's current level, which is the number of LEDs shown
matching_led: dict: matches each button input pin to the LED power pin for verification

temp: str: used to hold raw_input at start of game
lost: bool: indicates if the player has lost the game
checked: bool: indicates if the current sequence LED has been checked for an input match
"""

import time # For flashing LEDs
import RPi.GPIO as g # Controls Raspberry Pi GPIO pins
from random import randint # Generates sequence of lights

# This function initializes the GPIO pins and introduces the player to the game.
def initialize():
    # Setup system
    g.setmode(g.BOARD)
    g.setwarnings(False)

    # Setup input (with pulldown resistor) and output pins
    g.setup([11, 33, 35, 36, 37], g.OUT)
    g.setup(all_buttons, g.IN, pull_up_down=g.PUD_DOWN)
    g.output(11, g.HIGH) # Power for button supply

    # Introduce game
    print 'Welcome to Simon, Raspberry Pi edition! The rules are very simple. A series of LEDs will'
    print 'flash in a certain order; your job is to press the buttons below the LEDs in the same'
    print 'order. You can play after the LEDs flash thrice, by pressing each button for less than a second.'
    print 'You can press the next button after an LED flashes. If you succeed, the LEDs will flash again'
    print 'in the same order with an addition. If you miss, the correct LED will flash for a few seconds'
    print 'before the game ends.\n'
    
    temp = raw_input('When you are ready to start the game, press Enter/Return.')
# End initialize

# This function runs the game.
def gameplay():
    # Modify global vars
    global sequence, led_delay, level
    lost = False
    checked = False

    # Display a countdown ending
    for i in range(5,-1,-1):
        print i
        time.sleep(1)
    # End for i
    print ''

    # Main gameplay loop
    while lost is False:
        level += 1
        print 'Level {}'.format(level)

        # Generate and display the sequence
        sequence.append(single_led(randint(34,37)))
        for i in sequence:
            g.output(i, g.HIGH)
            time.sleep(led_delay)
            g.output(i, g.LOW)
            time.sleep(led_delay)
        # End for i

        # Flash all LEDs thrice to indicate user turn
        for i in range(3):
            g.output(all_leds, g.HIGH)
            time.sleep(0.1)
            g.output(all_leds, g.LOW)
            time.sleep(0.1)
        # End for i

        # Scan for correct user input
        for i in range(len(sequence)):
            checked = False
            while checked is False:
                for j in all_buttons:
                    if g.input(j): # Button j was pressed
                        if matching_led[j] == sequence[i]:
                            checked = True # Break button scan loop
                            g.output(matching_led[j], g.HIGH) # Flash LED
                            time.sleep(0.7)
                            g.output(matching_led[j], g.LOW)
                        else:
                            for k in range(5): # Flash the correct answer 5 times
                                g.output(sequence[i], g.HIGH)
                                time.sleep(0.5)
                                g.output(sequence[i], g.LOW)
                                time.sleep(0.5)
                            # End for i
                            lost = True
                            checked = True
                        # End if right_button(i,j)
                    # End if g.input(j)
                # End for j
            # End while checked
            if lost:
                break
            # End if lost
        # End for i

        if lost:
            pass
        else: 
            for i in range(3): # Flash all LEDs to indicate successful entry
                g.output(all_leds, g.HIGH)
                time.sleep(0.1)
                g.output(all_leds, g.LOW)
                time.sleep(0.1)
            # End for i
            if len(sequence) < 19:
                led_delay -= 0.05 # Decrease the flash interval
            # End if len(sequence)
            time.sleep(1) # Break before next level
        # End if lost
    # End while lost
# End gameplay

# This function declares a loss and closes the program
def endgame():
    # Display congratulatory message
    print '\nCongratulations, you made it to level {}!'.format(level)
    print 'Thanks for playing Simon. Goodbye!'
    
    # Disable GPIO pins and cleanup
    g.output(all_leds, g.LOW)
    g.output(11, g.LOW) # Power off buttons
    g.cleanup()

    # Leave message visible for 5 seconds
    time.sleep(5)
# End endgame

if __name__ == '__main__':
    # Create global variables for arrays of pins
    all_leds = [33, 35, 36, 37]
    all_buttons = [13, 15, 38, 40]

    # Create global variables for game
    sequence = []
    led_delay = 1.00
    level = 0
    matching_led = {13: 33, 15: 35, 38: 36, 40: 37}
    single_led = lambda x: x if x <> 34 else 33 # Used to correct randint call to first pin

    # Run the game
    initialize()
    gameplay()
    endgame()
# End if __name__