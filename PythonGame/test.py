import pyray
from sprite import Sprite, Timer, DrawMode

INPUTS = ["UP", "DOWN", "LEFT", "RIGHT"]
PHONE_BACKGROUN = "background.png"
BUTTON_POS = [[10,10],[10,30],[5,20],[15,20]]

def main(screen_size, inp): # Game stuff here
    u = 0
    d = 0
    l = 0
    r = 0


    # Init the sprite, Framerate, File location, Position, number of frames
    background = pyray.load_texture("PythonGame/Assets/background.png")

    man = Sprite(5, "PythonGame/Assets/AppleSmall.png", [128,128],2)
    gun = Sprite(5, "PythonGame/Assets/gun.png", [128,128],2)
    # Add all sprites to array for easy updating
    sprites = [man, gun]
    
    # Timers are used instead of sleep
    # Control Timers
    intro_timer = Timer(1)
    main_timer = Timer(10)
    end_timer = Timer(1)

    # Game Timers
    man_timer = Timer(1)
    timers = [intro_timer, main_timer, end_timer, man_timer]

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
                man.hide()
                gun.hide()
                pyray.draw_text("Schmoove about and do stuff",10,10,80,pyray.RED)
            
            # Start the game
            if intro_timer.done() and intro_timer.running:
                # Set Sprite peramiters
                man.goal = [pyray.get_random_value(0,screen_size[0]), pyray.get_random_value(0,screen_size[1])]
                print(man.goal)
                man.move_speed = 10
                intro_timer.stop()
                main_timer.start()
                man.show()
                gun.show()
                print("Still running")

            # Main game stuff here
            if main_timer.running:
                # Process man
                if man.at_goal:
                    man_timer.start()
                    if man_timer.done():
                        man_timer.stop()
                        man_timer.reset()
                        man.goal = [pyray.get_random_value(0,screen_size[1]), pyray.get_random_value(0,screen_size[0])]

                ## GET NETWORK STUFF
                # Up
                buttons = inp.get_inputs_sum()
                while buttons["UP"] >= u:
                    u += 1
                    gun.position[1] -= 10

                # Down
                while buttons["DOWN"] >= d:
                    d += 1
                    gun.position[1] += 10
                
                # Left
                while buttons["LEFT"] >= l:
                    l += 1
                    gun.position[0] -= 10
                
                # Right
                while buttons["RIGHT"] >= r:
                    r += 1
                    gun.position[0] += 10

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