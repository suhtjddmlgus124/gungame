import pygame
from engine import Engine
from .entity import PlayerRenderer, BulletRenderer, EnemyRenderer
from .settings import *

class Renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.player_renderer = PlayerRenderer(self.screen)
        self.bullet_renderer = BulletRenderer(self.screen)
        self.enemy_renderer = EnemyRenderer(self.screen)

    def render(self, engine: Engine):
        self.screen.fill('black')

        # 총알 렌더링
        for bullet in engine.bullets:
            self.bullet_renderer.render(bullet)
        # 적 렌더링
        for enemy in engine.enemies:
            self.enemy_renderer.render(enemy)
        # 플레이어 렌더링
        for player in engine.players:
            self.player_renderer.render(player)

        pygame.display.update()