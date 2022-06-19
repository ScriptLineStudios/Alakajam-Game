import pygame
import asyncio

from scripts.player import Player
from scripts.tile import Tile
from scripts.parachute import Parachute
from scripts.enemy import Enemy

import random
from typing import List

import json

class Game:
    FPS = 60
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 600))
        self.display = pygame.Surface((150, 150))
        self.clock = pygame.time.Clock()

        self.running = True
        pygame.display.set_caption("Alakajam")

        self.player = Player(100, 100)

        self.key_presses = {"a": False, "d": False}

        with open("assets/map/map.json", "rb") as file:
            map_data = json.load(file)

        self.tiles = []
        for rect in map_data["map"]:
            self.tiles.append(Tile(rect=rect, color=(100, 100, 100)))

        self.enemies = []
        self.enemies.append(Enemy(100, 300))
        self.enemies.append(Enemy(120, 300))
        self.enemies.append(Enemy(140, 300))
        self.enemies.append(Enemy(160, 300))
        self.enemies.append(Enemy(180, 300))


        self.rot = 0

        self.enemy_bullets = []

        self.explosion_effects = []
        self.explosions = []


    def render_map(self, display: pygame.Surface, tiles: List[Tile]) -> None:
        """
        Renders the games tiles
        """

        for tile in tiles:
            display.blit(tile.image, (tile.rect.x-self.player.camera.x, tile.rect.y-self.player.camera.y))


    async def main(self):
        while self.running:
            self.display.fill((65, 106, 163))
            pygame.display.set_caption(f"{self.clock.get_fps()}")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.player.is_on_ground:
                            self.player.y_velocity -= self.player.JUMP_HEIGHT

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        self.player.parachutes.append(Parachute(self.player.rect.x-self.player.camera.x, self.player.rect.y-self.player.camera.y-16))
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3:
                        for i in range(10):
                            self.explosions.append([self.player.rect.x, self.player.rect.y+random.randrange(-7, 7), random.randrange(-4, 4),random.randrange(-2, 7), .01, (242, 211, 171), False, .05, 100, (159, 79, 80)])
                        self.player.parachutes.pop()



            keys = pygame.key.get_pressed()
            self.key_presses["a"] = keys[pygame.K_a]
            self.key_presses["d"] = keys[pygame.K_d]

            self.player.handle_movement(self.key_presses, self.tiles)
            self.player.draw(self.display)

            for enemy in self.enemies:
                if enemy.rot_rect.colliderect(pygame.Rect(self.player.rect.x-self.player.camera.x, self.player.rect.y-self.player.camera.y, 16, 16)):
                    for i in range(100):
                        self.explosions.append([self.player.rect.x, self.player.rect.y+random.randrange(-7, 7), random.randrange(-4, 4),random.randrange(-2, 7), 1, (242, 211, 171), False, .2, 100, (39, 39, 68)])
                    self.enemies.remove(enemy)
                    self.player.y_velocity -= 5
                enemy.draw(self.display, self.player, self.enemy_bullets, self.explosions)

            for bullet in self.enemy_bullets:
                bullet.draw(self.display, self.player)

            self.render_map(self.display, self.tiles)

            for eff in self.explosion_effects:
                  eff[2] -= 1
                  if eff[2] <= 0:
                        self.explosion_effects.remove(eff)
                  pygame.draw.circle(self.display, eff[3], (eff[0]-self.player.camera.x,eff[1]-self.player.camera.y), 1)

            for part in self.explosions:
                  if part[7] <= 0:
                        self.explosions.remove(part)
                  part[1] -= part[3]*random.random()
                  if part[3] > -10:
                        part[3] -= .3
                  part[0] += part[2]*random.random()
                  part[4] += .01
                  part[7] -= .005
                  if part[6] is False:
                        self.explosion_effects.append([part[0], part[1], 10, part[9]])

                  pygame.draw.circle(self.display, part[5], (part[0]-self.player.camera.x, part[1]-self.player.camera.y), part[4])


            await asyncio.sleep(0)
            self.screen.blit(pygame.transform.scale(self.display, (600, 600)), (0, 0))
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def run(self):
        asyncio.run(self.main())