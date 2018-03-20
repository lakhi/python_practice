# Rock-paper-scissors-lizard-Spock game simulation
import math
import random

# helper functions

def number_to_name(number):
    return {
            0:'rock',
            1:'Spock',
            2:'paper',
            3:'lizard',
            4:'scissors'
            }[number]
    
def name_to_number(name):
    if(name == 'rock'):
        number = 0
    elif(name == 'Spock'):
        number = 1
    elif(name == 'paper'):
        number = 2
    elif(name == 'lizard'):
        number = 3
    elif(name == 'scissors'):
        number = 4        
    return number

def rpsls(name): 
    player_guess = name
    player_number = name_to_number(player_guess)

    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0,5)

    # compute difference of player_number and comp_number modulo five
    decider = (player_number - comp_number) % 5

    # use if/elif/else to determine winner
    if(decider == 3 or decider == 4):
        result = "Computer wins!"
    elif(decider == 1 or decider == 2):
        result = "Player wins!"
    else:
        result = "Player and computer tie!"

    # convert comp_number to name using number_to_name
    computer_guess = number_to_name(comp_number)

    # print results
    print "Player chooses " + player_guess
    print "Computer chooses " + computer_guess
    print result + "\n"
     
# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")