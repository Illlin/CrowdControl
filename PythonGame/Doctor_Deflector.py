import pyray
from sprite import Sprite, Timer, DrawMode
import random

INPUTS = ["UP", "DOWN", "LEFT", "RIGHT"]


def main(screen_size): # Game stuff here
    # Init the sprite, Framerate, File location, Position, number of frames
    background = pyray.load_texture("PythonGame/Assets/background.png")

    man_up = Sprite(5, "PythonGame/Assets/man_up.png", [-100,-100],2)
    man_right = Sprite(5, "PythonGame/Assets/man_right.png", [-100,-100],2)
    man_down = Sprite(5, "PythonGame/Assets/man_down.png", [-100,-100],2)
    man_left = Sprite(5, "PythonGame/Assets/man_left.png", [-100,-100],2)

    apple = Sprite(5, "PythonGame/Assets/AppleSmall.png", [-100,-100],2)
    apple_offset = 50

    doc_1 = Sprite(5, "PythonGame/Assets/doctor.png", [100,-100],2)
    doc_2 = Sprite(5, "PythonGame/Assets/doctor.png", [100,-100],2)

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
    timers = [intro_timer, main_timer, end_timer, doctor_timer]

    starting_pos_list = [[0, screen_size[1]/2], [screen_size[0], screen_size[1]/2], [screen_size[0]/2, 0], [screen_size[0]/2, screen_size[1]]]
    start_pos_1, start_pos_2 = starting_pos_list[0], starting_pos_list[1]
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
                apple.show()
                doctor_timer.start()
                if doctor_timer.done():
                    doctor_timer.reset()
                    if doc_choice == 1:
                        start_pos_1 = random.choice(starting_pos_list)
                        doc_1.set_pos(start_pos_1)
                        doc_1.move_speed = 4
                        doc_1.goal = [screen_size[0]/2, screen_size[1]/2]
                        doc_1.show()
                        doc_choice = 2

                    elif doc_choice == 2:
                        start_pos_2 = random.choice(starting_pos_list)
                        doc_2.set_pos(start_pos_2)
                        doc_2.move_speed = 4
                        doc_2.goal = [screen_size[0]/2, screen_size[1]/2]
                        doc_2.show()
                        doc_choice = 1

                if pyray.is_key_pressed(pyray.KeyboardKey.KEY_UP):
                    for man_sprite in man_sprites:
                        man_sprite.hide()
                    man_up.show()
                    apple.set_pos_center([screen_size[0]/2, screen_size[1]/2 - apple_offset])

                # Down
                if pyray.is_key_pressed(pyray.KeyboardKey.KEY_DOWN):
                    for man_sprite in man_sprites:
                        man_sprite.hide()
                    man_down.show()
                    apple.set_pos_center([screen_size[0]/2, screen_size[1]/2 + apple_offset])
                
                # Left
                if pyray.is_key_pressed(pyray.KeyboardKey.KEY_LEFT):
                    for man_sprite in man_sprites:
                        man_sprite.hide()
                    man_left.show()
                    apple.set_pos_center([screen_size[0]/2 - apple_offset, screen_size[1]/2])
                
                # Right
                if pyray.is_key_pressed(pyray.KeyboardKey.KEY_RIGHT):
                    for man_sprite in man_sprites:
                        man_sprite.hide()
                    man_right.show()
                    apple.set_pos_center([screen_size[0]/2 + apple_offset, screen_size[1]/2])
                
                if doc_1.get_collision(apple):
                    doc_1.goal = start_pos_1
                    doc_1.move_speed = 100
                
                elif doc_2.get_collision(apple):
                    doc_2.goal = start_pos_2
                    doc_2.move_speed = 100
                
                else:
                    for man_sprite in man_sprites:
                        for doc_sprite in doc_sprites:
                            if man_sprite.get_collision(doc_sprite):
                                win = False

            # Ending
            if main_timer.done():
                main_timer.stop()
                end_timer.start()
                for sprite in man_sprites + doc_sprites + [apple]:
                    sprite.hide()

                if win:
                    pyray.draw_text("You won a fish",10,10,80,pyray.RED)
                else:
                    pyray.draw_text("You lose a fish :(",10,10,80,pyray.RED)

            # Return to next Game
            if end_timer.done():
                return False # return win or lose so music can play


            # Each frame, Render and update each sprite and timers
            [x.draw() for x in man_sprites + doc_sprites+ [apple]]
            [x.animate(delta) for x in man_sprites + doc_sprites+ [apple]]
            [x.tick(delta) for x in timers]