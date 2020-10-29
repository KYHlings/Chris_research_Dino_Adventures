from random import randint

import pygame

from game_src.level_handler import create_level
from game_src.pause_screen import pause_screen
from game_src.score_counter import score_by_player_position
from sprites_classes.dead_frog import Dead_Frog
from image.image_handler import get_player_sprite, get_get_sprite, get_mob_sprite, \
    get_life_sprite, get_roadkill_sprite, get_beer_sprite, get_floating_mob_sprite, get_sloshed_face, get_drowned_sprite

from sprites_classes.npc import Mob, Goat, Floating_mob
from sprites_classes.player import Player
from quiz_ui.quiz_handler import quiz_window, quiz
from music_and_sound.sound_handler import get_level_music, get_goat_music, get_drunk_music
from game_src.window_handler import screen, lose_window, win_window, \
    text_object, score_font, roadkill_window, drown_window


# This function updates the window with sprites_classes each loop
def redraw_window(animals, wise_goat, dead_frog, background_image, lanes, floating_lanes, score):
    screen.blit(background_image, (0, 0))
    score_text, score_rect = text_object(f"score:{score}", score_font)
    score_rect.topright = (790, 10)
    screen.blit(score_text, score_rect)
    life_x = 10
    beer_y = 285

    for i in range(animals.lives):
        screen.blit(get_life_sprite(), (life_x, 10))
        life_x += 25
    for lane in floating_lanes:
        for mob in lane.floating_mobs:
            screen.blit(mob.image, mob.mob_rect)

    if dead_frog.is_dead:
        if dead_frog.cause_of_death == "roadkill":
            screen.blit(dead_frog.roadkill_img, (dead_frog.dead_x, dead_frog.dead_y))
        elif dead_frog.cause_of_death == "drowned":
            screen.blit(dead_frog.drowned_img, (dead_frog.dead_x, dead_frog.dead_y))
        screen.blit(animals.update_img()[0], (1000, 1000))

    else:
        screen.blit(animals.update_img()[0], animals.update_img()[1])
    for lane in lanes:
        for car in lane.mobs:
            screen.blit(car.image, car.mob_rect)
    screen.blit(get_get_sprite(), (animals.player_x - 20, wise_goat.get_y - 30))

    screen.blit(get_life_sprite(), (10, 315))
    screen.blit(pygame.transform.flip(get_sloshed_face(), True, True), (10, 180))
    for i in range(animals.drunk_meter):
        screen.blit(get_beer_sprite(), (15, beer_y))
        beer_y -= 25

    pygame.display.update()


