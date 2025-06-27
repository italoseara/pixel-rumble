# Engine Documentation

This document describes the main classes, arguments, and usage examples for the Pixel Rumble game engine. The engine is built on top of Pygame and provides a component-based architecture for 2D games.

---

## Table of Contents

- [Game](#game)
- [Scene](#scene)
- [GameObject](#gameobject)
- [Camera](#camera)
- [Component System](#component-system)
  - [Component (Base)](#component)
  - [Transform](#transform)
  - [RigidBody](#rigidbody)
  - [SpriteRenderer](#spriterenderer)
  - [BoxCollider](#boxcollider)
  - [Canvas](#canvas)
- [UI System](#ui-system)
  - [UIComponent (Base)](#uicomponent)
  - [Text](#text)
  - [Button](#button)
- [SpriteSheet](#spritesheet)
- [Example Usage](#example-usage)

---

## Game

**Class:** `Game`

Initializes the main game window and manages the game loop and scenes.

**Constructor Arguments:**

- `title` (str): The title of the game window.
- `width` (int, optional): Window width. Default: 800.
- `height` (int, optional): Window height. Default: 600.
- `fps` (int, optional): Frames per second. Default: 60.
- `icon` (str, optional): Path to window icon. Default: None.

**Example:**

```python
# Initialize and run the game
if __name__ == "__main__":
    game = Game(title="Pixel Rumble", width=800, height=600)
    game.push_scene(MyScene())
    game.run()
```

---

## Scene

**Class:** `Scene`

A container for game objects and logic. Handles camera, background, and scene transitions.

**Key Methods:**

- `add(game_object)`: Add a `GameObject` to the scene.
- `start()`: Called when the scene is pushed.
- `pause()`: Called when another scene is pushed over this one.
- `resume()`: Called when this scene becomes topmost again.

**Example:**

```python
class MyScene(Scene):
    def start(self):
        player = GameObject("Player")
        player.add_component(Transform(position=(100, 100)))
        self.add(player)
```

---

## GameObject

**Class:** `GameObject`

Represents an entity in the game world. Can have components attached.

**Constructor Arguments:**

- `name` (str): Unique name for the object.
- `parent` (GameObject, optional): Parent object. Default: None.

**Key Methods:**

- `find(name)`: Find a GameObject by name.

**Example:**

```python
player = GameObject("Player")
player.add_component(Transform(position=(100, 100)))
player.add_component(SpriteRenderer(path="assets/img/players.png"))
```

---

## Camera

**Class:** `Camera`

Handles the viewport and can follow a target GameObject.

**Constructor Arguments:**

- `x` (float, optional): Initial X position. Default: 0.
- `y` (float, optional): Initial Y position. Default: 0.
- `width` (int, optional): Viewport width. Default: 800.
- `height` (int, optional): Viewport height. Default: 600.

**Key Methods:**

- `set_target(target, smooth=False, smooth_speed=10, offset=(0,0))`: Follow a GameObject.
- `update(dt)`: Update camera position.

**Example:**

```python
camera = Camera(x=0, y=0, width=800, height=600)
camera.set_target(player)
```

---

## Component System

### Component

**Class:** `Component`

Base class for all components. Attach to GameObjects to add behavior.

**Key Methods:**

- `start()`: Called when added to a GameObject.
- `update(dt)`: Called every frame.
- `draw(surface)`: Render visuals.
- `handle_event(event)`: Handle input events.
- `destroy()`: Called when removed.

**Example:**

```python
class CustomComponent(Component):
    def update(self, dt):
        print("Updating!")
player.add_component(CustomComponent())
```

### Transform

**Class:** `Transform(Component)`

Handles position, rotation, and scale.

**Constructor Arguments:**

- `position` (Vector2 or tuple, optional): Position. Default: (0,0).
- `rotation` (float, optional): Rotation in degrees. Default: 0.0.
- `scale` (Vector2 or float, optional): Scale. Default: 1.
- `x` (float, optional): X position. Default: 0.0.
- `y` (float, optional): Y position. Default: 0.0.

**Example:**

```python
player.add_component(Transform(position=(100, 100), rotation=0, scale=1))
```

### RigidBody

**Class:** `RigidBody(Component)`

Adds physics properties.

**Constructor Arguments:**

- `mass` (float, optional): Mass. Default: 1.
- `drag` (float, optional): Drag. Default: 0.05.
- `gravity` (float, optional): Gravity. Default: 10.0.

**Example:**

```python
player.add_component(RigidBody(mass=2, drag=0.1, gravity=9.8))
```

### SpriteRenderer

**Class:** `SpriteRenderer(Component)`

Renders a sprite or animation.

**Constructor Arguments:**

- `path` (str): Path to image or sprite sheet.
- `color` (pg.Color, optional): Color filter. Default: white.
- `flip_x` (bool, optional): Flip horizontally. Default: False.
- `flip_y` (bool, optional): Flip vertically. Default: False.
- `pivot` (Vector2/tuple/str, optional): Pivot point. Default: (0.5,0.5).
- `grid_size` (tuple, optional): Sprite grid size.
- `sprite_index` (tuple, optional): Sprite index.
- `animation_frames` (list, optional): Animation frames.
- `animation_duration` (float, optional): Animation duration.
- `loop` (bool, optional): Loop animation. Default: True.

**Example:**

```python
player.add_component(SpriteRenderer(path="assets/img/players.png", flip_x=True))
```

### BoxCollider

**Class:** `BoxCollider(Component)`

Adds a rectangular collider for physics and collisions.

**Constructor Arguments:**

- `width` (float, optional): Collider width.
- `height` (float, optional): Collider height.
- `offset` (Vector2/tuple, optional): Offset from GameObject position.

**Example:**

```python
player.add_component(BoxCollider(width=32, height=32))
```

### Canvas

**Class:** `Canvas(Component)`

Container for UI components. Handles their update, events, and drawing.

**Key Methods:**

- `add(component)`: Add a UI component.

**Example:**

```python
canvas = Canvas()
canvas.add(Text(text="Hello!", x=100, y=50))
player.add_component(canvas)
```

---

## UI System

### UIComponent

**Class:** `UIComponent`

Base class for UI elements. Handles position, size, and pivot.

**Constructor Arguments:**

- `x` (int/str, optional): X position or percentage. Default: 0.
- `y` (int/str, optional): Y position or percentage. Default: 0.
- `width` (int, optional): Width. Default: 0.
- `height` (int, optional): Height. Default: 0.
- `pivot` (Vector2/tuple/str, optional): Pivot point. Default: (0,0).

### Text

**Class:** `Text(UIComponent)`

Displays text on the screen.

**Constructor Arguments:**

- `text` (str, optional): Text to display. Default: "".
- `x` (int, optional): X position. Default: 0.
- `y` (int, optional): Y position. Default: 0.
- `color` (pg.Color, optional): Text color. Default: white.
- `shadow` (bool, optional): Draw shadow. Default: True.
- `shadow_color` (pg.Color, optional): Shadow color. Default: black.
- `font_size` (int, optional): Font size. Default: 48.
- `pivot` (Vector2/tuple/str, optional): Pivot point. Default: (0,0).

**Example:**

```python
text = Text(text="Score: 0", x=20, y=20, color=(255,255,255))
```

### Button

**Class:** `Button(UIComponent)`

A clickable button UI element.

**Constructor Arguments:**

- `text` (str, optional): Button text. Default: "Button".
- `x` (int/str, optional): X position or percentage. Default: 0.
- `y` (int/str, optional): Y position or percentage. Default: 0.
- `size` ("sm"|"md"|"lg", optional): Button size. Default: "md".
- `disabled` (bool, optional): Disabled state. Default: False.
- `on_click` (Callable, optional): Function to call on click. Default: None.
- `pivot` (Vector2/tuple/str, optional): Pivot point. Default: (0.5,0.5).

**Example:**

```python
button = Button(text="Play", x="50%", y="80%", size="lg", on_click=start_game)
```

---

## SpriteSheet

**Class:** `SpriteSheet`

Handles loading and slicing sprite sheets.

**Constructor Arguments:**

- `filename` (str): Path to the sprite sheet image.
- `size` (tuple, optional): Size of each sprite.
- `spacing` (tuple, optional): Spacing between sprites. Default: (0,0).
- `scale` (int, optional): Scale factor. Default: 1.

**Key Methods:**

- `get_sprite(index, colorkey=None)`: Get a sprite by index.

**Example:**

```python
sheet = SpriteSheet(filename="assets/img/players.png", size=(32,32))
sprite = sheet.get_sprite((0,0))
```

---

## Example Usage

```python
import pygame as pg
from engine.core.game import Game
from engine.core.scene import Scene
from engine.core.game_object import GameObject
from engine.core.components.transform import Transform
from engine.core.components.sprite_renderer import SpriteRenderer

# Create a custom scene
class MyScene(Scene):
    def start(self):
        player = GameObject("Player")
        player.add_component(Transform(position=(100, 100)))
        player.add_component(SpriteRenderer(path="assets/img/players.png"))
        self.add(player)

# Initialize and run the game
if __name__ == "__main__":
    game = Game(title="Pixel Rumble", width=800, height=600)
    game.push_scene(MyScene())
    game.run()
```

---

For more details, see the source code and docstrings in each class.
