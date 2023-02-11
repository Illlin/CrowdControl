import pyray
from sprite import Sprite, Timer
import Doctor_Deflector
import threading
import random
import requests
import json

password = "FishBiscuitsAreFish"

server_get = "127.0.0.1:5000/inputs"
server_set = "127.0.0.1:5000/set_inputs"

class Inputs:
    def __init__(self):
        self.inputs = {}

    def read(self):
        return self.inputs

    def set_inputs(self, names, positions):
        self.inputs = {}
        for x in names:
            self.inputs[x] = 0

        data_json = json.dumps(
            {
                "password":password,
                "options":names,
                "positions":positions
            }
        )
        payload = {'json_payload': data_json}
        r = requests.post("http://localhost:8080", data=payload)

        

    def press(self, name):
        if name in self.inputs:
            self.inputs[name] += 1

    def server_com():
        requests.get('https://github.com/inputs.json')
        

def set_inputs(names,layout):
    # Do something to set the inputs on the server end
    pass


def get_inputs():
    x = 4 # Number of buttons
    sum = [0]*x
    # Spoof inputs for now
    n = 100 # 100 people
    for i in range(100):
        random.randint()




if __name__ == "__main__":
    screen_size = [640,480]
    pyray.set_config_flags(
        pyray.ConfigFlags.FLAG_VSYNC_HINT | 
        pyray.ConfigFlags.FLAG_VSYNC_HINT )

    pyray.init_window(*screen_size, "CubeWorld")
    Doctor_Deflector.main(screen_size)