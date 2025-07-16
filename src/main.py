from engine import Game
from game.scenes.lobby import LobbyScene
from game.scenes import MainMenu


def main() -> None:
    try:
        game = Game(title="Pixel Rumble - Demo", icon="assets/img/logo.png")
        game.push_scene(LobbyScene())
        game.run()
    except KeyboardInterrupt:
        game.quit()


if __name__ == "__main__":
    main()
