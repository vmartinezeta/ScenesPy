import arcade
import math

class Bacteria(arcade.Sprite):
    def __init__(self, filename, sprite_scaling, hembra):
        super().__init__(filename, sprite_scaling)
        self.circle_angle = 0
        self.circle_radius = 0
        self.circle_speed = 10/1000
        self.circle_center_x = 0
        self.circle_center_y = 0
        self.tiempo = 0
        self.hembra = hembra
        self.vida = 5

    def update(self):
        self.center_x = self.circle_radius * math.sin(self.circle_angle) \
            + self.circle_center_x
        self.center_y = self.circle_radius * math.cos(self.circle_angle) \
            + self.circle_center_y

        self.circle_angle += self.circle_speed