from pathlib import Path
import pygame
from . import globals
from .projectile import Projectile

sprite_path = Path("assets", "art", "spaceships", "bgbattleship.png")

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.start_img = self.image
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(0, 0)
        self.acceleration = 4
        self.friction = 1
        self.max_speed = 500
        self.fire_delay = 700
        self.last_shot = 0
        self.sprite_rotation_offset = -90

    def update(self):
        collisions = pygame.sprite.spritecollide(
            self, globals.ASTEROID_SPRITES, False, collided=pygame.sprite.collide_mask
        )
        if len(collisions):
            globals.LIVES -= 1
            self.destroy()
        self.pos += self.vel * globals.DT
        self.rect.center = self.pos
        self.mask = pygame.mask.from_surface(self.image)
        self.last_shot += globals.CLOCK.get_time()
        self.rotate()
        self.check_bounds()
        self.reduce_velocity()

    def rotate(self):
        _, self.angle = (pygame.mouse.get_pos() - self.pos).as_polar()
        self.image = pygame.transform.rotozoom(
            self.start_img, -self.angle + self.sprite_rotation_offset, 1
        )
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, direction):
        match direction:
            case "UP":
                if -1 * self.vel.y < self.max_speed:
                    self.vel.y -= self.acceleration
            case "DOWN":
                if self.vel.y < self.max_speed:
                    self.vel.y += self.acceleration
            case "LEFT":
                if -1 * self.vel.x < self.max_speed:
                    self.vel.x -= self.acceleration
            case "RIGHT":
                if self.vel.x < self.max_speed:
                    self.vel.x += self.acceleration

    def shoot(self):
        if self.last_shot >= self.fire_delay:
            self.last_shot = 0
            origin = self.pos + pygame.math.Vector2.from_polar(
                (self.image.get_height() / 2, self.angle)
            )
            projectile = Projectile(origin, self.angle)
            globals.PROJECTILE_SPRITES.add(projectile)

    def reduce_velocity(self):
        if self.vel.x < 0:
            self.vel.x += self.friction
        if self.vel.x > 0:
            self.vel.x -= self.friction
        if self.vel.y < 0:
            self.vel.y += self.friction
        if self.vel.y > 0:
            self.vel.y -= self.friction

    def check_bounds(self):
        if self.pos.x < 0:
            self.pos.x = globals.WINDOW_WIDTH
        if self.pos.x > globals.WINDOW_WIDTH:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = globals.WINDOW_HEIGHT
        if self.pos.y > globals.WINDOW_HEIGHT:
            self.pos.y = 0

    def destroy(self):
        self.kill()
