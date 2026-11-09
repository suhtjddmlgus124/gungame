import random
import pygame
from engine.entity import Player
from ..ui import Healthbar

class PlayerRenderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.healthbar = Healthbar()

    def render(self, player: Player):
        if player.live:
            pygame.draw.rect(self.screen, self._pk_to_color(player.pk), player.rect)
            self.healthbar.render(self.screen, player, 'green')

    def _pk_to_color(self, pk):
        rng = random.Random(pk)
        return tuple(rng.randint(100, 255) for _ in range(3))