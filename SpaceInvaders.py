import turtle
from functools import partial
import math
from time import sleep
from tkinter import TclError
import sys

# This code was produced by Billy Rebecchi of Sandwell Academy for the 1978 project of West Bromwich Albion
# The foundation of this code was built upon the tphysics library, Copyright of Billy Rebecchi
# tphysics is open source and free for use by anyone, for any purpose
# See http://github.com/thebillington/tphysics for more information on distribution rights

#ENGINE

#Create a game object to hold all of our physics
class Game(object):

    #Initialize
    def __init__(self, name = "Space Invaders", width = 600, height = 600, colour = "black", sleep_time = 0) :

        #Create a screen and set the name
        self.window = turtle.Screen()
        self.window.title(name)
        self.window.screensize(width, height, colour)

        #Create a turtle to do our drawing
        self.t = turtle.Turtle()
        
        #Hide the turtle
        self.t.hideturtle()
        
        #Disable the tracer
        self.window.tracer(0, 0)

        #Create a list of shapes
        self.shapes = []
        
        #Create a key listener
        self.keylistener = KeyListener(self.window)
        
        #Create an empty list of sprites
        self.sprites = []

        # Set the sleep time
        self.sleep = sleep_time

        # Set the colour
        self.colour = "light green"

        # Add the box to the shapes
        self.box = Rectangle(0, 0, 650, 650)
        self.box.fill_colour = colour
        self.box.line_colour = self.colour
        self.shapes.append(self.box)
    
    #Define a function to add a shape
    def add_shape(self, shape):

        #Add the shape
        self.shapes.append(shape)
    
    #Define a function to add a shape
    def add_player(self, p):

        #Add the shape
        self.shapes.extend(p.shapes)

        # Add the buller
        self.shapes.append(p.bullet)

        # Store the player
        self.player = p
    
    #Define a function to add a shape
    def add_object(self, obj):

        #Add the shape
        self.shapes.extend(obj.shapes)
        
    #Define a function to add a sprite
    def add_sprite(self, sprite):
        
        #Add the sprite
        self.sprites.append(sprite)
    
    #Create a function to iterate over each of the shapes and draw them on screen
    def update(self):

        #Check for game exit
        try:
            
            #Clear the canvas
            self.t.clear()

            # Check if the player has fired
            if self.player.fired:

                # Move the bullet
                self.player.bullet.y += 5
        
            #For each of the shapes in the dictionary, draw them
            for s in self.shapes:
                
                #Check the type of the shape
                if s.type == Shape.RECT:
                    self.rectangle(s)
            
            #Update the screen
            self.window.update()

            # Sleep
            sleep(self.sleep)

        except TclError as e:
            print("Program exited successfully.")
            sys.exit()

    # Function to return the left edge of the screen
    def screen_left(self):

        # Return the left side of the screen
        return self.box.x - self.box.width / 2

    # Function to return the right edge of the screen
    def screen_right(self):

        # Return the right side of the screen
        return self.box.x + self.box.width / 2
    
    #Create a function to allow us to draw a rectangle
    def rectangle(self, s):

        # Check if the shape should be drawn or not
        if s.drawn:
        
            #Check whether the line should be drawn
            if s.line:
                #Set the colour of the line
                self.t.color(s.line_colour)
            else:
                #Set the colour of the line to the fill colour
                self.t.color(s.fill_colour)
            
            #Move the pen to the correct position
            self.t.penup()
            self.t.goto(s.x - (s.width/2), s.y + (s.height/2))
            self.t.pendown()
            
            #If the shape should be filled
            if s.fill:
                #Start the fill
                self.t.begin_fill()
            
            #Draw the rectangle
            for i in range(2):
                self.t.forward(s.width)
                self.t.right(90)
                self.t.forward(s.height)
                self.t.right(90)
            
            #If the shape should be filled
            if s.fill:
                #Set the colour and end the fill
                self.t.color(s.fill_colour)
                self.t.end_fill()
        
    #Create a function to add a mouse click
    def addclick(self, f, m=1):
        
        #Add the function to the click listener
        self.window.onclick(f, m)
    
    #Create a function to add a key listener
    def addkeypress(self, f, key):
        
        #Add the key and start listening
        self.window.onkey(f, key)
        self.window.listen()
        
    #Create a function to check whether a key is currently being pressed
    def ispressed(self, k):
        
        #Return the key listener check
        return self.keylistener.isPressed(k)

# KEYS

