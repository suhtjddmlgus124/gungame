import pygame
from pygame import Vector2 as Vector
from ..settings import *

class Enemy(pygame.sprite.Sprite):
    WIDTH = 40
    HEIGHT = 40
    SPEED = 80
    MAX_HP = 200
    ATTACK_INTERVAL = 1
    DAMAGE = 10

    def __init__(self, pk, initial_position):
        super().__init__()
        self.pk = pk
        self.rect = pygame.Rect(
            initial_position[0],
            initial_position[1],
            self.WIDTH,
            self.HEIGHT,
        )
        self.rect.center = Vector(initial_position[0], initial_position[1])
        self.direction = Vector(0, 0)
        self.hp = self.MAX_HP
        self.attack_timer = 0.0

    def move(self, dx, dy):
        self.direction = Vector(dx, dy)

    def damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def heal(self, amount):
        self.hp = min(self.MAX_HP, self.hp + amount)

    def update(self, dt):
        if self.hp <= 0:
            self.kill()

        if self.direction.length_squared() > 0:
            self.direction.normalize_ip()

        self.rect.center += self.direction * self.SPEED * dt

        # 공격 쿨타임
        self.attack_timer += dt

    # state
    def serialize(self):
        return {
            'pk': self.pk,
            'x': self.rect.centerx,
            'y': self.rect.centery,
            'hp': self.hp,
        }

    @classmethod
    def deserialize(self, data):
        enemy = Enemy(pk=data['pk'], initial_position=(data['x'], data['y']))
        enemy.hp = data['hp']
        return enemy