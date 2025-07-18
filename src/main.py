from engine import Game
from game.scenes.menu import MainMenu
from logger_config import setup_logger


def main() -> None:
    setup_logger()

    try:
        game = Game(title="Pixel Rumble - Demo", icon="assets/img/logo.png")
        game.push_scene(MainMenu())
        game.run()
    except KeyboardInterrupt:
        game.quit()


if __name__ == "__main__":
    main()
