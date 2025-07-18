from engine import GameObject, Transform, SpriteRenderer


class GunPrefab(GameObject):
    _gun_pivot: dict[str, tuple[float, float]] = {
        "pistol": (-0.5, 0.5),
        "awm": (0.1, 0.5),
        "uzi": (-0.5, 0.5),
    }
    
    def __init__(self, player: GameObject, gun_type: str) -> None:
        super().__init__(f"{player.name}'s Gun", player)

        # Add components for the gun
        self.add_component(Transform(y=-20, scale=2, z_index=2))
        self.add_component(SpriteRenderer(
            f"assets/img/guns/{gun_type}.png", 
            pivot=self._gun_pivot.get(gun_type, (-0.5, 0.5))
        ))
