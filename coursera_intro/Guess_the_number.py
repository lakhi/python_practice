# "Guess the number" game!

import simplegui
import random

# Default game: range between 0-100
high = 100
low = 0
global secret_number, count

# helper functions to start and restart the game
def new_game():
    global secret_number, count

    secret_number = random.randrange(low, high)
    if (high == 100):
        count = 7
    else:
        count = 10
    
    print "\nNew game! Range between: " + str(low) + "-" + str(high-1) + " (inclusive)"
    print "Number of tries: " + str(count) + "\n"

def tries_over():
    print "\nNumber of tries over. You lose!"
    print "Secret number was:", secret_number
    new_game()
    
# define event handlers for control panel
def range100():
    global high, count
    high = 100
    new_game()
    
def range1000():
    # button that changes range to range [0,1000) and restarts
    global high, count
    high = 1000
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    global count
    
    if (guess):
        guess = int(guess)
    
    if (count > 0):
        count-= 1
        print "Your guess:", guess
        if (guess == secret_number):
            print "Correct! You win! Congratulations!"
            new_game()
        elif (guess < secret_number):
            print "Computer says: Higher \t Tries left:", count
        elif (guess > secret_number):
            print "Computer says: Lower \t Tries left:", count
    
    if (count == 0):
        tries_over()    
                
# create frame
frame = simplegui.create_frame("Guess the number", 250, 250)

# register event handlers for control elements

frame.add_input("Enter guess", input_guess, 100)
frame.add_button("Range: 1-100", range100)
frame.add_button("Range: 1-1000", range1000)

# call new_game and start frame

new_game()
frame.start()