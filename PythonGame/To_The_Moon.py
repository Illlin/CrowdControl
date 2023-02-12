import pyray
from sprite import Sprite, Timer, DrawMode
import math
import time

INPUTS = ["BUY", "SELL"]
PHONE_BACKGROUN = "background.png"


def main(screen_size, inp): # Game stuff here
    music = pyray.load_music_stream("PythonGame/Assets/transition.wav")
    music.looping = False

    pyray.play_music_stream(music)

    # Init the sprite, Framerate, File location, Position, number of frames
    background = pyray.load_texture("PythonGame/Assets/to_the_moon_bg.png")


    text = Sprite(1, "PythonGame/Assets/to_the_moon_title.png", [0,0], 1)
    text.scale = 0.70
    text.offset = (text.size[0]*text.scale)*0.5,(text.size[1]*text.scale)*1
    text.set_pos_center([screen_size[0]*0.9,1100])
    text.rotation = -120

    stonks = Sprite(5, "PythonGame/Assets/stonks.png", [0,0],1)
    cover = Sprite(5, "PythonGame/Assets/blue_rectangle.png", [220,-97],1)
    cover.move_speed = 95
    moon_body = Sprite(5, "PythonGame/Assets/Moon_body.png", [600,600],2)
    moon_head = Sprite(5, "PythonGame/Assets/Moon_head.png", [840,630],2)
    moon_head.offset = (moon_head.size[0]*moon_head.scale)*0.5,(moon_head.size[1]*moon_head.scale)*0.8
    # Add all sprites to array for easy updating
    sprites = [stonks, cover, moon_body, moon_head, text]
    
    # Timers are used instead of sleep
    # Control Timers
    intro_timer = Timer(4)
    moon_timer = Timer(3.5)
    main_timer = Timer(10)
    end_timer = Timer(1)

    # Game Timers
    t1, t2, t3, t4, t5 = Timer(1.8), Timer(3.3), Timer(5.4), Timer(7.3), Timer(9.9)
    timers = [intro_timer, main_timer, end_timer, t1, t2, t3, t4, t5, moon_timer]

    # Start the main game timer
    intro_timer.start()
    moon_timer.start()

    # Load background

    # Main game loop
    while not pyray.window_should_close():
        moon_head.rotation = 30*math.sin(time.time()*3)
        # Time in s since last frame
        delta = pyray.get_frame_time()

        # This stuff happens while drawing
        with DrawMode():
            pyray.update_music_stream(music)
            # Ignore this
            pyray.clear_background(pyray.BLACK)
            source = pyray.Rectangle(0, 0, 1036, -1036)
            pyray.draw_texture_pro(background, source, pyray.Rectangle(0, 0, *screen_size), (0,0), 0, pyray.WHITE)

            # Draw the intro stuff
            if intro_timer.running:
                for sprite in sprites:
                    sprite.hide()
                moon_head.show()
                moon_body.show()
                text.show()
                text.rotation += 1.2

            if moon_timer.done() and moon_timer.running:
                moon_body.goal = [1300,600]
                moon_head.goal = [1540,630]
                moon_body.move_speed = 400
                moon_head.move_speed = moon_body.move_speed
                moon_timer.stop()
                moon_timer.reset()

            
            # Start the game
            if intro_timer.done() and intro_timer.running:
                music = pyray.load_music_stream("PythonGame/Assets/Funky_time.wav")
                background = pyray.load_texture("PythonGame/Assets/blue_rectangle.png")
                music.looping = False

                pyray.play_music_stream(music)
                # Set Sprite peramiters
                intro_timer.stop()
                main_timer.start()
                win = True
                t1.start()
                t2.start()
                t3.start()
                t4.start()
                t5.start()
                for sprite in sprites:
                    sprite.show()
                text.hide()
                cover.goal = [10000, -97]
                buy = None

            # Main game stuff here
            if main_timer.running:
                if inp.get_top() == "BUY" or pyray.is_key_pressed(pyray.KeyboardKey.KEY_DOWN):
                    buy = False
                elif inp.get_top() == "SELL" or pyray.is_key_pressed(pyray.KeyboardKey.KEY_UP):
                    buy = True
                
                if t1.running and t1.done():
                    print("1")
                    if buy: # Possibly show result of each section? Like "BUY" if majority buy
                        win = False
                    t1.stop()
                    t2.start()

                if t2.running and t2.done():
                    print("2")
                    if not buy:
                        win = False
                    t2.stop()
                    t3.start()

                if t3.running and t3.done():
                    print("3")
                    if buy:
                        win = False
                    t3.stop()
                    t4.start()

                if t4.running and t4.done():
                    print("4")
                    if not buy:
                        win = False
                    t4.stop()
                    t5.start()

                if t5.running and t5.done():
                    print("5")
                    if buy:
                        win = False
                    t5.stop()


            [x.draw() for x in sprites]
            [x.animate(delta) for x in sprites]
            [x.tick(delta) for x in timers]

            if intro_timer.running:
                pyray.draw_text("Buy Red, Sell Green",540,900,80,pyray.WHITE)

            # Ending
            if main_timer.done():
                main_timer.stop()
                end_timer.start()
                for sprite in sprites:
                    sprite.hide
                
                if win:
                    pyray.draw_text("You won it",740,900,80,pyray.RED)
                else:
                    pyray.draw_text("To the moon! And back...",340,900,80,pyray.RED)
            
            # Return to next Game
            if end_timer.done():
                pyray.stop_music_stream(music)
                return win # return win or lose so music can play


            # Each frame, Render and update each sprite and timers

            