# This function runs the main game
def game_loop(sound_fx, volume):
    clock = pygame.time.Clock()
    animals = Player(400, 570, 40, 30, 0, get_player_sprite(0))
    dead_frog = Dead_Frog()
    pygame.display.set_caption("Drunk Frogger")

    level_number = 1
    score = 0
    while True:
        last_y = 570
        question_number = 1
        level = create_level(level_number)
        wise_goat = Goat(animals.player_x, level.quiz_cord[0])
        running = True
        get_level_music(level_number)
        while running:
            score, last_y = score_by_player_position(animals.player_y, last_y, score)
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            for lane in level.lanes:
                for car in lane.mobs[:]:
                    if not car.is_left:
                        car.update_rect(1, lane.velocity)
                        if car.mob_x >= 800:
                            lane.mobs.remove(car)
                    else:
                        car.update_rect(-1, lane.velocity)
                        if car.mob_x <= -50:
                            lane.mobs.remove(car)
            for lane in level.floating_lanes:
                for floating_mob in lane.floating_mobs[:]:
                    if not floating_mob.is_left:
                        floating_mob.update_rect(1, lane.velocity)
                        if floating_mob.mob_x >= 800:
                            lane.floating_mobs.remove(floating_mob)
                    else:
                        floating_mob.update_rect(-1, lane.velocity)
                        if floating_mob.mob_x <= -50:
                            lane.floating_mobs.remove(floating_mob)

            for i in range(len(level.lanes)):
                if pygame.time.get_ticks() - level.time_spawned[i] >= level.spawn_timer[i]:
                    if not level.lanes[i].is_left:
                        level.lanes[i].mobs.append(
                            Mob(-40, level.lanes[i].y, get_mob_sprite(False), level.lanes[i].is_left))
                    else:
                        level.lanes[i].mobs.append(
                            Mob(800, level.lanes[i].y, get_mob_sprite(True), level.lanes[i].is_left))
                    level.time_spawned[i] = pygame.time.get_ticks()
                    level.spawn_timer[i] = randint(1000, 2000)

            for i in range(len(level.floating_lanes)):
                if pygame.time.get_ticks() - level.fl_time_spawned[i] >= level.fl_spawn_timer[i]:
                    if not level.floating_lanes[i].is_left:
                        level.floating_lanes[i].floating_mobs.append(
                            Floating_mob(-40, level.floating_lanes[i].y, get_floating_mob_sprite(False),
                                         level.floating_lanes[i].is_left))
                    else:
                        level.floating_lanes[i].floating_mobs.append(
                            Floating_mob(800, level.floating_lanes[i].y, get_floating_mob_sprite(True),
                                         level.floating_lanes[i].is_left))
                    level.fl_time_spawned[i] = pygame.time.get_ticks()
                    level.fl_spawn_timer[i] = randint(1000, 2000)
            keys = pygame.key.get_pressed()
            if dead_frog.is_dead:
                dead_frog.check_time_of_death()
            else:
                animals.move(keys)
            if keys[pygame.K_p]:
                level.spawn_paused()
                volume = pause_screen(volume)
                level.spawn_resumed()
                if not volume:
                    return

            for lane in level.lanes:
                for car in lane.mobs:
                    if animals.check_collide(car):
                        score -= 20
                        if animals.lives != 1:
                            animals.lives -= 1
                            dead_frog.player_died(animals.player_x, animals.player_y, "roadkill")
                            sound_fx.play_splat()
                            animals.reset()
                        else:
                            roadkill_window()
                            return

            animals.floating = False
            for lane in reversed(level.floating_lanes):
                if not animals.floating:
                    for floating_mob in lane.floating_mobs:
                        if animals.check_collide(floating_mob):
                            animals.floating = True
                            if lane.is_left:
                                animals.player_x -= lane.velocity
                            else:
                                animals.player_x += lane.velocity

                            break
                        else:
                            animals.floating = False

            if level.sinking_cord[0] < animals.player_y < level.sinking_cord[1] and not animals.floating:
                score -= 20
                if animals.lives != 1:
                    animals.lives -= 1
                    dead_frog.player_died(animals.player_x, animals.player_y, "drowned")
                    sound_fx.play_splash()
                    animals.reset()
                else:
                    drown_window()
                    return

            # This if statement checks if the player has reached the safe zone and triggers the quiz function
            if animals.player_y <= level.quiz_cord[question_number - 1]:
                level.spawn_paused()
                get_goat_music()

                # This if statement checks if the player answers correctly. If the player answers correctly they trigger the win function
                # if they do not answer correctly they get moved to the start position and adds one to the drunk_meter integer
                if not quiz_window(quiz()):
                    score -= 100
                    if animals.drunk_meter == 4:
                        lose_window()
                        return
                    animals.drunk_meter += 1
                    dead_frog.roadkill_img = get_roadkill_sprite(animals.drunk_meter)
                    dead_frog.drowned_img = get_drowned_sprite(animals.drunk_meter)
                    sound_fx.play_burp()
                    animals.drunken_consequence()
                    get_drunk_music(level_number, animals.drunk_meter)
                    animals.reset()
                else:
                    score += 100
                    question_number += 1
                    if question_number == level.amount_quiz + 1:
                        if no_death:
                            score += 200

                        win_window()
                        animals.reset()
                        running = False
                    else:
                        wise_goat.get_y = level.quiz_cord[question_number - 1]
                        if animals.drunk_meter == 0:
                            get_level_music(level_number)
                        else:
                            get_drunk_music(level_number, animals.drunk_meter)
                level.spawn_resumed()
            redraw_window(animals, wise_goat, dead_frog, level.background_image, level.lanes, level.floating_lanes,
                          score)
        level_number += 1
        if level_number == 3:
            level_number = 1
