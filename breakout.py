# CodeSkulptor runs Python programs in your browser.
# Click the upper left button to run this simple demo.

# CodeSkulptor is tested to run in recent versions of
# Chrome, Firefox, and Safari.

import simplegui

message = "Welcome To Atari Breakout!"

# Handler for mouse click
def click():
    global message
    message = "Game starts now in"
    
    
    
# Handler to draw on canvas
def draw(canvas):
    canvas.draw_text(message, [50,112], 48, "Red")

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", 300, 200)
frame.add_button("Start Game", click)
frame.set_draw_handler(draw)

# The Vector class
class Vector:
    
    # Initialiser
    def __init__(self, p=(0,0)):
        self.x = p[0]
        self.y = p[1]
        
    # Returns a string representation of the vector
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
    
    # Tests the equality of this vector and another
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    # Tests the inequality of this vector and another
    def __ne__(self, other):
        return not self.__eq__(other) 

    # Returns a tuple with the point corresponding to the vector
    def getP(self):
        return (self.x, self.y)
    
    # Returns a copy of the vector
    def copy(self):
        v = Vector()
        v.x = self.x
        v.y = self.y
        return v
    
    # Adds another vector to this vector
    def add(self, other):
        if other.x != 0:
            self.x += other.x
        if other.y != 0:
            self.y += other.y
        return self

    def __add__(self, other):
        return self.copy().add(other);
    
    # Negates the vector (makes it point in the opposite direction)
    def negate(self):
        return self.multiply(-1)

        # Magic method for - (one operand)
    def __neg__(self):
        return self.copy().negate()
        
    # Subtracts another vector from this vector
    def subtract(self, other):
        return self.add(-other)
    
    # Magic method for - (two operands)
    def __sub__(self, other):
        return self.copy().subtract(other)
    
    # Returns the dot product of this vector with another one
    def dot(self, other):
        return self.x*other.x + self.y*other.y

    # Multiplies the vector by a scalar
    def multiply(self, k):
        self.x *= k
        self.y *= k
        return self
    
    # Magic method for *
    # If the arguments are two vectors, it returns the dot product
    # Otherwise, returns the product by a scalar
    
    def __mul__(self, x):
        try:
            return self.dot(x)
        except:
            return self.copy().multiply(x)

    # Magic method for * when the lefthand side is not a vector
    def __rmul__(self, k):
        return self.copy().multiply(k)
    
    # Divides the vector by a scalar
    def divide(self, k):
        return self.multiply(1/k)

    # Magic method for /
    def __truediv__(self, k):
        return self.copy().divide(k)
    
    # Normalizes the vector
    def normalize(self):
        return self.divide(self.length())
    
    # Returns a normalized version of the vector
    def getNormalized(self):
        return self.copy().normalize()
       
    # Returns the length of the vector
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    # Returns the squared length of the vector
    def lengthSquared(self):
        return self.x**2 + self.y**2
    
    # Reflect this vector on a normal
    def reflect(self, normal):
        n = normal.copy()
        n.multiply( 2*self.dot(normal) )
        self.subtract(n)
        return self

    # Returns the angle between this vector and another one
    # You will need to use the arccosine function:
    # acos in the math library
    def angle(self, other):
        pass



class Wall:
    def __init__(self, x, border, color):
        self.x = x
        self.border = border
        self.color = color
        self.normal = Vector((1,0))
        self.edgeR = x + 1 + self.border
        self.edgeL = x - 1 - self.border

    def draw(self, canvas):
        canvas.draw_line((self.x, 0),
                         (self.x, CANVAS_HEIGHT),
                         self.border*2+1,
                         self.color)
    def hit(self, ball):
        hR = (ball.offsetL() <= self.edgeR)
        hL = (ball.offsetR() >= self.edgeL)
        return hR and hL

    
