import arcade
import random
import math
import os
import pyglet
from Include.classes.Bacteria import Bacteria
from Include.classes.Player import Player
from Include.classes.GameConfig import GameConfig
from Include.classes.Tanque import Tanque

class GameOverView(arcade.View):
    def __init__(self, descripcion):
        super().__init__()
        self.descripcion = descripcion

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            self.descripcion,
            GameConfig.SCREEN_WIDTH / 2,
            GameConfig.SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):        
        gameView = GameView()
        gameView.setup()
        self.window.show_view(gameView)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)        
        self.pause = False
        self.gameOver = False
        self.bacteriaList = None
        self.player = None
        self.fondoSound = None
        self.emitter = None
        self.emitter_timeout = 0
        self.tanque = None

    def setup(self):
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        self.gameOverSound = arcade.load_sound(GameConfig.SOUND_GAMEOVER)
        fondoSound = arcade.load_sound(GameConfig.SOUND_FONDO)    
        self.fondoSound = arcade.play_sound(fondoSound)

        self.bacteriaList = arcade.SpriteList()

        self.player = Player(GameConfig.SPRITE_PLAYER, GameConfig.SPRITE_SCALING)
        self.player.center_x = 50
        self.player.center_y = 70
        self.player.iniciarTemporizador()

        self.crearBacterias(30)

        self.window.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.BLACK)

    def crearBacterias(self, cantidad):
        for i in range(cantidad):
            hembra = bool(random.randint(0,1))
            filename = GameConfig.SPRITE_BACTERIA_HEMBRA
            if not hembra :
                filename = GameConfig.SPRITE_BACTERIA_MACHO
            bacteria = Bacteria(filename, GameConfig.SPRITE_SCALING / 3, hembra)

            bacteria.circle_center_x = random.randrange(GameConfig.SCREEN_WIDTH)
            bacteria.circle_center_y = random.randrange(GameConfig.SCREEN_HEIGHT)
            bacteria.circle_radius = random.randrange(100, 200)
            bacteria.circle_angle = random.random() * 2 * math.pi

            self.bacteriaList.append(bacteria)

    def on_draw(self):
        self.clear()

        if self.player.tanque:
            self.player.tanque.draw()

        if self.player.emitter:
            self.player.emitter.draw()

        self.player.draw()
        self.bacteriaList.draw()

        output = "vida: " + str(self.player.vida)
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
        if self.pause :
            arcade.draw_text("Pausado", GameConfig.SCREEN_WIDTH/2, GameConfig.SCREEN_HEIGHT/2, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.pause or self.gameOver: return
        self.player.center_x = x
        self.player.center_y = y

    def on_mouse_press(self, x, y, _button, _modifiers):
        if self.pause or self.gameOver: return
        self.player.vaciarTanque()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.S:
            self.player.bottom()
        elif symbol == arcade.key.W:
            self.player.top()
        elif symbol == arcade.key.A:
            self.player.left()
        elif symbol == arcade.key.D:
            self.player.right()
        elif symbol == arcade.key.SPACE:
            self.pause = not self.pause

    def on_update(self, delta_time):
        if self.pause or self.gameOver: return
        self.player.update()
        self.bacteriaList.update()


        if self.player.emitter:
            self.player.emitter.update()
            for bacteria in self.bacteriaList:
                hitParticleList = bacteria.collides_with_list(self.player.emitter._particles)
                for _ in hitParticleList:
                    bacteria.remove_from_sprite_lists()

        machos = filter(lambda bacteria:not bacteria.hembra, self.bacteriaList)

        hembras = arcade.SpriteList()
        for bacteria in self.bacteriaList:
            if bacteria.hembra:
                hembras.append(bacteria)

        for macho in machos:
            hitHembraList = macho.collides_with_list(hembras)
            for hembra in hitHembraList:
                macho.remove_from_sprite_lists()
                hembra.remove_from_sprite_lists()
                if len(self.bacteriaList) > 100:return
                self.crearBacterias(5)

        hitList = self.player.collides_with_list(self.bacteriaList)
        for bacteria in hitList:
            self.player.morir()
            bacteria.remove_from_sprite_lists()

        if not self.gameOver and (not self.player.tieneVida() or len(self.bacteriaList)==0 ):
            self.gameOver = True
            self.window.set_mouse_visible(True)
            self.finJuego()

    def finJuego(self):
        descripcion = "Fallaste - Click para reiniciar"
        if self.player.tieneVida() and len(self.bacteriaList)==0:
            descripcion = "Ganaste - Click para reiniciar"
        arcade.stop_sound(self.fondoSound)
        game_over = GameOverView(descripcion)
        arcade.play_sound(self.gameOverSound)
        self.window.show_view(game_over)