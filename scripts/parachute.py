from typing import List

import pygame

from scripts.entity import Entity
from scripts.tile import Tile

class Parachute(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.parachute_deploy_images = [self.load_image("parachute_deploy1"), self.load_image("parachute_deploy2"), self.load_image("parachute_deploy3"),
        self.load_image("parachute_deploy4")]

        self.animation_index = 0

    def draw(self, display, player):
        self.x = player.rect.x
        self.y = player.rect.y-8

        if self.animation_index < 18:
            self.animation_index = self.animate(self.parachute_deploy_images, self.animation_index, 5)
        display.blit(self.parachute_deploy_images[self.animation_index//5], (self.x-player.camera.x, self.y-player.camera.y))