#Create a key listener class
class KeyListener(object):
    
    #List of keys
    keys = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "space", "Up", "Down", "Left", "Right"]
    
    #Constructor
    def __init__(self, window):
        
        #Store the window
        self.window = window
        
        #Run the setup function for the dictionary
        self.setup()
        
        #Setup the key listeners
        self.createListeners()
        
    #Function to initialize the key listener
    def setup(self):
        
        #Create a dictionary to store the keys that are currently being pressed
        self.pressed = {}
        
        #For each of the keys, set them to false in the dictionary
        for k in KeyListener.keys:
            self.pressed[k] = False
    
    #Function to handle key down events
    def keyDown(self, k):
        
        #Add this key to the list of pressed keys
        self.pressed[k] = True
    
    #Function to handle key up events
    def keyUp(self, k):
        
        #Add this key to the list of pressed keys
        self.pressed[k] = False
        
    #Function to add key listeners for each key
    def createListeners(self):
        
        #For each of the keys, add a listener
        for k in KeyListener.keys:
            
            #Set the current key
            fp = partial(self.keyDown, k)
            fr = partial(self.keyUp, k)
            
            #Add the on key listeners
            self.window.onkeypress(fp, k)
            self.window.onkeyrelease(fr, k)
        
        #Start the listener
        self.window.listen()
            
    #Function to check whether a key is pressed
    def isPressed(self, k):
        
        #Return whether the key is pressed or not
        return self.pressed[k]

# SHAPES

#Define a class to hold opur shape
class Shape(object):
    
    #Types
    POINT = "point"
    RECT = "rectangle"

    #Implement our init function
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        
        self.line_colour = "black"
        self.fill_colour = "red"
        self.fill = True
        self.line = True

        self.drawn = True

    #Define pythagoral function
    def pythagoras(self, s):

        #Return the distance between the shapes
        return math.sqrt(math.pow(abs(self.x - s.x) , 2) + math.pow(abs(self.y - s.y) , 2))

#Create our rectangle class
class Rectangle(Shape):

    #Define our initialize function
    def __init__(self, x, y, width, height):

        #Create our derivative shape
        super(Rectangle, self).__init__(x, y, Shape.RECT)
        self.width = width
        self.height = height

    #Define a function to get the corners
    def update_corners(self):

        #Fetch the x, y, width and height
        x = self.x
        y = self.y
        width = self.width
        height = self.height

        #Create our corners
        self.corners = [Point(x - width / 2, y + height / 2), Point(x - width / 2, y - height / 2), Point(x + width / 2, y + height / 2), Point(x + width / 2, y - height / 2)]
        
    #define a collice function
    def collide(self, s):

        #If s is a rectangle
        if s.type == Shape.RECT:

            #Craete our collide x variable
            col_x = abs(self.x - s.x) < (self.width / 2) + (s.width / 2)
            #Create our collide y variables
            col_y = abs(self.y - s.y) < (self.height / 2) + (s.height / 2)
            #return col_x and col_y
            return (col_x and col_y)
            
        return("Collision not implemented")

    # Create a function to check if the object is off screen
    def off_screen(self):

        # Return whether the player is off screen
        return self.x - self.width / 2 < -325 or self.x + self.width > 325 or self.y - self.height / 2 < -325 or self.y + self.height > 325 

# SPACE INVADERS

