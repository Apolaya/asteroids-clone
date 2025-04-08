import pygame
import random

from . import globals


def spawn_location():
    player = globals.PLAYER_SPRITE.sprite
    loc = player.pos.copy()
    while loc.distance_to(player.pos) < 100:
      x = random.randint(0, globals.WINDOW_WIDTH)
      y = random.randint(0, globals.WINDOW_HEIGHT)
      loc = pygame.math.Vector2((x, y))
    return loc

def random_heading():
   return pygame.math.Vector2(random.randrange(-100, 100)/100, random.randrange(-100, 100)/100)

def random_angle():
    return random.randint(0, 360)
