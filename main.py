import pygame
import asyncio

from scripts.player import Player
from scripts.tile import Tile
from scripts.parachute import Parachute


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

    def render_map(self, display: pygame.Surface, tiles: List[Tile]) -> None:
        """
        Renders the games tiles
        """

        for tile in tiles:
            pygame.draw.rect(self.display, (60, 255, 100), (tile.rect.x-self.player.camera.x, tile.rect.y-self.player.camera.y, tile.rect.width, tile.rect.height))

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
                    if event.button == 1:
                        self.player.parachutes.append(Parachute(self.player.rect.x-self.player.camera.x, self.player.rect.y-self.player.camera.y-16))
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.player.parachutes.pop()

            keys = pygame.key.get_pressed()
            self.key_presses["a"] = keys[pygame.K_a]
            self.key_presses["d"] = keys[pygame.K_d]

            self.player.handle_movement(self.key_presses, self.tiles)
            self.player.draw(self.display)

            self.render_map(self.display, self.tiles)

            await asyncio.sleep(0)
            self.screen.blit(pygame.transform.scale(self.display, (600, 600)), (0, 0))
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def run(self):
        asyncio.run(self.main())