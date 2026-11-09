import pygame
from pygame import Vector2 as Vector
from ..settings import *

class Bullet(pygame.sprite.Sprite):
    WIDTH = 5
    HEIGHT = 5
    SPEED = 500
    DAMAGE = 10

    def __init__(self, pk, initial_position, initial_direction, shooter_pk):
        super().__init__()
        self.pk = pk
        self.rect = pygame.Rect(initial_position[0], initial_position[1], self.WIDTH, self.HEIGHT)
        self.rect.center = Vector(initial_position[0], initial_position[1])
        self.direction = Vector(initial_direction[0], initial_direction[1])
        self.shooter_pk = shooter_pk

        # 속도 정규화
        if self.direction.length_squared() > 0:
            self.direction.normalize_ip()

    def update(self, dt):
        # 움직임
        self.rect.center += self.direction * self.SPEED * dt

        # 화면에서 벗어나면 삭제
        if self.rect.bottom < 0 or self.rect.top > WORLD_HEIGHT or self.rect.right < 0 or self.rect.left > WORLD_WIDTH:
            self.kill()

    # state
    def serialize(self):
        return {
            'pk': self.pk,
            'x': self.rect.centerx,
            'y': self.rect.centery,
        }

    @classmethod
    def deserialize(self, data):
        return Bullet(
            data['pk'], 
            initial_position=(data['x'], data['y']), 
            initial_direction=(0, 0),
            shooter_pk=0,
        )