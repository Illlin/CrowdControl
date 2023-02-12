import pyray
from sprite import Sprite, Timer
import Doctor_Deflector
import To_The_Moon
import menu
import test
import threading
import requests
import json
import time
import basic_pong
import germ_journey
import score
import random

password = "FishBiscuitsAreFish"

server_get = "http://34.142.66.132/get-buttons"
server_set = "http://34.142.66.132/"

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
            if self.data["users"][i] in buttons:
                buttons[self.data["users"][i]] += 1
            else:
                buttons[self.data["users"][i]] = 1
        return buttons

    def get_top(self):
        max = -1
        current = ""
        buts = self.get_inputs_1per()
        for i in buts:
            if buts[i] > max:
                max = buts[i]
                current = i
        return current

    def get_inputs_sum(self):
        return self.data["hits"]


def run():
    while True:
        a.update_inputs()
        time.sleep(0.1)


a = Inputs()


if __name__ == "__main__":
    c_score = 0
    getter = threading.Thread(target=run)
    getter.start()
    screen_size = [1920,1080]
    pyray.set_config_flags(
        pyray.ConfigFlags.FLAG_VSYNC_HINT | 
        pyray.ConfigFlags.FLAG_VSYNC_HINT )

    pyray.init_window(*screen_size, "CubeWorld")
    pyray.init_audio_device()
    a.set_inputs(menu.INPUTS, test.BUTTON_POS, menu.PHONE_BACKGROUN)
    menu.main(screen_size,a)
    while True:
        g = [1,2,3]
        random.shuffle(g)
        for b in g:
            if b == 1:
                a.set_inputs(To_The_Moon.INPUTS, test.BUTTON_POS, To_The_Moon.PHONE_BACKGROUN)
                won = To_The_Moon.main(screen_size,a)
            if b == 2:
                a.set_inputs(Doctor_Deflector.INPUTS, test.BUTTON_POS, Doctor_Deflector.PHONE_BACKGROUN)
                won= Doctor_Deflector.main(screen_size,a)
            if b == 3:
                a.set_inputs(germ_journey.INPUTS, test.BUTTON_POS, germ_journey.PHONE_BACKGROUN)
                won= germ_journey.main(screen_size,a)
            c_score += won
            score.main(screen_size,a,c_score, won)