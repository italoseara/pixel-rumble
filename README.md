# Pixel Rumble

A 2d platformer game built using a custom Pygame game engine. This engine provides a flexible and modular architecture for creating games with Pygame, featuring components for physics, rendering, UI, and more.

> Clique [aqui](README.pt-br.md) para a versão em Português.

# Engine Overview

## Features

- **Unity-like architecture**: Inspired by Unity's component-based design, allowing for modular game object creation
- **Component-based**: Build game objects by attaching various components
- **Physics system**: RigidBody, collisions, and basic physics simulation
- **Rendering**: Sprite rendering with transformation support
- **UI system**: Text, buttons, and input fields
- **Scene management**: Organize your game into different scenes
- **Camera system**: Follow objects, smooth camera movement

## Installation

### Requirements

- Python 3.12+
- Pygame 2.0+

### Setup

1. Clone this repository
2. Install dependencies:

```
pip install pygame
```

## Quick Start

```python
import pygame as pg
from pygame.math import Vector2
from engine import *

# Create a simple scene
class MyScene(Scene):
    def start(self):
        # Create a player object
        player = GameObject("Player")
        player.add_component(Transform(x=100, y=100))
        player.add_component(SpriteRenderer("assets/player.png"))
        self.add(player)

        # Add UI text
        ui = GameObject("UI")
        canvas = ui.add_component(Canvas())
        canvas.add(Text("Hello World", x=10, y=10))
        self.add(ui)

# Start the game
def main():
    game = Game("My Game", width=800, height=600)
    game.push_scene(MyScene())
    game.run()

if __name__ == "__main__":
    main()
```

## Core Concepts

### Game

The `Game` class manages the game loop, scene transitions, and initialization. It's a singleton that manages the overall game state.

```python
game = Game("My Game", width=800, height=600, fps=60)
game.push_scene(MyScene())
game.run()
```

### Scene

Scenes contain game objects and manage their lifecycle. You can create different scenes for menus, levels, etc.

```python
class GameplayScene(Scene):
    def start(self):
        # Initialize scene objects
        pass

    def pause(self):
        # Called when scene is paused
        pass

    def resume(self):
        # Called when scene is resumed
        pass
```

### GameObject

GameObjects are containers for components and represent entities in your game.

```python
player = GameObject("Player")
player.add_component(Transform(x=100, y=100))
player.add_component(SpriteRenderer("assets/player.png"))
```

### Components

Components define the behavior and properties of game objects.

#### Core Components

- **Transform**: Handles position, rotation, and scale
- **SpriteRenderer**: Renders images
- **BoxCollider**: Handles collision detection
- **RigidBody**: Implements physics behaviors

#### UI Components

- **Canvas**: Container for UI components
- **Text**: Displays text
- **Button**: Clickable UI element
- **InputField**: User text input

## Physics System

The engine includes a basic physics system with gravity, collisions, and forces.

```python
# Create a physics-enabled object
obj = GameObject("PhysicsObject")
obj.add_component(Transform(x=0, y=0))
obj.add_component(BoxCollider(width=32, height=32))
obj.add_component(RigidBody(mass=1, drag=0.05, gravity=10))

# Apply forces to the object
rigid_body = obj.get_component(RigidBody)
rigid_body.add_force(Vector2(100, 0))  # Apply continuous force
rigid_body.add_impulse(Vector2(0, -500))  # Apply instant impulse (jump)
```

## Camera System

The camera controls what's visible on the screen and can track game objects.

```python
# Make camera follow a player object
self.camera.set_target(player, smooth=True, smooth_speed=5)
```

## UI System

Create in-game UI with the Canvas component and UI elements.

```python
ui = GameObject("UI")
canvas = ui.add_component(Canvas())

# Add text
text = canvas.add(Text("Score: 0", x=10, y=10))

# Update text
text.text = "Score: 100"
```

## Custom Components

Create custom behaviors by extending the Component class:

```python
class PlayerController(Component):
    def __init__(self, move_speed=5):
        super().__init__()
        self.move_speed = move_speed

    def update(self, dt):
        keys = pg.key.get_pressed()
        transform = self.parent.get_component(Transform)

        if keys[pg.K_LEFT]:
            transform.x -= self.move_speed * dt
        if keys[pg.K_RIGHT]:
            transform.x += self.move_speed * dt
```

## Debug Mode

The engine includes a debug mode that visualizes colliders, transforms, and other components:

```python
# Set in constants.py
DEBUG_MODE = True
```
