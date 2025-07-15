from engine import Game
from game.scenes.lobby import LobbyScene


def main() -> None:
    game = Game(title="Pixel Rumble - Demo", icon="assets/img/logo.png")
    game.push_scene(LobbyScene())
    game.run()


if __name__ == "__main__":
    main()
