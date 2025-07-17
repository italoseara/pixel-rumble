from engine import Component


class GunController(Component):
    def __init__(self, automatic: bool = False, fire_rate: float = 0.5, damage: int = 10,
                 bullet_speed: float = 500, bullet_lifetime: float = 2, bullet_size: tuple[int, int] = (10, 10)) -> None:
    
        super().__init__()
        self.automatic = automatic
        self.fire_rate = fire_rate
        self.damage = damage
        self.bullet_speed = bullet_speed
        self.bullet_lifetime = bullet_lifetime
        self.bullet_size = bullet_size