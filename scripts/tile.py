import pygame


class Tile:
    def __init__(self, rect, color):
        self.color = color

        self.rect = pygame.Rect(rect)

    def collision(self, player_rect: pygame.Rect) -> bool:
        return player_rect.colliderect(self.rect)

    def draw(self, display):
        pygame.draw.rect(display, self.color, self.rect)