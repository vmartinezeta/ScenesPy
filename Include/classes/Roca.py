import arcade
import math

class Roca(arcade.Sprite):
    def __init__(self, filename, spriteScaling, dx, dy):
        super().__init__(filename, spriteScaling)
        self.circle_angle = 0
        self.circle_radius = 0
        self.circle_speed = 0.008
        self.circle_center_x = 0
        self.circle_center_y = 0        
        self.tiempo = 0
        self.estaFuera = False
        self.dx = dx
        self.dy = dy

    def update(self):
        self.tiempo = self.tiempo + 50
        if not self.estaFuera and self.tiempo >= 2000:
            self.estaFuera = True

        self.center_x += self.dx
        self.center_y += self.dy