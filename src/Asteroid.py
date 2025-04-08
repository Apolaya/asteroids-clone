from pathlib import Path
import pygame
from . import globals, utilities

sprite_list = {
    2 : Path('assets', 'art', 'asteroids', 'large', 'a10000.png'),
    1 : Path('assets', 'art', 'asteroids', 'medium', 'a10000.png'),
    0 : Path('assets', 'art', 'asteroids', 'small', 'a10000.png')   
}

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos, size=2):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load(sprite_list[size]).convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.heading = utilities.random_heading()
        self.vel = self.heading * globals.ASTEROID_SPEED
        self.size = size

    def update(self):
        collisions = pygame.sprite.spritecollide(self, globals.PROJECTILE_SPRITES, False, collided=pygame.sprite.collide_mask)
        if len(collisions):
            for sprite in collisions:
                sprite.kill()
            self.destroy()
        self.pos += self.vel * globals.DT
        self.check_bounds()
        self.rect.center = self.pos
        self.mask = pygame.mask.from_surface(self.image)

    def check_bounds(self):
        if self.pos.x < 0:
            self.pos.x = globals.WINDOW_WIDTH
        if self.pos.x > globals.WINDOW_WIDTH:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = globals.WINDOW_HEIGHT
        if self.pos.y > globals.WINDOW_HEIGHT:
            self.pos.y = 0
    
    #TODO spawns with same velocity
    def destroy(self):
        if self.size > 0:
            for _ in range(globals.ASTEROID_MULTIPLE):
              asteroid = Asteroid(self.pos, self.size - 1)
              globals.ASTEROID_SPRITES.add(asteroid)
        globals.SCORE += globals.ASTEROID_POINTS * (self.size + 1)
        self.kill() 