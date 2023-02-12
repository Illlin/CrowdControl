import pyray
from sprite import Sprite, Timer, DrawMode

INPUTS = ["BUY", "SELL"]


def main(screen_size, inp): # Game stuff here
    # Init the sprite, Framerate, File location, Position, number of frames
    background = pyray.load_texture("PythonGame/Assets/blue_rectangle.png")

    stonks = Sprite(5, "PythonGame/Assets/stonks.png", [0,0],1)
    cover = Sprite(5, "PythonGame/Assets/blue_rectangle.png", [220,-97],1)
    cover.move_speed = 150
    moon_man = Sprite(5, "PythonGame/Assets/moon_man.png", [0,0],2)
    # Add all sprites to array for easy updating
    sprites = [stonks, cover, moon_man]
    
    # Timers are used instead of sleep
    # Control Timers
    intro_timer = Timer(1)
    main_timer = Timer(10)
    end_timer = Timer(1)

    # Game Timers
    t1, t2, t3, t4, t5 = Timer(1.8), Timer(1.5), Timer(2), Timer(2), Timer(2.6)
    timers = [intro_timer, main_timer, end_timer, t1, t2, t3, t4, t5]

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
                pyray.draw_text("GOODBUY MOONMEN",10,10,80,pyray.RED)
            
            # Start the game
            if intro_timer.done() and intro_timer.running:
                # Set Sprite peramiters
                intro_timer.stop()
                main_timer.start()
                win = True
                t1.start()
                for sprite in sprites:
                    sprite.show()
                cover.goal = [10000, -97]
                buy = None

            # Main game stuff here
            if main_timer.running:
                if pyray.is_key_pressed(pyray.KeyboardKey.KEY_DOWN):
                    buy = False
                elif pyray.is_key_pressed(pyray.KeyboardKey.KEY_UP):
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


            # Ending
            if main_timer.done():
                main_timer.stop()
                end_timer.start()
                for sprite in sprites:
                    sprite.hide
                
                if win:
                    pyray.draw_text("You won it",10,10,80,pyray.RED)
                else:
                    pyray.draw_text("You loser.",10,10,80,pyray.RED)
            
            # Return to next Game
            if end_timer.done():
                return False # return win or lose so music can play


            # Each frame, Render and update each sprite and timers
            [x.draw() for x in sprites]
            [x.animate(delta) for x in sprites]
            [x.tick(delta) for x in timers]