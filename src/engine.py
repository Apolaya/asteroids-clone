from pathlib import Path
import sys

import pygame

from . import globals
from .Player import Player
from .Asteroid import AsteroidManager
from .UI import UI, StartModal, PauseModal, EndModal


bg_path = Path("assets", "art", "background.png")
music_path = Path("assets", "sounds", "through_space.ogg")

"""This method runs the game and is called in the top-level main module."""
def run():
    """Initialize audio mixer and engine, set up display, start clock, and set starting state"""
    pygame.mixer.pre_init(44100, -16, 2, 64)
    pygame.mixer.init()
    if pygame.mixer.get_init():
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.2)

    pygame.init()

    screen = pygame.display.set_mode((globals.WINDOW_WIDTH, globals.WINDOW_HEIGHT))
    pygame.display.set_caption("Asteroid Survivors")
    background = pygame.image.load(bg_path)

    start_modal = StartModal((globals.WINDOW_WIDTH/2,globals.WINDOW_HEIGHT/2))
    pause_modal = PauseModal((globals.WINDOW_WIDTH/2,globals.WINDOW_HEIGHT/2))

    clock = globals.CLOCK
    state = "START"
    mouse = (-1,-1)
    respawn_timer = 3

    #Create UI, asteroid spawner, and player
    ui = UI(screen)
    spawner = AsteroidManager()
    spawner.start_game()

    player = Player(
        pygame.math.Vector2((screen.get_width() / 2, screen.get_height() / 2))
    )
    globals.PLAYER_SPRITE.add(player)

    pygame.mixer.music.play()

    #Enter game loop
    while True:

        # limits FPS and returns value for framerate-independent physics
        globals.DT = clock.tick(globals.FRAMERATE) / 1000
        print(globals.SCORE)

        #Set state based on input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state == "EXIT"
                print("User closed the window")
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "PAUSED" if state == "RUNNING" else "RUNNING"
            
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = event.pos

        #Run the correct logic based  on current state
        if state == "START":
            globals.LIVES = 3
            globals.SCORE = 0
            screen.blit(background, (0, 0))
            screen.blit(start_modal,start_modal.rect)
            pygame.display.flip()
            clicked = start_modal.check_click(mouse)
            match clicked:
                case 'Start':
                    mouse = (-1,-1)
                    state = 'RUNNING'
                case 'Quit':
                    mouse = (-1,-1)
                    state = 'EXIT'
            continue

        #On pause, stop the simulation and display the pause modal
        if state == "PAUSED":
            screen.blit(background, (0,0))
            screen.blit(pause_modal, pause_modal.rect)
            ui.draw()
            pygame.display.flip()
            clicked = pause_modal.check_click(mouse)
            match clicked:
                case 'Resume':
                    mouse = (-1,-1)
                    state = 'RUNNING'
                case 'Quit':
                    pygame.quit()
                    sys.exit()
            continue
        
        #On running out of lives, display the game over modal
        if state == "GAMEOVER":
            end_modal = EndModal((globals.WINDOW_WIDTH/2,globals.WINDOW_HEIGHT/2))
            screen.blit(background, (0,0))
            screen.blit(end_modal, end_modal.rect)
            ui.draw()
            pygame.display.flip()
            clicked = end_modal.check_click(mouse)
            match clicked:
                case 'Retry':
                    mouse = (-1,-1)
                    state = 'START'
                case 'Quit':
                    pygame.quit()
                    sys.exit()
            continue

        #Standard gameplay state to run simulation
        if state == "RUNNING":
            #If player is destroyed, respawn and reset wave
            if len(globals.PLAYER_SPRITE) < 1:
                respawn_timer -= globals.DT
                if respawn_timer <= 0:
                  respawn_timer = 3
                  spawner.reset_game()
                  player = Player(
                      pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
                  )
                  globals.PLAYER_SPRITE.add(player)

            #Respond to continuous input from keys and mouse
            keys = pygame.key.get_pressed()
            left_mouse, middle_mouse, right_mouse = pygame.mouse.get_pressed()
            if keys[pygame.K_w]:
                player.move("UP")
            if keys[pygame.K_s]:
                player.move("DOWN")
            if keys[pygame.K_a]:
                player.move("LEFT")
            if keys[pygame.K_d]:
                player.move("RIGHT")
            if keys[pygame.K_SPACE] or left_mouse:
                player.shoot()

            #Update all sprites and the UI
            spawner.update()
            globals.PLAYER_SPRITE.update()
            globals.ASTEROID_SPRITES.update()
            globals.PROJECTILE_SPRITES.update()
            ui.update()
            screen.blit(background, (0, 0))

            #Handle collisions and increment score
            points, resources = spawner.handle_collision()
            globals.SCORE += points

            #Check for game over
            if globals.LIVES < 1:
                state = "GAMEOVER"

            #Draw all sprites to display
            globals.PLAYER_SPRITE.draw(screen)
            globals.ASTEROID_SPRITES.draw(screen)
            globals.PROJECTILE_SPRITES.draw(screen)
            ui.draw()
            pygame.display.flip()
