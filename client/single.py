import asyncio
import pygame
from pygame import Vector2 as Vector

from engine import Engine
from engine.settings import *
from renderer import Renderer
from renderer.settings import *

FPS = 60

async def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('GunGame Single')

    clock = pygame.time.Clock()
    engine = Engine()
    renderer = Renderer(screen)

    engine.add_player(1, (WORLD_WIDTH/2, WORLD_HEIGHT/2))

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    engine.shoot_player(1, event.pos[0], event.pos[1])

        keys = pygame.key.get_pressed()
        
        dx = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        dy = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        engine.move_player(1, dx, dy)

        engine.update(dt)
        renderer.render(engine)

        await asyncio.sleep(0)

    pygame.quit()

if __name__ == '__main__':
    asyncio.run(main())