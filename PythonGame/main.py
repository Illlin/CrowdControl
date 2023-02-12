import pyray
from sprite import Sprite, Timer
import Doctor_Deflector
import test
import threading
import requests
import json
import time

password = "FishBiscuitsAreFish"

server_get = "http://www.localhost:5000/get-buttons"
server_set = "http://www.localhost:5000/"

class Inputs:
    def __init__(self):
        self.inputs = {}

    def read(self):
        return self.inputs

    def set_inputs(self, names, positions,background):
        self.inputs = {}
        for x in names:
            self.inputs[x] = 0

        data = {
            "names":names,
            "positions":positions,
            "password":password,
            "background":background
        }
    
        header = {"Content-Type": "application/json"}
        r = requests.post(server_set, json = data, headers=header)

        

    def press(self, name):
        if name in self.inputs:
            self.inputs[name] += 1

    def update_inputs(self):
        resp = requests.get(url=server_get)
        self.data = resp.json()

    def get_inputs_1per(self):
        buttons = {}
        for i in self.data["users"]:
            print(self.data["users"][i])
            if self.data["users"][i] in buttons:
                buttons[self.data["users"][i]] += 1
            else:
                buttons[self.data["users"][i]] = 1
        return buttons

    def get_top(self):
        max = -1
        current = ""
        buts = self.get_inputs_1per()
        print(buts)
        for i in buts:
            if buts[i] > max:
                max = buts[i]
                current = i
        print(current)
        return current

    def get_inputs_sum(self):
        return self.data["hits"]


def run():
    while True:
        a.update_inputs()
        print(a.get_inputs_sum())
        time.sleep(0.1)


a = Inputs()


if __name__ == "__main__":
    getter = threading.Thread(target=run)
    getter.start()
    screen_size = [1920,1080]
    pyray.set_config_flags(
        pyray.ConfigFlags.FLAG_VSYNC_HINT | 
        pyray.ConfigFlags.FLAG_VSYNC_HINT )

    pyray.init_window(*screen_size, "CubeWorld")
    Doctor_Deflector.main(screen_size)
    a.set_inputs(test.INPUTS, test.BUTTON_POS,test.PHONE_BACKGROUN)
    test.main(screen_size, a)

