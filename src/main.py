from engine import Game
from game.scenes import MainMenu


def main() -> None:
    game = Game(title="Pixel Rumble - Demo", icon="assets/img/logo.png")
    game.push_scene(MainMenu())
    # game.push_scene(Scene2())
    game.run()


if __name__ == "__main__":
    main()
