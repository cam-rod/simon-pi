# Cameron Rodriguez
# June 17, 2019
# This game allows a user to play Simon on a Raspberry Pi.

"""
Data Dictionary

all_leds
all_buttons
sequence
led_delay

temp
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
    g.setup([13, 15, 38, 40], g.IN, pull_up_down=g.PUD_DOWN)

    # Introduce game
    print 'Welcome to Simon, Raspberry Pi edition! The rules are very simple. A series of LEDs will'
    print 'flash in a certain order; your job is to press the buttons below the LEDs in the same'
    print 'order. If you succeed, the LEDs will flash again in the same order. If you miss, the'
    print 'correct LED will flash for a few seconds.\n'
    
    temp = raw_input('When you are ready to start the game, press Enter/Return.')
# End initialize

# This function runs the game.
def gameplay():
    pass

if __name__ == '__main__':
    # Create global variables for arrays of pins
    all_leds = [33, 35, 36, 37]
    all_buttons = [13, 15, 38, 40]

    # Create global variables for game
    sequence = []
    led_delay = 1.00

    # Start the game
    initialize()
    gameplay()