import pyray
from sprite import Sprite, Timer, DrawMode
import random

INPUTS = ["UP", "DOWN", "LEFT", "RIGHT"]


def main(screen_size): # Game stuff here
    # Init the sprite, Framerate, File location, Position, number of frames
    background = pyray.load_texture("PythonGame/Assets/background.png")

    man_up = Sprite(5, "PythonGame/Assets/apple_man_up.png", [128,128],2)
    man_right = Sprite(5, "PythonGame/Assets/apple_man_right.png", [128,128],2)
    man_down = Sprite(5, "PythonGame/Assets/apple_man_down.png", [128,128],2)
    man_left = Sprite(5, "PythonGame/Assets/man_left.png", [128,128],2)

    doc_1 = Sprite(5, "PythonGame/Assets/doctor.png", [128,128],2)
    doc_2 = Sprite(5, "PythonGame/Assets/doctor.png", [128,128],2)

    # Add all sprites to array for easy updating
    man_sprites = [man_up, man_right, man_down, man_left]
    doc_sprites = [doc_1, doc_2]
    
    # Timers are used instead of sleep
    # Control Timers
    intro_timer = Timer(1)
    main_timer = Timer(10)
    end_timer = Timer(2)

    # Game Timers
    doctor_timer = Timer(2)
    doc_choice = 1
    doc_1_dir, doc_2_dir = 0, 0
    timers = [intro_timer, main_timer, end_timer, doctor_timer]

    starting_pos_list = [[0, screen_size[1]/2], [screen_size[0], screen_size[1]/2], [screen_size[0]/2, 0], [screen_size[0]/2, screen_size[1]]]
    win = True

    intro_timer.start()

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
                for sprite in man_sprites:
                    sprite.hide()
        
                pyray.draw_text("THE EVIL DRS WANT YOUR LUNGS!!!!!",10,10,50,pyray.RED)
            
            # Start the game
            if intro_timer.done() and intro_timer.running:
                # Set Sprite peramiters
                intro_timer.stop()
                main_timer.start()
                man_up.show()

            # Main game stuff here
            if main_timer.running:
                doctor_timer.start()
                if doctor_timer.done():
                    doctor_timer.reset()
                    if doc_choice == 1:
                        start_pos_1 = random.choice(starting_pos_list)
                        doc_1.set_pos(start_pos_1)
                        doc_1.move_speed(4)
                        doc_1.goal([screen_size[0]/2, screen_size[1]/2])
                        doc_1.show()
                        doc_choice = 2
                        doc_1_dir = starting_pos_list.index(start_pos_1)

                    elif doc_choice == 2:
                        start_pos_2 = random.choice(starting_pos_list)
                        doc_2.set_pos(start_pos_2)
                        doc_2.move_speed(4)
                        doc_2.goal([screen_size[0]/2, screen_size[1]/2])
                        doc_2.show()
                        doc_choice = 1
                        doc_2_dir = starting_pos_list.index(start_pos_2)

                if doc_1.get_collision(man_sprites[doc_1_dir]):
                    doc_1.goal(start_pos_1)
                    doc_1.move_speed(100)
                
                elif doc_2.get_collision(man_sprites[doc_2_dir]):
                    doc_2.goal(start_pos_2)
                    doc_2.move_speed(100)
                
                else:
                    for man_sprite in man_sprites:
                        for doc_sprite in doc_sprites:
                            if man_sprite.get_collision(doc_sprite):
                                win = False

            # Ending
            if main_timer.done():
                main_timer.stop()
                end_timer.start()
                for sprite in man_sprites + doc_sprites:
                    sprite.hide()

                if win:
                    pyray.draw_text("You won a fish",10,10,80,pyray.RED)
                else:
                    pyray.draw_text("You lose a fish :(",10,10,80,pyray.RED)

            # Return to next Game
            if end_timer.done():
                return False # return win or lose so music can play


            # Each frame, Render and update each sprite and timers
            [x.draw() for x in man_sprites+doc_sprites]
            [x.animate(delta) for x in man_sprites+doc_sprites]
            [x.tick(delta) for x in timers]