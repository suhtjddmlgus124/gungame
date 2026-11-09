from itertools import count
import random
import pygame
from pygame import Vector2 as Vector
from .entity import Player, Bullet, Enemy
from .utils import PkGroup
from .settings import *

class Engine:
    ENEMY_SPAWN_INTERVAL = 5
    ENEMY_SPERATION_RADIUS = 50
    ENEMY_SPERATION_WEIGHT = 1.5

    def __init__(self):
        self.tick = 0

        self.players = PkGroup()

        self.bullets = PkGroup()
        self.bullet_pk = count(1)

        self.enemies = PkGroup()
        self.enemy_pk = count(1)
        self.enemy_spawn_timer = 0.0

    # state
    def get_state(self):
        return {
            'tick': self.tick,
            'players': { str(p.pk): p.serialize() for p in self.players },
            'enemies': { str(e.pk): e.serialize() for e in self.enemies },
            'bullets': { str(b.pk): b.serialize() for b in self.bullets },
        }

    def load_state(self, state):
        self.tick = state['tick']
        self.players.empty()
        self.enemies.empty()
        self.bullets.empty()
        for p_data in state['players'].values():
            self.players.add(Player.deserialize(p_data))
        for e_data in state['enemies'].values():
            self.enemies.add(Enemy.deserialize(e_data))
        for b_data in state['bullets'].values():
            self.bullets.add(Bullet.deserialize(b_data))
    
    # 플레이어
    def add_player(self, pk, initial_position):
        player = Player(pk, initial_position)
        self.players.add(player)
        return player

    def remove_player(self, pk):
        player = self.players.get(pk)
        if player: 
            player.kill()

    def move_player(self, pk, dx, dy):
        player = self.players.get(pk)
        if player: 
            player.move(dx, dy)

    def shoot_player(self, pk, x, y):
        player = self.players.get(pk)
        if not player:
            return

        direction = Vector(x, y) - Vector(player.rect.center)
        bullet = Bullet(next(self.bullet_pk), player.rect.center, direction, player.pk)
        self.bullets.add(bullet)

    # 적
    def add_enemy(self, initial_position):
        enemy = Enemy(next(self.enemy_pk), initial_position)
        self.enemies.add(enemy)

    # 로직
    def update(self, dt):
        self.players.update(dt)
        self.bullets.update(dt)
        self.enemies.update(dt)

        # 적이 총알에 맞는 것 구현
        enemy_bullet_collisions = pygame.sprite.groupcollide(self.enemies, self.bullets, False, False)
        for enemy, bullets in enemy_bullet_collisions.items():
            for bullet in bullets:
                enemy.damage(bullet.DAMAGE)
                bullet.kill()
        
        # 적이 가장 가까운 살아 있는 플레이어를 추적
        live_players = list(filter(lambda p: p.live, self.players))
        if len(live_players) > 0:
            for enemy in self.enemies:
                target = min(live_players, key=lambda p: Vector(Vector(p.rect.center) - Vector(enemy.rect.center)).length_squared(), default=None)
                if target is None:
                    break

                target_direction = Vector(target.rect.center) - Vector(enemy.rect.center)
                if target_direction.length_squared() > 0:
                    target_direction.normalize_ip()

                # 분리 행동 (집단이 서로 뭉치지 않도록 함)
                seperation = Vector(0, 0)
                for other in self.enemies:
                    if enemy is other:
                        continue
                    offset = Vector(enemy.rect.center) - Vector(other.rect.center)
                    if 0 < offset.length_squared() < self.ENEMY_SPERATION_RADIUS ** 2:
                        seperation += offset.normalize()
                if seperation.length_squared() > 0:
                    seperation.normalize_ip()

                direction = target_direction + seperation * self.ENEMY_SPERATION_WEIGHT
                enemy.move(direction.x, direction.y)
        else:
            for enemy in self.enemies:
                enemy.move(0, 0)

        # 일정 시간마다 적이 네 모서리에서 생성됨
        self.enemy_spawn_timer += dt
        if self.enemy_spawn_timer >= self.ENEMY_SPAWN_INTERVAL:
            side = random.randint(0, 3)
            if side == 0:
                self.add_enemy((random.uniform(0, WORLD_WIDTH), 0))
            elif side == 1:
                self.add_enemy((WORLD_WIDTH, random.uniform(0, WORLD_HEIGHT)))
            elif side == 2:
                self.add_enemy((random.uniform(0, WORLD_WIDTH), WORLD_HEIGHT))
            else:
                self.add_enemy((0, random.uniform(0, WORLD_HEIGHT)))
            self.enemy_spawn_timer = 0.0

        # 적이 살아있는 플레이어를 공격
        player_enemy_collisions = pygame.sprite.groupcollide(self.players, self.enemies, False, False)
        for player, enemies in player_enemy_collisions.items():
            for enemy in enemies:
                if enemy.attack_timer >= enemy.ATTACK_INTERVAL and player.live:
                    player.damage(enemy.DAMAGE)
                    enemy.attack_timer = 0.0

        self.tick += 1