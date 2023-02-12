import pyray
from sprite import Sprite, Timer, DrawMode

INPUTS = ["READY"]
PHONE_BACKGROUN = "background.png"


def main(screen_size, inp): # Game stuff here
    music = pyray.load_music_stream("PythonGame/Assets/home_screen.wav")

    pyray.play_music_stream(music)

    # Init the sprite, Framerate, File location, Position, number of frames
    background = pyray.load_texture("PythonGame/Assets/background.png")
    qr = Sprite(5, "PythonGame/Assets/linkQR.png", [screen_size[0]*0.5,screen_size[1]*0.8],1)
    qr.show()
    qr.set_pos_center([screen_size[0]*0.5,screen_size[1]*0.65])
    bg = Sprite(5, "PythonGame/Assets/pinwheel_bg.png", [screen_size[0]*0.7,screen_size[1]*0.7],1)
    bg.scale = 5
    bg.offset = (bg.size[0]*bg.scale)*0.5,(bg.size[1]*bg.scale)*0.5
    
    # Add all sprites to array for easy updating
    sprites = [bg,qr]

    # Main game loop
    while not pyray.window_should_close():
        pyray.update_music_stream(music)
        # Time in s since last frame
        delta = pyray.get_frame_time()

        # This stuff happens while drawing
        with DrawMode():

            bg.rotation += 0.5
            bg.show()
            # Ignore this
            pyray.clear_background(pyray.BLACK)
            source = pyray.Rectangle(0, 0, screen_size[0], -screen_size[1])
            pyray.draw_texture_pro(background, source, pyray.Rectangle(0, 0, *screen_size), (0,0), 0, pyray.WHITE)

            [x.draw() for x in sprites]


            ## GET NETWORK STUFF
            # Up
            peeps = inp.get_inputs_1per()
            if "READY" in peeps:
                a = peeps["READY"]
            else:
                a = 0
            print(peeps)
            pyray.draw_text(f"{a} People connected!",600,300,80,pyray.BLACK)
            pyray.draw_text(f"http://34.142.66.132/",580,420,80,pyray.BLACK)
            
            # Return to next Game
            if pyray.is_key_down(pyray.KeyboardKey.KEY_SPACE):
                pyray.stop_music_stream(music)
                return False


            # Each frame, Render and update each sprite and timers
            [x.animate(delta) for x in sprites]