# Create an object to hold the player shapes and allow the user to move the player
class Player(object):

    # Create a constructor
    def __init__(self, x, y):

        # Set the width and heights of the tank
        self.tankW = 80
        self.tankH = 20

        # Set the colour of the player
        self.colour = "light green"

        # Generate an empty list of component shapes
        self.shapes = []

        # Add the tank and the turret
        self.shapes.append(Rectangle(x, y, self.tankW, self.tankH))
        self.shapes.append(Rectangle(x, y + self.tankH / 2 + self.tankH / 4, self.tankW / 4, self.tankH / 2))

        # Set the colour of each shape
        for s in self.shapes:
            s.fill_colour = self.colour
            s.line_colour = self.colour

        # Set the fired variable to false
        self.fired = False

        # Generate the bullet
        self.bullet = Rectangle(x, y + self.tankH, 5, 5)
        self.bullet.fill_colour = self.colour
        self.bullet.line_colour = self.colour

    # Function to reset the bullet
    def reset_bullet(self):

        # Set bullet to none
        self.fired = False
        self.bullet.x = self.shapes[0].x
        self.bullet.y = self.shapes[0].y + self.tankH

    # Create a function to try and fire
    def fire(self):

        # Fire a bullet
        self.fired = True

    # Check whether the bullet has collided with an obstacle
    def hit_obstacle(self, obstacles):

        # Look at each shape in the obstacle
        for s in obstacles.shapes:

            # Check if this has collided with the bullet and it hasn't already been hit
            if s.collide(self.bullet) and s.drawn:

                # Remove the shame
                s.drawn = False
                return True

    # Check whether the bullet has collided with an enemy
    def hit_enemy(self, enemies):

        # Look at each shape in the enemies list
        for s in enemies.shapes:

            # Check if this has collided with the bullet and it hasn't already been hit
            if s.collide(self.bullet) and s.drawn:

                # Remove the shame
                s.drawn = False
                return True

    # Create a function to allow the player to move
    def move(self, x):

        # Move each of the shapes by x
        for s in self.shapes:
            s.x += x

        # If the bullet hasn't been fired, fire it
        if not self.fired:
            self.bullet.x += x

    # Return the shapes
    def get_shapes(self):

        # Return the list of composite shapes
        return self.shapes

    # Create a function to return the left hand side of the player
    def left(self):

        # Return the left hand value of the player
        return self.shapes[0].x - self.shapes[0].width / 2

    # Create a function to return the right edge of the player
    def right(self):

        # Return the right hand value of the player
        return self.shapes[0].x + self.shapes[0].width / 2

    # Create a function set the left hand position of the player
    def set_left(self, x):

        # Set the x location of the base shape
        self.shapes[0].x = x + self.shapes[0].width / 2

        # Set the location of all the other shapes in the player
        for s in self.shapes:
            s.x = self.shapes[0].x

        # Set the x location of the buller if it hasn't been fired
        if not self.fired:
            self.bullet.x = self.shapes[0].x

    # Create a function set the left hand position of the player
    def set_right(self, x):

        # Set the x location of the player
        self.shapes[0].x = x - self.shapes[0].width / 2

        # Set the location of all the other shapes in the player
        for s in self.shapes:
            s.x = self.shapes[0].x

        # Set the x location of the buller if it hasn't been fired
        if not self.fired:
            self.bullet.x = self.shapes[0].x

# Create an object to hold the obstacles
class Obstacle(object):

    # Create a constructor
    def __init__(self, x, y):

        # Create an empty list of shapes for this obstacle to hold
        self.shapes = []

        # Set the width and height of the obstacle
        w = 80
        h = 80

        # Set the number of individual shapes in the rows/columns of the obstacle
        components = 4

        # Set the colour of the obstacles
        colour = "light green"
        
        # Iteratively produce the shapes and add them to the list of shapes
        for i in range(components):
            for j in range(components):

                # Create the rectangle at the correct position and fill it in
                s = Rectangle(x - w / 2 + (i * (w / components)), y - h / 2 + (j * (h / components)), w / components, h /components)
                s.fill_colour = colour
                s.line_colour = colour

                # Add the shape to the list of shapes
                self.shapes.append(s)

# Create a class to generate and hold set of obstacles
class Obstacles(object):

    # Constructor
    def __init__(self):

        # Create an empty list of shapes
        self.shapes = []

        # Set the base x and y
        baseX = -260
        baseY = -100

        # Generate the obstacles and add their shapes to the list of shapes
        for i in range(4):

            # Generate an obstacle at the correct location
            self.shapes.extend(Obstacle(baseX + i * 160 + 40, baseY).shapes)

# Create a function to generate the enemies
class Enemies(object):

    # Constructor
    def __init__(self, x, y, w, h, nx, ny, direction):

        # Set the left and right location of all the players
        self.left = x
        self.right = x + (2 * nx * w)
        self.absLeft = x
        self.absRight = -x

        # Create an empty list to hold all of the enemies
        self.shapes = []

        # Iteratively create the correct number of enemies
        for i in range(nx):
            for j in range(ny):

                # Create an enemy at the correct location
                self.shapes.append(Rectangle(x + (i * 2 * w), y + (j * 2 * h), w, h))

        # Set all the shapes to white
        for s in self.shapes:
            s.fill_colour = "white"
            s.line_colour = "white"

        # Store the direction of movement
        self.direction = direction

    # Define a function to move the invaders
    def move(self):

        # Check if the enemies need to switch direction
        if self.left < self.absLeft or self.right > self.absRight:

            # Switch direction
            self.direction *= -1

            # Look at each shape
            for s in self.shapes:

                # Move down
                s.y -= 5

        # Move the overall left and right position
        self.left += self.direction
        self.right += self.direction

        # For each shape
        for s in self.shapes:

            # Move the shape
            s.x += self.direction
