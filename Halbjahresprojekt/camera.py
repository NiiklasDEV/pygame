import pygame
vector = pygame.math.Vector2
from settings import Settings
from abc import ABC, abstractmethod

class Camera:
    def __init__(self, player) -> None:
        self.player = player
        self.offset = vector(0,0)
        self.offset_float = vector(0,0)
        self.CONST = vector(-Settings.window_width / 2 + player.rect.w / 2, - self.player.rect.bottom + 20)

    def setmethod(self,method):
        self.method = method

    def scroll(self):
        self.method.scroll()


class CamScroll(ABC):
    def __init__(self, camera, player) -> None:
        super().__init__()
        self.camera = camera
        self.player = player
    
    @abstractmethod
    def scroll(self):
        pass

class Follow(CamScroll):
    def __init__(self, camera, player) -> None:
        super().__init__(camera, player)
    
    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)


class Border(CamScroll):
    def __init__(self, camera, player) -> None:
        super().__init__(camera, player)

    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)
        self.camera.offset.x = max(self.player.left_border, self.camera.offset.x)
        self.camera.offset.x = min(self.camera.offset.x, self.player.right_border - Settings.window_width)

class Auto(CamScroll):
    def __init__(self, camera, player) -> None:
        super().__init__(camera, player)
    
    def scroll(self):
        self.camera.offset.x += 1

