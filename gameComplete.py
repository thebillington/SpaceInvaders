# Import everything we need from the space invaders code
from SpaceInvaders import *

# Create a game object
game = Game()

# Create a player and set the position
player = Player(0, -250)

# Add the player to the game
game.add_player(player)

# Create an obstacle
obstacles = Obstacles()

# Add the obstacle to the game
game.add_object(obstacles)

# Create a batch of enemies
enemies = Enemies(-250, 80, 20, 20, 10, 6, 1)

# Add the enemies to the game
game.add_object(enemies)

# Create a loop to keep checking if keys have been pressed or if the bullets have hit an invader
while True:

    # Check if the right key is pressed and if so, move right on x axis
    if game.ispressed("Right"):
        player.move(2)
        
    # Check if the left key is pressed and if so, move left on x axis
    if game.ispressed("Left"):
        player.move(-2)

    # Move the enemies
    enemies.move()

    # Fire if the space key is pressed and we haven't already fired
    if game.ispressed("space") and not player.fired:
        player.fire()

    # Check if the player has hit an obstacle
    if player.hit_obstacle(obstacles) or player.hit_enemy(enemies):

        # Reset the bullet
        player.reset_bullet()

    # If the players bullet goes off the screen, reset it
    if player.bullet.off_screen():
        player.reset_bullet()

    # Check if the player has gone off the left of the screen
    if player.left() < game.screen_left():

        # Set the player position back onto the screen
        player.set_left(game.screen_left())

    # Check if the player has gone off the right of the screen
    if player.right() > game.screen_right():

        # Set the player position back onto the screen
        player.set_right(game.screen_right())

    # Re-draw
    game.update()
