from engine import GameObject, Transform, SpriteRenderer


class GunPrefab(GameObject):
    def __init__(self, player: GameObject, gun_type: str) -> None:
        super().__init__(f"{player.name}'s Gun ({gun_type})", player)

        self.player = player
        self.gun_type = gun_type

        # Add components for the gun
        self.add_component(Transform(y=-20, scale=2, z_index=2))
        self.add_component(SpriteRenderer(f"assets/img/guns/{gun_type}.png"))
