# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

paddle1_pos = HEIGHT/2 - HALF_PAD_HEIGHT
paddle2_pos = HEIGHT/2 - HALF_PAD_HEIGHT

paddle1_vel = paddle2_vel = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH/2, HEIGHT/2]    
    ball_vel = [random.randrange(2, 5), random.randrange(1, 4)]
    
    if direction == LEFT:
        ball_vel[0] = -ball_vel[0]    

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    score1 = score2 = 0
    spawn_ball(RIGHT)   
    
def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] -= ball_vel[1]
    
    # ball touches the gutter (nested if: ball touches the paddle)
    if (ball_pos[0] >= (WIDTH - 1) - PAD_WIDTH - BALL_RADIUS):
        if ball_pos[1] >= paddle2_pos and ball_pos[1] <= paddle2_pos + PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0] * 1.1 # bounce back off the paddle with increased speed
            ball_vel[1] *= 1.1
        else:    
            score1 += 1
            spawn_ball(LEFT)
        
    elif (ball_pos[0] <= PAD_WIDTH + BALL_RADIUS):
        if ball_pos[1] >= paddle1_pos and ball_pos[1] <= paddle1_pos + PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0] * 1.1
            ball_vel[1] *= 1.1
        else:
            score2 += 1
            spawn_ball(RIGHT)
    
    # bounce back off the upper wall    
    if (ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]        
    elif (ball_pos[1] <= BALL_RADIUS):
        ball_vel[1] = -ball_vel[1] 
    
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 1,	"White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + PAD_HEIGHT + paddle1_vel <= HEIGHT - 1 and paddle1_pos + paddle1_vel >= 0:
        paddle1_pos += paddle1_vel
    if paddle2_pos + PAD_HEIGHT + paddle2_vel <= HEIGHT - 1 and paddle2_pos + paddle2_vel >= 0:
        paddle2_pos += paddle2_vel
    
    # draw paddles
    c.draw_polygon([[0, paddle1_pos], [PAD_WIDTH, paddle1_pos], [PAD_WIDTH, paddle1_pos + PAD_HEIGHT], [0, paddle1_pos + PAD_HEIGHT]], 1, "White", "White")
    
    c.draw_polygon([[(WIDTH - 1) - PAD_WIDTH, paddle2_pos], [WIDTH - 1, paddle2_pos], [WIDTH - 1, paddle2_pos + PAD_HEIGHT], [(WIDTH - 1) - PAD_WIDTH, paddle2_pos + PAD_HEIGHT]], 1, "White", "White")
    
    # draw scores
    c.draw_text(str(score1), [(WIDTH / 2) - 80, 40], 40, "White")
    c.draw_text(str(score2), [(WIDTH / 2) + 60, 40], 40, "White")

    
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = -3
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 3
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -3
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 3        
   
def keyup(key):
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0.0
    elif key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0.0
    
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Reset', new_game, 200)

# start frame
new_game()
frame.start()
