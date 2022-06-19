from typing import List

import pygame

from scripts.entity import Entity
from scripts.tile import Tile
from scripts.vector2 import Vector2

import random
import math

class EnemyBullet(Entity):
    def __init__(self, x, y, px, py):
        super().__init__(x, y)
        self.px = px
        self.py = py


        self.rect = pygame.Rect(x, y, 5, 5)

    def move_towards(self, x_pos: int, y_pos: int) -> None:
        """
        Moves entity toward a give position
        """

        position_vector = Vector2(self.rect.x-8, self.rect.y-8)
        update_position = position_vector.move_towards(x_pos, y_pos, 20)
        self.rect.x += update_position[0]
        self.rect.y += update_position[1] 

    def draw(self, display, player):
        self.move_towards(player.rect.x, player.rect.y)
        pygame.draw.circle(display, (255,0,0), (self.rect.x-player.camera.x, self.rect.y-player.camera.y), 5)

class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.images = [self.load_image("book_enemy_fly1"), self.load_image("book_enemy_fly2"), 
                       self.load_image("book_enemy_fly3"), self.load_image("book_enemy_fly4")]
        self.animation_index = 0

        self.rect = pygame.Rect(x, y, 20, 20)

        self.rotation = 0

        self.bullet_cooldown = 0
        self.rot_rect = pygame.Rect(x, y, 20, 20)
        self.offset = random.randrange(-32, 32)

    def get_centered_position(self) -> pygame.Rect:
        """
        Returns the center of the entities rect
        """

        return self.rect.center

    def move_towards(self, x_pos: int, y_pos: int) -> None:
        """
        Moves entity toward a give position
        """

        position_vector = Vector2(*self.get_centered_position())
        update_position = position_vector.move_towards(x_pos, y_pos, 3)
        self.rect.x += update_position[0] * abs(x_pos - position_vector.x) / 100 + 1.1
        self.rect.y += update_position[1] * abs(y_pos - position_vector.y) / 100 + 1.1 

    def rot_center(self, image, angle, x, y):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

        return rotated_image, new_rect

    def draw(self, display, player, enemy_bullets, explosions):
        self.animation_index = self.animate(self.images, self.animation_index, 5)
        self.move_towards(player.rect.x+self.offset, player.rect.y+self.offset)
        dy, dx = (player.rect.y) - self.rect.y, (player.rect.x) - self.rect.x
        self.rotation = math.degrees(-math.atan2(dy, dx))
        img_copy, rect = self.rot_center(self.images[self.animation_index//5], self.rotation, (self.rect.x-player.camera.x), (self.rect.y-player.camera.y))
        display.blit(img_copy, rect)
        self.rot_rect = rect

        