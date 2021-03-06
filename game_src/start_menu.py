import sys

from game_src.score_handler import score_window
from game_src.settings import settings_window
from game_src.variabels import *
from image.image_handler import main_menu_image
from music_and_sound.sound_handler import get_title_music, music_volume
from game_src.window_handler import draw_text, instruction_window


def start_menu(sound_fx, volume, quiz_category):
    # This loads the sound handler module
    music_volume(volume)
    sound_fx.play_announcement()
    get_title_music()
    running = True
    while running:
        # This program writes out the start menu
        screen.blit(main_menu_image(), (0, 0))
        #screen.fill(WHITE)
        draw_text("Main Menu", menu_font_large, BLACK, screen, 370, 20, 'topleft')
        draw_text("[B]egin Game", menu_font, BLACK, screen, 500, 180, 'topleft')
        draw_text("[S]ettings", menu_font, BLACK, screen, 500, 260, 'topleft')
        draw_text("[T]utorial", menu_font, BLACK, screen, 500, 340, 'topleft')
        draw_text("[H]igh Score", menu_font, BLACK, screen, 500, 420, 'topleft')
        draw_text("[Q]uit Game", menu_font, BLACK, screen, 500, 500, 'topleft')

        # This section takes input user to control menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_b:
                    return volume, quiz_category
                if event.key == pygame.K_s:
                    volume, quiz_category = settings_window(volume, quiz_category)
                if event.key == pygame.K_t:
                    instruction_window()
                if event.key == pygame.K_h:
                    score_window()
                if event.key == pygame.K_q:
                    sys.exit()
        pygame.display.update()
