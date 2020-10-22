import pygame


class Mob:
    def __init__(self, mob_x, mob_y, width, height, image, is_left):
        self.mob_x = mob_x
        self.mob_y = mob_y
        self.image = image
        self.width = width
        self.height = height
        self.velocity = 5
        self.mob_mask = pygame.mask.from_surface(self.image)
        self.mob_rect = self.image.get_rect(topleft=(self.mob_x, self.mob_y))
        self.is_left = is_left

    def update_rect(self, direction):
        self.mob_x += self.velocity * direction
        self.mob_rect = self.image.get_rect(topleft=(self.mob_x, self.mob_y))


class Goat:
    def __init__(self, get_x, get_y, width, height):
        self.get_x = get_x
        self.get_y = get_y
        self.width = width
        self.height = height
        self.velocity = 4
