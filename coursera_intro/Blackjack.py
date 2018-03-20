# Mini-project #6 - Blackjack

import simplegui
import random

CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []	# create Hand object

    def __str__(self):
        # return a string representation of a hand
        hand_str = "Hand contains:: "
        for card in self.hand:	
            hand_str += str(card) + " "
        
        return hand_str
        
    def add_card(self, card):
        self.hand.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        for card in self.hand:
            value += VALUES[card.get_rank()]
            
        for card in self.hand:
            if card.get_rank() == 'A':
                if value + 10 <= 21:
                    value += 10
                    break		# can add only one ace
                    
        return value                    
        
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards        
        hand_pos = list(pos)
        for card in self.hand:
            card.draw(canvas, hand_pos)
            hand_pos[0] += CARD_SIZE[0] 		# Horizontal sequence
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = list()
        
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))
        
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)
        
    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()
    
    def __str__(self):
        # return a string representing the deck
        return "Deck contains:: " + str([str(card) for card in self.deck])


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score

    if in_play:
        outcome = "You lost the round. Start a new one. Hit or stand?"
        score -= 1
    else:
        outcome = "Hit or Stand?"
    
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    in_play = True

def hit():
    # if the hand is in play, hit the player
    global outcome, in_play, deck, player_hand, dealer_hand, score
    
    playerHit = False
    if in_play:
        player_hand.add_card(deck.deal_card())
        playerHit = True
    else:
        outcome = "Game is over! Press Deal to get things rolling!"
    
    # if busted, assign a message to outcome, update in_play and score
    if playerHit:
        if player_hand.get_value() > 21:
            in_play = False
            score -= 1
            outcome = "You have busted. New Deal?"
        else:    
            outcome = "Good hit. Now hit or stand?"
    
def stand():
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    global outcome, in_play, deck, player_hand, dealer_hand, score
    
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())		# Hit the dealer
            
            if dealer_hand.get_value() > 21:	 		# Dealer busts
                score += 1
                outcome = "Dealer has busted. You win! Wanna deal again?"
                in_play = False
        
        # at this point value of dealer's hand is at least 17, so now dealer will never hit. Hence we compare the hands        
        if in_play:
            if player_hand.get_value() > dealer_hand.get_value():
                in_play = False
                score += 1
                outcome = "You win the hand! Lets deal again?"
            else:
                in_play = False
                outcome = "Its a tie. New Deal?"
    
    else:
        outcome = "Game is over! Press Deal to get things rolling!"
    

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    player_hand.draw(canvas, (50,100))
    dealer_hand.draw(canvas, [50, 300])
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [50 + CARD_CENTER[0], 152 + CARD_CENTER[1] * 4], CARD_BACK_SIZE)
    
    canvas.draw_text("Score: " + str(score), (50, 20), 20, 'White', 'serif')
    canvas.draw_line((150, 0), (150, 30), 2, 'Black')
    canvas.draw_text(outcome, (200, 20), 20, 'White', 'serif')
    canvas.draw_line((0, 30), (600, 30), 2, 'Black')
    
    canvas.draw_text("Your hand", (50, 80), 20, 'White', 'serif')
    canvas.draw_text("Dealer's hand", (50, 280), 20, 'White', 'serif')
    
    canvas.draw_line((0, 550), (600, 550), 2, 'Black')
    canvas.draw_text("BlackJack", (0, 600), 60, 'Black', 'monospace')
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
