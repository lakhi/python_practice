# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global cards, exposed, state, turns

    l1 = range(8)
    l2 = range(8)
    exposed = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
    state = 0
    turns = 0    
    cards = l1 + l2
    random.shuffle(cards)
     
# define event handlers
def mouseclick(pos):
    global cards, exposed, state, idx1, idx2, turns
 
    num_pos = range(0, 16*50, 50)
   
    if state == 0:
        state = 1
    elif state == 1:       
        state = 2        
    else:
        if cards[idx1] == cards[idx2]:
            exposed[idx1] = exposed[idx2] = True
        else:
            exposed[idx1] = exposed[idx2] = False
        state = 1
    
    for num in num_pos:
        if pos[0] >= num and pos[0] <= num + 49:
            
            if exposed[num_pos.index(num)] == False:
                exposed[num_pos.index(num)] = True
                if state != 1:
                    idx2 = num_pos.index(num)
                else:
                    idx1 = num_pos.index(num)
    turns += 1

def draw(c):
    number_pos = [10, 75]
    xcard = 0
    i = 0
    
    for card in cards:
        closed_card_box = [[xcard, 0], [50 + xcard, 0], [50 + xcard, 100], [xcard, 100]]   
        
        if exposed[i]:
            c.draw_text(str(card), [number_pos[0], number_pos[1]], 60, 'White')
        else:       
            c.draw_polygon(closed_card_box, 1.5, 'White', 'Green')
            
        number_pos[0] += 50
        xcard += 50
        i += 1

    if turns % 2 == 0:
        label.set_text("Turns = " + str(turns / 2))
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()