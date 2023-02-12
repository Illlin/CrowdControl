import pyray
from sprite import Sprite, Timer, DrawMode
import random
import math

INPUTS = ["UP", "DOWN", "LEFT", "RIGHT"]
PHONE_BACKGROUN = "background.png"

def main(screen_size, inp): # Game stuff here
    music = pyray.load_music_stream("PythonGame/Assets/transition.wav")
    music.looping = False

    pyray.play_music_stream(music)

    # Init the sprite, Framerate, File location, Position, number of frames
    background = pyray.load_texture("PythonGame/Assets/germ_title_bg_as.png")

    boris = Sprite(5, "PythonGame/Assets/Bacteria Boris.png", [128,128],2)
    boris.scale = 0.1
    text = Sprite(5, "PythonGame/Assets/germ_title.png", [-500,200],1)
    text.show()
    text.move_speed = 500
    text.goal = [500,200]

    flag = Sprite(5, "PythonGame/Assets/flag.png", [128,128],2)
    flag.scale = 0.4
    target = Sprite(5, "PythonGame/Assets/gun.png", [128,128],2)
    target.scale = 0.3

    # Add all sprites to array for easy updating
    sprites = [boris, flag, target,text]
    
    # Timers are used instead of sleep
    # Control Timers
    intro_timer = Timer(4)
    b_timer = Timer(3)
    main_timer = Timer(10)
    end_timer = Timer(1)

    # Game Timers
    man_timer = Timer(1)
    timers = [intro_timer, main_timer, end_timer,b_timer]
    reached_goal = False
    square_size = 100

    # Start the main game timer
    intro_timer.start()
    b_timer.start()

    # Load background

    # Main game loop
    u = 0
    d = 0
    l = 0
    r = 0
    win = False
    while not pyray.window_should_close():
        # Time in s since last frame
        delta = pyray.get_frame_time()

        # This stuff happens while drawing
        with DrawMode():
            pyray.update_music_stream(music)
            # Ignore this
            pyray.clear_background(pyray.BLACK)
            source = pyray.Rectangle(0, 0, 896, -512)
            pyray.draw_texture_pro(background, source, pyray.Rectangle(0, 0, *screen_size), (0,0), 0, pyray.WHITE)

            # Draw the intro stuff
            if intro_timer.running:

                for sprite in sprites:
                    sprite.hide()
                text.show()
                boris.show()
                boris.set_pos_center([screen_size[0]/2,800])
                #pyray.draw_text("BACTERIA BORIS HOLY SHIT",10,10,80,pyray.RED)

            if b_timer.done() and b_timer.running:
                b_timer.stop()
                b_timer.reset()
                boris.goal = target.position[:]
                boris.move_speed = 800
                print("BEEEE")
            
            
            # Start the game
            if intro_timer.done() and intro_timer.running:
                background = pyray.load_texture("PythonGame/Assets/petri_dish_bg.png")
                music = pyray.load_music_stream("PythonGame/Assets/cool.wav")
                pyray.play_music_stream(music)
                # Set Sprite peramiters

                boris.move_speed = 200
                intro_timer.stop()
                main_timer.start()

                #boris.set_pos([0, random.randint(0, math.floor(screen_size[1]/square_size) * square_size)])
                flag.set_pos([1600, random.randint(200,800)])

                for sprite in sprites:
                    sprite.show()

                print("Still running")
                buttons = inp.get_inputs_sum()
                if "UP" in buttons:
                    while buttons["UP"] >= u:
                        u += 1
                    # Down
                if "DOWN" in buttons:
                    while buttons["DOWN"] >= d:
                        d += 1
                    # Left
                if "LEFT" in buttons:
                    while buttons["LEFT"] >= l:
                        l += 1
                # Right
                if "RIGHT" in buttons:
                    while buttons["RIGHT"] >= r:
                        r += 1

            # Main game stuff here
            if main_timer.running:
                text.hide()
                # Process man
                buttons = inp.get_inputs_sum()
                if "UP" in buttons:
                    while buttons["UP"] >= u:   
                        u += 1
                        target.position[1] -= square_size

                # Down
                if "DOWN" in buttons:
                    while buttons["DOWN"] >= d:   
                        d += 1
                        target.position[1] += square_size
                
                # Left
                if "LEFT" in buttons:
                    while buttons["LEFT"] >= l:
                        l += 1
                        target.position[0] -= square_size
                    
                # Right
                if "RIGHT" in buttons:
                    while buttons["RIGHT"] >= r:
                        r += 1
                        target.position[0] += square_size

                if pyray.is_key_pressed(pyray.KeyboardKey.KEY_UP):
                    target.position[1] -= square_size
                if pyray.is_key_pressed(pyray.KeyboardKey.KEY_DOWN):
                    target.position[1] += square_size
                if pyray.is_key_pressed(pyray.KeyboardKey.KEY_LEFT):
                    target.position[0] -= square_size
                if pyray.is_key_pressed(pyray.KeyboardKey.KEY_RIGHT):
                    target.position[0] += square_size

                if not boris.get_collision(flag):
                    #print(target)
                    boris.set_goal_center([target.position[0]+target.size[0]*target.scale,target.position[1]+target.size[1]*target.scale])
                else:
                    win = True
                    boris.move_speed = 0

                
            # Ending
            if main_timer.done():
                main_timer.stop()
                end_timer.start()
                for sprite in sprites:
                    sprite.hide()

                pyray.draw_text("You won? Maybe?",10,10,80,pyray.RED)
            
            # Return to next Game
            if end_timer.done():
                return win # return win or lose so music can play


            # Each frame, Render and update each sprite and timers
            [x.draw() for x in sprites]
            [x.animate(delta) for x in sprites]
            [x.tick(delta) for x in timers]