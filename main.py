import pygame
from image_handler import get_player_sprite

pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_player_sprite()


def main():
    player_x = 400
    player_y = 300
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Drunk Frogger")
    running = True

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        velocity = 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > velocity:
            player_x -= velocity
        if keys[pygame.K_RIGHT] and player_x < 800 - 40 - velocity:
            player_x += velocity
        if keys[pygame.K_DOWN] and player_y < 600 - 30 - velocity:
            player_y += velocity
        if keys[pygame.K_UP] and player_y > velocity:
            player_y -= velocity
        if keys[pygame.K_ESCAPE]:
            running = False

        screen.blit(get_player_sprite(), (player_x, player_y))
        pygame.display.update()


if __name__ == '__main__':
    main()
