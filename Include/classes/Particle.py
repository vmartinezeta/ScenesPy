import arcade


class Particle(arcade.LifetimeParticle):
    def __init__(self,filename, change_xy, lifetime, center_xy, angle, change_angle, scale):
        super().__init__(filename, change_xy, lifetime, center_xy, angle, change_angle, scale)

    def update(self):
        print("works")