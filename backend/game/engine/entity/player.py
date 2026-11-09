import pygame
from pygame import Vector2 as Vector
from ..settings import *

class Player(pygame.sprite.Sprite):
    WIDTH = 40
    HEIGHT = 40
    SPEED = 250
    MAX_HP = 100
    RESPAWN_INTERVAL = 3.0

    def __init__(self, pk, initial_position):
        super().__init__()
        self.pk = pk
        self.rect = pygame.Rect(initial_position[0], initial_position[1], self.WIDTH, self.HEIGHT)
        self.rect.center = Vector(initial_position[0], initial_position[1])
        self.direction = Vector(0, 0)
        self.hp = self.MAX_HP
        self.live = True
        self.respawn_timer = 0.0

    # 이동
    def move(self, dx, dy):
        if self.live:
            self.direction = Vector(dx, dy)
        else:
            self.direction = Vector(0, 0)

    # 체력
    def damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def heal(self, amount):
        self.hp = min(self.MAX_HP, self.hp + amount)

    def update(self, dt):
        # 속도 정규화
        if self.direction.length_squared() > 0:
            self.direction.normalize_ip()

        # 움직임
        self.rect.center += self.direction * self.SPEED * dt

        # 화면에서 벗어나지 않도록 함
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WORLD_WIDTH)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, WORLD_HEIGHT)

        # 사망
        if self.hp <= 0:
            self.live = False
        # 부활
        if not self.live and self.respawn_timer < self.RESPAWN_INTERVAL:
            self.respawn_timer += dt
        if self.respawn_timer >= self.RESPAWN_INTERVAL:
            self.hp = self.MAX_HP
            self.rect.center = (WORLD_WIDTH/2, WORLD_HEIGHT/2)
            self.respawn_timer = 0.0
            self.live = True

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
        player = Player(pk=data['pk'], initial_position=(data['x'], data['y']))
        player.hp = data['hp']
        return player