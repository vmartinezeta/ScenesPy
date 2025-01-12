import arcade

class Player(arcade.Sprite):
    def __init__(self, filename, spriteScaling):
        super().__init__(filename, spriteScaling)
        self.center_x = 0
        self.center_y = 0
        self.vida = 10
        self.dx = 6
        self.dy = 6

    def top(self):
        if self.dy < 0 :
            self.dy = -1*self.dy

    def right(self):
        if self.dx< 0:
            self.dx =-1*self.dx

    def bottom(self):
        if self.dy>0:
            self.dy = -1*self.dy
    
    def left(self):
        if self.dx>0:
            self.dx=-1*self.dx

    def quitarVida(self):
        self.vida -= 1

    def tieneVida(self):
        return self.vida != 0