class Ball:
    def __init__(self, pos, vel, radius, border, color):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.border = 1
        self.color = color
        
        speed = 10.0
        x = 0.0
        y = 180.0
        direction = 200
        width = 10
        height = 10
        
    def offsetL(self):
        return self.pos.x - self.radius
       
    def offsetR(self):
        return self.pos.x + self.radius
       
    def update(self):
        self.pos.add(self.vel)
        if self.pos.y + self.radius < 0:
            self.pos.y = CANVAS_HEIGHT + self.radius
        elif self.pos.y - self.radius > CANVAS_HEIGHT:
            self.pos.y = -self.radius

    def draw(self, canvas):
        canvas.draw_circle(self.pos.getP(),
                              self.radius,
                              self.border,
                              self.color,
                              self.color)
        
    def bounce(self, normal):
        self.vel.reflect(normal)

        
        
#i have added to the interaction class by adding the player to it so the player stops when they heit one of the walls
#need to make the balls bounce off of the player.
class Interaction:
    def __init__(self):
        self.balls = []
        self.walls = []
        self.player = []
    
    def addWall(self, wall):
        self.walls.append(wall)

    def addBall(self, ball):
        self.balls.append(ball)
        
    def addPlayer(self, player):
        self.player.append(player)

    def update(self):
        for ball in self.balls:
            ball.update()
            for wall in self.walls:
                if wall.hit(ball):
                    ball.bounce(wall.normal)
                    
        for player in self.player:
            player.update()
            for wall in self.walls:
                if wall.hit(player):
                    stop = (0,0)
                    player.move(Vector(stop))
        
    def draw(self, canvas):
        self.update()
        for wall in self.walls:
            wall.draw(canvas)
        for ball in self.balls:
            ball.draw(canvas)
        for player in self.player:
            player.draw(canvas)
            
            
#i have added a player class that draws and controls the players movement similar to the way that the balls work
class Player:
    
    def __init__(self, pos):
        self.pos = pos
        vel = (0,0)
        self.width = 30
        self.vel = Vector(vel)
        self.border = 1
        self.color = 'red'
        
        
        
        
    def offsetL(self):
        return self.pos.x - self.width
       
    def offsetR(self):
        return self.pos.x + self.width
    
    def move(self, other):
        speed = 7
        self.vel = other
        self.vel.multiply(speed)
    def update(self):
        
        player.pos.add(self.vel)
        
        if self.pos.y + self.width < 0:
            self.pos.y = CANVAS_HEIGHT + self.radius
        elif self.pos.y - self.width > CANVAS_HEIGHT:
            self.pos.y = -self.width

    def draw(self, canvas):
        a = self.pos.x - self.width
        b = self.pos.y - 5
        c = self.pos.x + self.width
        d = self.pos.y
        canvas.draw_polygon([(a, b), (a, d), (c, d), (c, b)], self.border, self.color, self.color)
        
        
    def bounce(self, normal):
        self.vel.reflect(normal)
#i have added eventhandlers to detect when the player has pressed 
#an arrow key and when they let go of a key.
def keydown(key):
    left = (-1,0)
    right = (1,0)
    
    if key == simplegui.KEY_MAP['right']:
        player.move(Vector(right))
    elif key == simplegui.KEY_MAP['left']:
        player.move(Vector(left))
        
def keyup(key):
    stop = (0,0)
    player.move(Vector(stop))
        
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 300
        
i = Interaction()

p = (300,200)
v = (5,-1)
b1 = Ball(Vector(p), Vector(v), 20, 0, 'blue')

p = (300,300)
player = Player(Vector(p))

i.addBall(b1)
i.addPlayer(player)

p = (300,100)
v = (-7.5,3)
b2 = Ball(Vector(p), Vector(v), 20, 0, 'green')
i.addBall(b2)


w1 = Wall(600, 5, 'red')
i.addWall(w1)

w2 = Wall(300, 5, 'red')
i.addWall(w2)

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("ball-wall", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(i.draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# Start the frame animation
frame.start()
