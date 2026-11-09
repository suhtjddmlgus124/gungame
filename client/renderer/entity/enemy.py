import pygame
from engine.entity import Enemy
from ..ui import Healthbar

class EnemyRenderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.healthbar = Healthbar()

    def render(self, enemy: Enemy):
        pygame.draw.rect(self.screen, (150, 0, 0), enemy.rect)
        self.healthbar.render(self.screen, enemy, 'red')