import pygame

class PkGroup(pygame.sprite.Group):
    """
    pk를 속성으로 갖는 Sprite는 이 그룹을 사용할 수 있습니다.
    """

    def __init__(self, *sprites):
        self.__sprites = {}
        super().__init__(*sprites)

    def add_internal(self, sprite, layer=None):
        if sprite.pk in self.__sprites:
            raise ValueError(f"Duplicated sprite PK: {sprite.pk}")
        super().add_internal(sprite, layer)
        self.__sprites[sprite.pk] = sprite

    def remove_internal(self, sprite):
        super().remove_internal(sprite)
        self.__sprites.pop(sprite.pk, None)

    def get(self, pk):
        return self.__sprites.get(pk)

    def empty(self):
        super().empty()
        self.__sprites.clear()