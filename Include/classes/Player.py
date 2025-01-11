import arcade

class Player(arcade.Sprite):
    def __init__(self, filename, spriteScaling):
        super().__init__(filename, spriteScaling)
        self.center_x = 0
        self.center_y = 0
        self.vida = 10

    def quitarVida(self):
        self.vida -= 1

    def tieneVida(self):
        return self.vida != 0