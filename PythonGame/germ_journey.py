import pyray
from sprite import Sprite, Timer, DrawMode
import random
import math

INPUTS = ["UP", "DOWN", "LEFT", "RIGHT"]

def main(screen_size, inp): # Game stuff here

    # Init the sprite, Framerate, File location, Position, number of frames
    background = pyray.load_texture("PythonGame/Assets/petri_dish_bg.png")

    boris = Sprite(5, "PythonGame/Assets/bacteria boris.png", [128,128],2)
    goal = Sprite(5, "PythonGame/Assets/flag.png", [128,128],2)
    target = Sprite(5, "PythonGame/Assets/target.png", [128,128],2)

    # Add all sprites to array for easy updating
    sprites = [boris, goal, target]
    
    # Timers are used instead of sleep
    # Control Timers
    intro_timer = Timer(1)
    main_timer = Timer(10)
    end_timer = Timer(1)

    # Game Timers
    man_timer = Timer(1)
    timers = [intro_timer, main_timer, end_timer]
    reached_goal = False
    square_size = 20

    # Start the main game timer
    intro_timer.start()

    # Load background

    # Main game loop
    while not pyray.window_should_close():
        # Time in s since last frame
        delta = pyray.get_frame_time()

        # This stuff happens while drawing
        with DrawMode():
            # Ignore this
            pyray.clear_background(pyray.BLACK)
            source = pyray.Rectangle(0, 0, screen_size[0], -screen_size[1])
            pyray.draw_texture_pro(background, source, pyray.Rectangle(0, 0, *screen_size), (0,0), 0, pyray.WHITE)

            # Draw the intro stuff
            if intro_timer.running:
                for sprite in sprites:
                    sprite.hide()

                pyray.draw_text("BACTERIA BORIS HOLY SHIT",10,10,80,pyray.RED)
            
            # Start the game
            if intro_timer.done() and intro_timer.running:
                # Set Sprite peramiters

                boris.move_speed = 10
                intro_timer.stop()
                main_timer.start()

                boris.set_pos(0, random.randint(0, math.floor(screen_size[1]/square_size) * square_size))
                goal.set_pos(random.randint(math.floor(screen_size[0]/square_size) -3, math.floor(screen_size[0]/square_size)) * square_size, random.randint(0, math.floor(screen_size[1]/square_size) * square_size))

                for sprite in sprites:
                    sprite.show()

                print("Still running")

            # Main game stuff here
            if main_timer.running:
                # Process man
                if boris.get_collision(goal):
                    reached_goal = True
                
                if inp.get_top() == "UP" or pyray.is_key_pressed(pyray.KeyboardKey.KEY_DOWN):
                    target[1] -= square_size
                if inp.get_top() == "DOWN" or pyray.is_key_pressed(pyray.KeyboardKey.KEY_DOWN):
                    target[1] += square_size
                if inp.get_top() == "LEFT" or pyray.is_key_pressed(pyray.KeyboardKey.KEY_DOWN):
                    target[0] -= square_size
                if inp.get_top() == "RIGHT" or pyray.is_key_pressed(pyray.KeyboardKey.KEY_DOWN):
                    target[0] += square_size

                if not reached_goal:
                    boris.goal(target.position)

                
            # Ending
            if main_timer.done():
                main_timer.stop()
                end_timer.start()
                for sprite in sprites:
                    sprite.hide()

                pyray.draw_text("You won? Maybe?",10,10,80,pyray.RED)
            
            # Return to next Game
            if end_timer.done():
                return False # return win or lose so music can play


            # Each frame, Render and update each sprite and timers
            [x.draw() for x in sprites]
            [x.animate(delta) for x in sprites]
            [x.tick(delta) for x in timers]