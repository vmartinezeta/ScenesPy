import random
import arcade
import math
import os
from Include.classes.Bacteria import Bacteria
from Include.classes.Player import Player
from Include.classes.Roca import Roca


SPRITE_SCALING = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Exterminar bacterias"


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
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
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

        self.gameOver = False
        self.allSpriteList = None
        self.bacteriaList = None
        self.roca = None
        self.score = 0
        self.player = None

    def setup(self):
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        self.allSpriteList = arcade.SpriteList()
        self.bacteriaList = arcade.SpriteList()

        self.score = 0
        self.player = Player(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                           SPRITE_SCALING)
        self.player.center_x = 50
        self.player.center_y = 70

        self.allSpriteList.append(self.player)

        self.crearBacterias(50)

        self.window.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.BLACK)

    def crearBacterias(self, cantidad):
        for i in range(cantidad):
            hembra = bool(random.randint(0,1))
            filename = ":resources:images/enemies/bee.png"
            if not hembra :
                filename = ":resources:images/enemies/frog.png"
            bacteria = Bacteria(filename, SPRITE_SCALING / 3, hembra)

            bacteria.circle_center_x = random.randrange(SCREEN_WIDTH)
            bacteria.circle_center_y = random.randrange(SCREEN_HEIGHT)
            bacteria.circle_radius = random.randrange(100, 200)
            bacteria.circle_angle = random.random() * 2 * math.pi

            self.allSpriteList.append(bacteria)
            self.bacteriaList.append(bacteria)

    def on_draw(self):

        self.clear()

        self.allSpriteList.draw()

        output = "vida: " + str(self.player.vida)
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        self.player.center_x = x
        self.player.center_y = y

    def on_mouse_press(self, x, y, _button, _modifiers):
        self.roca = Roca(":resources:images/items/coinSilver.png", SPRITE_SCALING / 3)
        self.roca.center_x = x
        self.roca.center_y = y
        self.allSpriteList.append(self.roca)

    def on_update(self, delta_time):
        self.allSpriteList.update()

        machos = []
        for bacteria in self.bacteriaList:
            if not bacteria.hembra:
                machos.append(bacteria)

        hembras = arcade.SpriteList()
        for bacteria in self.bacteriaList:
            if bacteria.hembra:
                hembras.append(bacteria)

        for macho in machos:
            hitHembraList = arcade.check_for_collision_with_list(macho, hembras)
            for hembra in hitHembraList:
                self.crearBacterias(5)
                hembra.remove_from_sprite_lists()

        hitList = arcade.check_for_collision_with_list(self.player, self.bacteriaList)
        for bacteria in hitList:
            if (self.player.tieneVida()):
                self.player.quitarVida()
                bacteria.remove_from_sprite_lists()

        if isinstance(self.roca, Roca):
            hitBacteriaList = arcade.check_for_collision_with_list(self.roca, self.bacteriaList)
            for bacteria in hitBacteriaList:
                bacteria.remove_from_sprite_lists()
        
        if isinstance(self.roca, Roca) and self.roca.estaFuera:
            self.roca = None

        if not self.gameOver and (not self.player.tieneVida() or len(self.bacteriaList)==0 ):
            self.gameOver = True
            self.window.set_mouse_visible(True)
            descripcion = "Fallaste - Click para reiniciar"
            if self.player.tieneVida() and len(self.bacteriaList)==0:
                descripcion = "Ganaste - Click para reiniciar"
            game_over = GameOverView(descripcion)
            self.window.show_view(game_over)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = GameView()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()