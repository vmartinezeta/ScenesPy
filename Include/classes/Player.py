import arcade
from Include.classes.GameConfig import GameConfig
from Include.classes.Tanque import Tanque
import random


class Player(arcade.Sprite):
    def __init__(self, filename, spriteScaling):
        super().__init__(filename, spriteScaling)
        self.center_x = 0
        self.center_y = 0
        self.vida = 10
        self.dx = 6
        self.dy = 6
        self.tanque = None
        self.capacidad = 5
        self.emitter = None
        self.emitter_timeout = 0
        self.tiempo = 0

    def emitterVeneno(self, x, y):
        return arcade.Emitter(
            center_xy=(x,y),
            emit_controller=arcade.EmitterIntervalWithTime(GameConfig.DEFAULT_EMIT_INTERVAL, GameConfig.DEFAULT_EMIT_DURATION),
            particle_factory=lambda emitter: arcade.LifetimeParticle(
                filename_or_texture=GameConfig.TEXTURE,
                change_xy=arcade.rand_in_circle((0.0, 0.0), GameConfig.PARTICLE_SPEED_FAST),
                lifetime=1.0,
                scale=GameConfig.DEFAULT_SCALE,
                alpha=GameConfig.DEFAULT_ALPHA
            )
        )

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

    def estaVacioTanque(self):
        return self.capacidad == 0

    def vaciarTanque(self):
        if self.estaVacioTanque(): return
        self.capacidad -= 1
        self.emitter = self.emitterVeneno(self.center_x, self.center_y)

    def llenarTanque(self):
        self.capacidad = 5

    def quitarTanque(self):
        self.tanque.eliminar()
        self.tanque = None

    def morir(self):
        if not self.tieneVida(): return
        self.vida -= 1

    def iniciarTemporizador(self):
        self.tiempo = 0

    def debeLlenarTanque(self):
        return self.tiempo > 1000    

    def update(self):
        self.tiempo += 1

        if not self.tanque and self.debeLlenarTanque():
            x = random.randrange(GameConfig.SCREEN_WIDTH)
            y = random.randrange(GameConfig.SCREEN_HEIGHT)
            self.tanque = Tanque(GameConfig.SPRITE_TANQUE, GameConfig.SPRITE_SCALING, x, y)

        if self.tanque:
            self.tanque.update()
            if self.tanque.debeEliminarse():
                self.quitarTanque()
                self.iniciarTemporizador()

        if self.tanque and self.tanque.collides_with_sprite(self):
            self.quitarTanque()
            self.llenarTanque()
            self.iniciarTemporizador()

        if self.emitter:
            self.emitter_timeout += 1
            if  self.emitter.can_reap() or self.emitter_timeout > GameConfig.EMITTER_TIMEOUT:
                self.emitter = None
                self.emitter_timeout = 0

    def tieneVida(self):
        return self.vida > 0