import pyray
from sprite import Sprite, Timer, DrawMode

INPUTS = ["READY"]
PHONE_BACKGROUN = "background.png"


def main(screen_size, inp): # Game stuff here
    # Init the sprite, Framerate, File location, Position, number of frames
    background = pyray.load_texture("PythonGame/Assets/background.png")

    bg = Sprite(5, "PythonGame/Assets/pinwheel_bg.png", [screen_size[0]*0.7,screen_size[1]*0.7],1)
    bg.scale = 5
    bg.offset = (bg.size[0]*bg.scale)*0.5,(bg.size[1]*bg.scale)*0.5
    
    # Add all sprites to array for easy updating
    sprites = [bg]

    # Main game loop
    while not pyray.window_should_close():
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
            pyray.draw_text(f"{len(peeps)} People connected!",600,500,80,pyray.RED)
            
            # Return to next Game
            if pyray.is_key_down(pyray.KeyboardKey.KEY_SPACE):
                return False


            # Each frame, Render and update each sprite and timers
            [x.animate(delta) for x in sprites]