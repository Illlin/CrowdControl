import pyray
from sprite import Sprite, Timer, DrawMode
import random

INPUTS = ["TOP", "BOTTOM"]


def main(screen_size): # Game stuff here
    # Init the sprite, Framerate, File location, Position, number of frames
    background = pyray.load_texture("PythonGame/Assets/background.png")

    paddle = Sprite(5, "PythonGame/Assets/paddle.png", [100,0],2)
    ball = Sprite(5, "PythonGame/Assets/ball.png", [screen_size[0],0],2)
    # Add all sprites to array for easy updating
    sprites = [paddle, ball]
    
    # Timers are used instead of sleep
    # Control Timers
    intro_timer = Timer(1)
    main_timer = Timer(10)
    end_timer = Timer(1)

    # Game Timers
    ball_timer = Timer(2)
    timers = [intro_timer, main_timer, end_timer, ball_timer]

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
                paddle.hide()
                ball.hide()
                pyray.draw_text("Get ready..!",10,10,80,pyray.RED)
            
            # Start the game
            if intro_timer.done() and intro_timer.running:
                # Set Sprite peramiters
                ball.move_speed = 50
                intro_timer.stop()
                main_timer.start()
                ball_timer.start()
                paddle.show()
                ball.show()
                ball.position = [screen_size[0], random.randint(0, screen_size[1]-ball.size[1])]
                ball.goal = [-screen_size[0], ball.position[1]]

            # Main game stuff here
            if main_timer.running:
                
                if ball.get_collision(paddle):
                    pass #collide
            # Ending
            if main_timer.done():
                main_timer.stop()
                end_timer.start()
                man.hide()
                gun.hide()
                pyray.draw_text("You won? Maybe?",10,10,80,pyray.RED)
            
            # Return to next Game
            if end_timer.done():
                return False # return win or lose so music can play


            # Each frame, Render and update each sprite and timers
            [x.draw() for x in sprites]
            [x.animate(delta) for x in sprites]
            [x.tick(delta) for x in timers]