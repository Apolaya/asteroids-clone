import pygame

# Scene settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 960
CLOCK = pygame.time.Clock()
FRAMERATE = 60
DT = 0
LIVES = 3
SCORE = 0

# Projectile config
PROJECTILE_SPEED = 500
PROJECTILE_DAMAGE = 10

# Sprite groups
PLAYER_SPRITE = pygame.sprite.GroupSingle()
ASTEROID_SPRITES = pygame.sprite.Group()
PROJECTILE_SPRITES = pygame.sprite.Group()
