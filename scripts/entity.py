import pygame
import abc

class Entity(abc.ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def load_image(self, path):
        image = pygame.image.load(f"assets/images/{path}.png").convert()
        image.set_colorkey((255, 255, 255))
        return image

    def animate(self, image_list, animation_index, time_to_show_image_on_screen):
        if animation_index+1 >= len(image_list)*time_to_show_image_on_screen:
            animation_index = 0
        animation_index += 1

        return animation_index

    abc.abstractclassmethod
    def draw(self, display):
        pass