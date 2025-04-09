from pathlib import Path
import pygame
from . import globals
from .projectile import Projectile

"""Load asset file paths on import."""
sprite_path = Path("assets", "art", "spaceships", "bgbattleship.png")
shoot_sound_path = Path("assets", "sounds", "alienshoot1.wav")
destroyed_sound_path = Path("assets", "sounds", "mechanical_explosion.wav")

"""This class manages the player-controlled sprite."""
class Player(pygame.sprite.Sprite):
    """Initialize with Sprite properties and custom gameplay properties."""
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
        self.shoot_sound = pygame.mixer.Sound(shoot_sound_path)
        self.shoot_sound.set_volume(0.5)
        self.destroyed_sound = pygame.mixer.Sound(destroyed_sound_path)
        self.destroyed_sound.set_volume(0.5)

    """Called on every loop to update state and position."""
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

    """Rotates player sprite toward mouse position."""
    def rotate(self):
        _, self.angle = (pygame.mouse.get_pos() - self.pos).as_polar()
        self.image = pygame.transform.rotozoom(
            self.start_img, -self.angle + self.sprite_rotation_offset, 1
        )
        self.rect = self.image.get_rect(center=self.rect.center)

    """Takes input from player to move sprite."""
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

    """Fires a Projectile object on player input, given a minimum set interval."""
    def shoot(self):
        if self.last_shot >= self.fire_delay:
            self.shoot_sound.play()
            self.last_shot = 0
            origin = self.pos + pygame.math.Vector2.from_polar(
                (self.image.get_height() / 2, self.angle)
            )
            projectile = Projectile(origin, self.angle)
            globals.PROJECTILE_SPRITES.add(projectile)

    """Gradually reduce the sprite velocity to simulate friction (ignore that we're in space)."""
    def reduce_velocity(self):
        if self.vel.x < 0:
            self.vel.x += self.friction
        if self.vel.x > 0:
            self.vel.x -= self.friction
        if self.vel.y < 0:
            self.vel.y += self.friction
        if self.vel.y > 0:
            self.vel.y -= self.friction

    """Wrap movement around screen boundaries."""
    def check_bounds(self):
        if self.pos.x < 0:
            self.pos.x = globals.WINDOW_WIDTH
        if self.pos.x > globals.WINDOW_WIDTH:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = globals.WINDOW_HEIGHT
        if self.pos.y > globals.WINDOW_HEIGHT:
            self.pos.y = 0

    """Play spaceship destruction audio and remove the player sprite."""
    def destroy(self):
        self.destroyed_sound.play()
        self.kill()
