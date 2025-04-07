from pathlib import Path
import pygame
from . import globals

sprite_path = Path('assets', 'art', 'projectiles', 'laserBullet.png')

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, heading):
        super().__init__()
        self.ttl = 1250
        self.sprite_scaling = 0.4
        self.large_image = pygame.image.load(sprite_path).convert_alpha()
        self.image = pygame.transform.scale_by(self.large_image, self.sprite_scaling)
        self.start_img = self.image
        self.pos = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.speed = globals.PROJECTILE_SPEED
        self.heading = heading
        self.vel = pygame.math.Vector2.from_polar((self.speed, heading))
        self.created = pygame.time.get_ticks()

    def update(self, dt):
        if pygame.time.get_ticks() - self.created > self.ttl:
            self.kill()
            return
        self.rotate()
        self.pos += self.vel * dt
        self.rect.center = self.pos
        self.check_bounds()

    def rotate(self):
        self.image = pygame.transform.rotozoom(self.start_img, -self.heading - 90, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def check_bounds(self):
        if self.pos.x < 0:
            self.pos.x = globals.WINDOW_WIDTH
        if self.pos.x > globals.WINDOW_WIDTH:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = globals.WINDOW_HEIGHT
        if self.pos.y > globals.WINDOW_HEIGHT:
            self.pos.y = 0
