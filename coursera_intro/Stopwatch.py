# Stopwatch: The Game
import simplegui

# define global variables
decisecond = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    A = 0
    B = 0
    C = 0
    D = decisecond
    if (D > 9):
        C = D / 10
        D %= 10
    if (C > 9):
        B = C / 10
        C %= 10
    if (B > 5):
        A += 1
        B %= 5
        
    time = str(A) + ':' + str(B) + str(C) + '.' + str(D)
    return time
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()
    
def stop():
    timer.stop()
    
# define event handler for timer with 0.1 sec interval
def stopwatch():
    global decisecond
    decisecond += 1
    
# define draw handler
def draw_watch(canvas):
    canvas.draw_text(format(decisecond), [150,150], 20, 'white')    
    
# create frame
timer = simplegui.create_timer(10, stopwatch)
frame = simplegui.create_frame('Stopwatch', 300, 300)

# register event handlers
frame.add_button('Start', start, 80)
frame.add_button('Stop', stop, 80)
frame.set_draw_handler(draw_watch)

# start frame
frame.start()

