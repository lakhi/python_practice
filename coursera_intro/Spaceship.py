# Akshay's Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
PI = math.pi
ROCK_CENTER = [45, 45]
CANNON_DIST = 45

score = 0
lives = 3
time = 0.5

# controls = {"left" : 'turn(counter_clockwise)', "right" : 'turn(clockwise)'}

# turn_direction = {"left" : counter_clockwise, "right" : clockwise}

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.forward_vector = angle_to_vector(self.angle)
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        # ship's position keeps changing due to the current velocity and friction
        for i in range(2):
            self.vel[i] *= 0.99
            self.pos[i] += self.vel[i]
        
        self.angle += self.angle_vel
        
        # ship accelerates if the thrusters are on. acceleration depends on the forward vector
        if self.thrust:
            self.forward_vector = angle_to_vector(self.angle)
            for i in range(2):
                self.vel[i] += 0.1 * self.forward_vector[i]
            
        if self.pos[0] < 0 or self.pos[0] >= WIDTH:
            self.pos[0] %= WIDTH
        if self.pos[1] < 0 or self.pos[1] >= HEIGHT:
            self.pos[1] %= HEIGHT    
    
    def turn(self, direction):
        turn_angle = 0.1 * PI/4
        
        if direction == 'counter_clockwise':
            turn_angle = - turn_angle
            
        self.angle_vel += turn_angle    
        
    def thrust_ship(self, thrust_switch):
        self.thrust = thrust_switch
        
        if self.thrust:
            self.image_center[0] += self.image_size[0]
            ship_thrust_sound.play()
        else:
            self.image_center[0] -= self.image_size[0]
            ship_thrust_sound.rewind()
            
    def shoot(self):
        global a_missile
        angle_components = angle_to_vector(self.angle)
        missile_pos = [0, 0]
        missile_vel = [0, 0]
        
        ''' launch a missile from the cannon: move from the center of the 
        ship to the cannon by taking the horizontal and vertical
        components of the distance to the cannon (which will always be 45)
        '''
        for i in range(2):
            missile_pos[i] = self.pos[i] + CANNON_DIST * angle_components[i]
            missile_vel[i] = self.vel[i] + 0.1 * self.forward_vector[i]
        
        a_missile = Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound)
            
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        for i in range(2):
            self.pos[i] += self.vel[i]

        self.angle += self.angle_vel
        
        if self.pos[0] < 0 or self.pos[0] >= WIDTH:
            self.pos[0] %= WIDTH
        if self.pos[1] < 0 or self.pos[1] >= HEIGHT:
            self.pos[1] %= HEIGHT

           
def draw(canvas):
    global time, a_rock
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    canvas.draw_text("Lives: " + str(lives), [20, 30], 20, 'white', 'monospace')
    canvas.draw_text("Score: " + str(score), [WIDTH - 120, 30], 20, 'white', 'monospace')
    
    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()

def keydown(key):
    if simplegui.KEY_MAP["left"] == key:
        my_ship.turn('counter_clockwise')
    elif simplegui.KEY_MAP["right"] == key:
        my_ship.turn('clockwise')
    elif simplegui.KEY_MAP["up"] == key:
        my_ship.thrust_ship(True)
    elif simplegui.KEY_MAP["space"] == key:
        my_ship.shoot()
        
def keyup(key):
    if simplegui.KEY_MAP["left"] == key:
        my_ship.turn('clockwise')
    elif simplegui.KEY_MAP["right"] == key:
        my_ship.turn('counter_clockwise')
    elif simplegui.KEY_MAP["up"] == key:
        my_ship.thrust_ship(False)
        
        
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    
    rock_pos = [random.randrange(ROCK_CENTER[0], WIDTH - ROCK_CENTER[0]), random.randrange(ROCK_CENTER[1], HEIGHT - ROCK_CENTER[1])]
    rock_vel = [random.random() * random.choice([-1, 1]), random.random() * random.choice([-1, 1])]
    rock_ang_vel =  PI * random.random() * random.choice([-1, 1]) / 100
    
    a_rock = Sprite(rock_pos, rock_vel, 0, rock_ang_vel, asteroid_image, asteroid_info)
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
