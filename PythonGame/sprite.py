import pyray
import numpy as np

class DrawMode():
    def __init__(self):
        pass

    def __enter__(self):
        pyray.begin_drawing()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pyray.end_drawing()


class Timer():
    def __init__(self, length, start = False):
        self.length = length
        self.current = length
        self.running = start

    def tick(self, delta):
        if self.running:
            self.current -= delta

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def done(self):
        return self.current <= 0

    def reset(self):
        self.current = self.length


class Sprite():
    def __init__(self, ani_speed, texture, position, frames):
        self.hidden = True
        self.ani_speed = ani_speed
        self.texture = texture
        self.position = position[::]
        self.floatPosition = [float(position[0]), float(position[1])]
        self.offset = (0,0)
        self.current_frame = 0
        self.max_frame = frames
        self.time = 0
        self.load_texture()
        self.goal = self.position[::]
        self.move_speed = 0
        self.at_goal = self.position == self.goal
        self.scale = 1
        self.rotation = 0
        self.tint = pyray.WHITE

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def load_texture(self):
        if type(self.texture) == str:
            self.texture = pyray.load_texture(self.texture)
        self.size = (self.texture.width/self.max_frame, self.texture.height)
        self.frameRec = pyray.Rectangle(0,0,self.size[0]*(self.current_frame+1), self.size[1])

    def set_frame(self, frame):
        self.current_frame = frame

    def animate(self, delta):
        self.at_goal = self.position == self.goal
        self.time += delta
        frames = self.time // (1/self.ani_speed)
        self.time = self.time % (1/self.ani_speed)
        self.next_frame(no=frames)

        if self.move_speed != 0:
            self.floatPosition = [float(self.position[0]), float(self.position[1])]
            dir = np.array(self.goal) - np.array(self.floatPosition)
            mag = np.sqrt(sum(i**2 for i in dir))
            if mag <= self.move_speed*delta:
                self.floatPosition = [float(self.goal[0]), float(self.goal[1])]
                self.position = self.goal
                return
            
            dir = dir / mag

            add = dir * self.move_speed*delta
            self.floatPosition = [x for x in add + self.floatPosition]
            self.position = [int(x) for x in add + self.floatPosition]

    def next_frame(self, no=1):
        self.current_frame = (self.current_frame + no) % self.max_frame
        self.frameRec.x = self.current_frame*self.size[0]

    def set_pos(self, pos):
        self.position = pos[::]

    def set_pos_center(self, pos):
        self.position = pos[0] - (self.size[0]*self.scale)/2, pos[1] - (self.size[1]*self.scale)/2

    def set_goal_center(self, pos):
        self.goal = pos[0] - (self.size[0]*self.scale)/2, pos[1] - (self.size[1]*self.scale)/2

    def draw(self):
        dest = self.get_rect()
        if not self.hidden:
            pyray.draw_texture_pro(
                self.texture,
                self.frameRec,
                dest,
                self.offset,
                self.rotation,
                self.tint
            )

    def get_rect(self):
        return pyray.Rectangle(*self.position,self.size[0]*self.scale, self.size[1]*self.scale)

    def get_collision(self, other):
        return pyray.check_collision_recs(self.get_rect(), other.get_rect())