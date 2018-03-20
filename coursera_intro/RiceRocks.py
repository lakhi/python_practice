# Akshay's RiceRocks Implementation
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
PI = math.pi
ROCK_CENTER = [45, 45]
CANNON_DIST = 45
MISSILE_LIFETIME = 50
started = False

score = 0
lives = 3
time = 0.5

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
missile_info = ImageInfo([5,5], [10, 10], 3, MISSILE_LIFETIME)
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

def process_sprite_group(sprite_group, canvas):
    if sprite_group:
        for sprite in list(sprite_group):
            sprite.draw(canvas)
            remove_missile = sprite.update()
            if remove_missile:
                sprite_group.remove(sprite)
        
def group_collide(group, other_object):
    for sprite in list(group):
        if sprite.collide(other_object):
            group.remove(sprite)
            return True
        
    return False    

def group_group_collide(group1, group2):
    group1_collide_count = 0
    
    for sprite in group1:
        collision = group_collide(group2, sprite)
        if collision:
            group1_collide_count += 1
            group1.remove(sprite)
    
    return group1_collide_count

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
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
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
        global missile_group
        angle_components = angle_to_vector(self.angle)
        missile_pos = [0, 0]
        missile_vel = [0, 0]
        
        ''' launch a missile from the cannon: move from the center of the 
        ship to the cannon by taking the horizontal and vertical
        components of the distance to the cannon (which will always be 45)
        '''
        fwd_vect = angle_to_vector(self.angle)
        for i in range(2):
            missile_pos[i] = self.pos[i] + CANNON_DIST * angle_components[i]
            missile_vel[i] = 7 * fwd_vect[i]
        
        a_missile = Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
            
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
   
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius            
            
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
            
        self.age += 1
        if self.age < self.lifespan:
            return False
        else:
            return True
            
    def collide(self, other_object):
        distance = dist(self.get_position(), other_object.get_position())
        
        if distance <= self.get_radius() + other_object.get_radius():
            return True
        else:
            return False

def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True        
        lives = 3
        score = 0
        
def draw(canvas):
    global time, lives, score, started, rock_group
    
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

    # update ship and sprites
    my_ship.update()
        
    # reset the game    
    if lives == 0:
        for rock in list(rock_group):
            rock_group.remove(rock)
        
        for missile in list(missile_group):
            missile_group.remove(missile)
            
        started = False
    
    # group it up if game is on!
    if started:
        process_sprite_group(rock_group, canvas)
        process_sprite_group(missile_group, canvas)
    else:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    
    if group_collide(rock_group, my_ship):
        lives -= 1

    score += 10 * group_group_collide(missile_group, rock_group)            
    
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
    global rock_group
    number_of_rocks = len(rock_group)
    
    if number_of_rocks < 12:
        rock_pos = [random.randrange(ROCK_CENTER[0], WIDTH - ROCK_CENTER[0]), random.randrange(ROCK_CENTER[1], HEIGHT - ROCK_CENTER[1])]
        rock_vel = [random.random() * random.choice([-1, 1]), random.random() * random.choice([-1, 1])]
        rock_ang_vel =  PI * random.random() * random.choice([-1, 1]) / 40
        
        # keep safe distance from ship
        dist_ship_rock = dist(my_ship.get_position(), rock_pos)
        if dist_ship_rock > my_ship.get_radius() + 50:
            a_rock = Sprite(rock_pos, rock_vel, 0, rock_ang_vel, asteroid_image, asteroid_info)
            rock_group.add(a_rock)
        
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
