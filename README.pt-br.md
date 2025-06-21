# Pixel Rumble

Um jogo de plataforma 2D construído com um motor de jogo customizado em Pygame. Este motor oferece uma arquitetura flexível e modular para criar jogos com Pygame, incluindo componentes para física, renderização, UI e mais.

> Click [here](README.md) for the English version.

# Visão Geral da Engine

## Funcionalidades

- **Arquitetura inspirada no Unity**: Design baseado em componentes, permitindo criação modular de objetos de jogo
- **Baseado em componentes**: Construa objetos de jogo anexando vários componentes
- **Sistema de física**: RigidBody, colisões e simulação física básica
- **Renderização**: Renderização de sprites com suporte a transformações
- **Sistema de UI**: Texto, botões e campos de entrada
- **Gerenciamento de cenas**: Organize seu jogo em diferentes cenas
- **Sistema de câmera**: Segue objetos, movimento suave da câmera

## Instalação

### Requisitos

- Python 3.12+
- Pygame 2.0+

### Configuração

1. Clone este repositório
2. Instale as dependências:

```
pip install pygame
```

## Início Rápido

```python
import pygame as pg
from pygame.math import Vector2
from engine import *

# Crie uma cena simples
class MinhaCena(Scene):
    def start(self):
        # Crie um objeto jogador
        player = GameObject("Player")
        player.add_component(Transform(x=100, y=100))
        player.add_component(SpriteRenderer("assets/player.png"))
        self.add(player)

        # Adicione texto de UI
        ui = GameObject("UI")
        canvas = ui.add_component(Canvas())
        canvas.add(Text("Olá Mundo", x=10, y=10))
        self.add(ui)

# Inicie o jogo
def main():
    game = Game("Meu Jogo", width=800, height=600)
    game.push_scene(MinhaCena())
    game.run()

if __name__ == "__main__":
    main()
```

## Conceitos Principais

### Game

A classe `Game` gerencia o loop do jogo, transições de cena e inicialização. É um singleton que controla o estado geral do jogo.

```python
game = Game("Meu Jogo", width=800, height=600, fps=60)
game.push_scene(MinhaCena())
game.run()
```

### Scene

Cenas contêm objetos de jogo e gerenciam seu ciclo de vida. Você pode criar cenas diferentes para menus, fases, etc.

```python
class CenaJogo(Scene):
    def start(self):
        # Inicialize objetos da cena
        pass

    def pause(self):
        # Chamado quando a cena é pausada
        pass

    def resume(self):
        # Chamado quando a cena é retomada
        pass
```

### GameObject

GameObjects são contêineres de componentes e representam entidades no seu jogo.

```python
player = GameObject("Player")
player.add_component(Transform(x=100, y=100))
player.add_component(SpriteRenderer("assets/player.png"))
```

### Componentes

Componentes definem o comportamento e as propriedades dos objetos de jogo.

#### Componentes Principais

- **Transform**: Gerencia posição, rotação e escala
- **SpriteRenderer**: Renderiza imagens
- **BoxCollider**: Detecta colisões
- **RigidBody**: Implementa comportamentos físicos

#### Componentes de UI

- **Canvas**: Contêiner para componentes de UI
- **Text**: Exibe texto
- **Button**: Elemento de UI clicável
- **InputField**: Entrada de texto do usuário

## Sistema de Física

O motor inclui um sistema de física básico com gravidade, colisões e forças.

```python
# Crie um objeto com física
o = GameObject("ObjetoFisica")
o.add_component(Transform(x=0, y=0))
o.add_component(BoxCollider(width=32, height=32))
o.add_component(RigidBody(mass=1, drag=0.05, gravity=10))

# Aplique forças ao objeto
rigid_body = o.get_component(RigidBody)
rigid_body.add_force(Vector2(100, 0))  # Força contínua
rigid_body.add_impulse(Vector2(0, -500))  # Impulso instantâneo (pulo)
```

## Sistema de Câmera

A câmera controla o que é visível na tela e pode seguir objetos do jogo.

```python
# Faça a câmera seguir o jogador
self.camera.set_target(player, smooth=True, smooth_speed=5)
```

## Sistema de UI

Crie UI no jogo com o componente Canvas e elementos de UI.

```python
ui = GameObject("UI")
canvas = ui.add_component(Canvas())

# Adicione texto
text = canvas.add(Text("Score: 0", x=10, y=10))

# Atualize o texto
text.text = "Score: 100"
```

## Componentes Customizados

Crie comportamentos customizados estendendo a classe Component:

```python
class ControladorJogador(Component):
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

## Modo Debug

O motor inclui um modo debug que visualiza colisores, transformações e outros componentes:

```python
# Defina em constants.py
DEBUG_MODE = True
```
