import pygame
from engine.entity import Bullet

class BulletRenderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def render(self, bullet: Bullet):
        pygame.draw.circle(self.screen, 'yellow', bullet.rect.center, bullet.rect.width/2)