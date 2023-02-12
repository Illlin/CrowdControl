import pyray
from sprite import Sprite, Timer, DrawMode
import random
import math
import time

INPUTS = ["LEFT", "RIGHT"]
PHONE_BACKGROUN = "background.png"


def main(screen_size, inp): # Game stuff here
    music = pyray.load_music_stream("PythonGame/Assets/transition.wav")
    music.looping = False

    pyray.play_music_stream(music)

    # Init the sprite, Framerate, File location, Position, number of frames
    background = pyray.load_texture("PythonGame/Assets/doctor_open_bg.png")

    man_right = Sprite(5, "PythonGame/Assets/man_right.png", [-100,-100],2)
    man_left = Sprite(5, "PythonGame/Assets/man_left.png", [-100,-100],2)

    text = Sprite(5, "PythonGame/Assets/get_good_soon.png", [0,0],1)
    text.scale = 0.5
    text.offset = (text.size[0]*text.scale)*0.5,(text.size[1]*text.scale)*0.5
    text.set_pos_center([screen_size[0]*0.83, 400])
    text.show()

    apple = Sprite(5, "PythonGame/Assets/AppleSmall.png", [-100,-100],2)
    apple.scale = 0.5
    apple_offset = 150

    doc_1 = Sprite(5, "PythonGame/Assets/DoctorSmall.png", [100,-100],2)
    doc_2 = Sprite(5, "PythonGame/Assets/DoctorSmall.png", [100,-100],2)

    introDoctor = Sprite(5, "PythonGame/Assets/DoctorSmall.png", [100,-100],2)
    introDoctor.scale = 0.01

    # Add all sprites to array for easy updating
    man_sprites = [man_left, man_right]
    doc_sprites = [doc_1, doc_2]
    
    # Timers are used instead of sleep
    # Control Timers
    intro_timer = Timer(4)
    main_timer = Timer(10)
    end_timer = Timer(1)

    # Game Timers
    doctor_timer = Timer(2)
    doc_choice = 1
    timers = [intro_timer, main_timer, end_timer, doctor_timer]

    starting_pos_list = [[-5-doc_1.size[0], screen_size[1]/2], [5+screen_size[0]+doc_1.size[0], screen_size[1]/2]]
    start_pos_1, start_pos_2 = random.choice(starting_pos_list), random.choice(starting_pos_list)
    win = True

    intro_timer.start()

    # Main game loop
    while not pyray.window_should_close():
        # Time in s since last frame
        delta = pyray.get_frame_time()

        # This stuff happens while drawing
        with DrawMode():
            pyray.update_music_stream(music)
            # Ignore this
            pyray.clear_background(pyray.BLACK)
            source = pyray.Rectangle(0, 0, 896,512)
            pyray.draw_texture_pro(background, source, pyray.Rectangle(0, 0, *screen_size), (0,0), 0, pyray.WHITE)

            # Draw the intro stuff
            if intro_timer.running:
                introDoctor.show()
                text.show()
                text.rotation = 10*math.sin(time.time()*2)
                introDoctor.scale *= 1.025
                introDoctor.set_pos_center([screen_size[0]*0.5, screen_size[1]*0.5])
                pyray.draw_text("Keep the doctors at bay!",600,500,50,pyray.GOLD)
            
            # Start the game
            if intro_timer.done() and intro_timer.running:
                introDoctor.hide()
                text.hide()
                background = pyray.load_texture("PythonGame/Assets/reception_bg.png")
                music = pyray.load_music_stream("PythonGame/Assets/bluesy.wav")
                pyray.play_music_stream(music)
                # Set Sprite peramiters
                intro_timer.stop()
                main_timer.start()
                man_right.show()
                man_left.set_pos_center([screen_size[0]/2, screen_size[1]/2])
                man_right.set_pos_center([screen_size[0]/2, screen_size[1]/2])
                apple.set_pos_center([screen_size[0]/2 + apple_offset, screen_size[1]/2])
                doc_1.set_pos_center(start_pos_1)
                doc_2.set_pos_center(start_pos_2)
                doc_1.set_goal_center([screen_size[0]/2, screen_size[1]/2])
                doc_2.set_goal_center([screen_size[0]/2, screen_size[1]/2])
                print(doc_1.position)

            # Main game stuff here
            if main_timer.running:
                print(doc_1.position)
                apple.show()
                doctor_timer.start()
                if doctor_timer.done():
                    doctor_timer.reset()
                    if doc_choice == 1:
                        start_pos_1 = random.choice(starting_pos_list)
                        doc_1.set_pos_center(start_pos_1)
                        doc_1.move_speed = 500
                        doc_1.set_goal_center([screen_size[0]/2, screen_size[1]/2])
                        doc_1.show()
                        doc_choice = 2

                    elif doc_choice == 2:
                        start_pos_2 = random.choice(starting_pos_list)
                        doc_2.set_pos_center(start_pos_2)
                        doc_2.move_speed = 500
                        doc_2.set_goal_center([screen_size[0]/2, screen_size[1]/2])
                        doc_2.show()
                        doc_choice = 1
                
                # Left
                if inp.get_top() == "LEFT" or pyray.is_key_down(pyray.KeyboardKey.KEY_LEFT):
                    for man_sprite in man_sprites:
                        man_sprite.hide()
                    man_left.show()
                    apple.set_pos_center([screen_size[0]/2 - apple_offset, screen_size[1]/2])
                
                # Right
                if inp.get_top() == "RIGHT" or pyray.is_key_down(pyray.KeyboardKey.KEY_RIGHT):
                    for man_sprite in man_sprites:
                        man_sprite.hide()
                    man_right.show()
                    apple.set_pos_center([screen_size[0]/2 + apple_offset, screen_size[1]/2])
                
                if doc_1.get_collision(apple):
                    doc_1.goal = start_pos_1[::]
                    doc_1.move_speed = 100
                
                elif doc_2.get_collision(apple):
                    doc_2.goal = start_pos_2[::]
                    doc_2.move_speed = 100
                
                else:
                    for man_sprite in man_sprites:
                        for doc_sprite in doc_sprites:
                            if man_sprite.get_collision(doc_sprite):
                                man_left.tint = pyray.RED
                                man_right.tint = pyray.RED
                                win = False


            # Return to next Game
            if end_timer.done():
                pyray.stop_music_stream(music)
                return win # return win or lose so music can play


            # Each frame, Render and update each sprite and timers
            [x.draw() for x in man_sprites + doc_sprites+ [apple] + [text]+ [introDoctor]]
            [x.animate(delta) for x in man_sprites + doc_sprites+ [apple] + [introDoctor]+[text]]
            [x.tick(delta) for x in timers]

            if main_timer.done():
                main_timer.stop()
                end_timer.start()
                for sprite in man_sprites + doc_sprites + [apple]:
                    sprite.hide()

                if win:
                    pyray.draw_text("You are safe... for now",650,500,80,pyray.RED)
                else:
                    introDoctor.show()
                    pyray.draw_text("You need more apples",600,500,80,pyray.RED)