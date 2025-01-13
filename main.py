import arcade
from Include.views.GameView import GameView
from Include.classes.GameConfig import GameConfig


def main():
    window = arcade.Window(GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT, GameConfig.SCREEN_TITLE)
    start_view = GameView()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()