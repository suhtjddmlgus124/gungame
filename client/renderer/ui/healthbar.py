import pygame

class Healthbar:
    """
    MAX_HP와 hp를 가진 sprite만 사용할 수 있습니다.
    """
    WIDTH = 45
    HEIGHT = 6
    OFFSET = 6

    def render(self, screen: pygame.Surface, sprite, color):
        ratio = sprite.hp / sprite.MAX_HP

        background = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        background.midbottom = (sprite.rect.centerx, sprite.rect.top - self.OFFSET)
        pygame.draw.rect(screen, 'white', background)

        health = background.copy()
        health.width = round(background.width * ratio)
        pygame.draw.rect(screen, color, health)