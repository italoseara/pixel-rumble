from engine import GameObject, Transform, SpriteRenderer, BoxCollider, RigidBody


class ItemPrefab(GameObject):
    def __init__(self, item_type: str) -> None:
        super().__init__(f"Item ({item_type})")

        # Add components for the item
        self.add_component(Transform(scale=2, z_index=2))
        self.add_component(SpriteRenderer(f"assets/img/guns/{item_type}.png"))
        self.add_component(RigidBody(mass=1.0, drag=0.5, is_kinematic=True))
        self.add_component(BoxCollider(width=15, height=15, is_trigger=True))