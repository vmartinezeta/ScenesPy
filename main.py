import random
import arcade
import math
import os
from Include.classes.Coin import Coin


SPRITE_SCALING = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Collect Coins Moving in Circles Example"


class GameOverView(arcade.View):

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Game Over - Click to restart",
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
        self.coinList = None
        self.score = 0
        self.playerSprite = None

    def setup(self):
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        self.allSpriteList = arcade.SpriteList()
        self.coinList = arcade.SpriteList()

        self.score = 0
        self.playerSprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                           SPRITE_SCALING)
        self.playerSprite.center_x = 50
        self.playerSprite.center_y = 70

        self.allSpriteList.append(self.playerSprite)

        for i in range(50):
            coin = Coin(":resources:images/items/coinGold.png", SPRITE_SCALING / 3)

            coin.circle_center_x = random.randrange(SCREEN_WIDTH)
            coin.circle_center_y = random.randrange(SCREEN_HEIGHT)

            coin.circle_radius = random.randrange(10, 200)

            coin.circle_angle = random.random() * 2 * math.pi

            self.coinList.append(coin)
            self.allSpriteList.append(coin)

        self.window.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):

        self.clear()

        self.allSpriteList.draw()

        output = "Score: " + str(self.score)
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

        if self.gameOver:
            arcade.draw_text("Game over", 400, 300, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        self.playerSprite.center_x = x
        self.playerSprite.center_y = y

    def on_update(self, delta_time):
        self.coinList.update()

        hit_list = arcade.check_for_collision_with_list(self.playerSprite, self.coinList)

        for coin in hit_list:
            self.score += 1
            coin.remove_from_sprite_lists()

        if not self.gameOver and len(self.coinList)==0:
            self.gameOver = True
            
            self.window.set_mouse_visible(True)
            game_over = GameOverView()
            self.window.show_view(game_over)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = GameView()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()