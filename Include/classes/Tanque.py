import arcade

class Tanque(arcade.Sprite):
    def __init__(self, filename, sprite_scaling, x, y):
        super().__init__(filename, sprite_scaling)        
        self.center_x = x
        self.center_y = y
        self.tiempo = 0
        self.capacidad = 1

    def debeEliminarse(self):
        return self.tiempo > 600

    def eliminar(self):
        self.kill()

    def update(self):
        self.tiempo += 1