import pygame


class Tile:
    def __init__(self, rect, color):
        self.color = color
        self.image = pygame.image.load("assets/images/building.png").convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = pygame.Rect(rect)

    def collision(self, player_rect: pygame.Rect) -> bool:
        return player_rect.colliderect(self.rect)

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))