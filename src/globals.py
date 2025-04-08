import pygame

#Scene settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 960
DT = 30
LIVES = 3
SCORE = 0

PROJECTILE_SPEED = 500

#Asteroid config
ASTEROID_SPEED = 75
ASTEROID_MULTIPLE = 2
ASTEROID_POINTS = 3
SPAWN_RATE = 5000

#Sprite groups
PLAYER_SPRITE = pygame.sprite.GroupSingle()
ASTEROID_SPRITES = pygame.sprite.Group()
PROJECTILE_SPRITES = pygame.sprite.Group()
