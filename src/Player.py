from pathlib import Path
import pygame
from . import globals
from .projectile import Projectile

"""Load asset file paths on import."""
sprite_path = Path("assets", "art", "spaceships", "bgbattleship.png")
shoot_sound_path = Path("assets", "sounds", "laserfire01.ogg")
upgrade_shoot_sound_path = Path("assets", "sounds", "laserfire02.ogg")
destroyed_sound_path = Path("assets", "sounds", "mechanical_explosion.wav")
shield_path = Path("assets", "art", "spaceships", "spr_shield.png")

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
        self.damage_up = 0
        self.shield_up = 0
        self.shield = None

    """Called on every loop to update state and position."""
    def update(self):
        asteroid_collisions = pygame.sprite.spritecollide(
            self, globals.ASTEROID_SPRITES, False, collided=pygame.sprite.collide_mask
        )
        if len(asteroid_collisions):
            if self.shield:
                self.shield_up = 0
                globals.PLAYER_SPRITE.remove(self.shield)
                self.shield.kill()
                self.shield = None
                for asteroid in asteroid_collisions:
                    asteroid.asteroid_sound.set_volume(asteroid.size * 0.2)
                    asteroid.asteroid_sound.play()
                    asteroid.kill()
            else:
                self.destroy()
                globals.PICKUP_SPRITES.empty()

        pickup_collisions = pygame.sprite.spritecollide(
            self, globals.PICKUP_SPRITES, False, collided=pygame.sprite.collide_mask
        )
        for pickup in pickup_collisions:
            pickup.sound.play()
            if pickup.type == 'shield':
                self.add_shield()
                pickup.kill()
            if pickup.type == 'damage':
                self.add_damage()
                pickup.kill()

        self.pos += self.vel * globals.DT
        self.rect.center = self.pos
        self.mask = pygame.mask.from_surface(self.image)
        self.last_shot += globals.CLOCK.get_time()
        self.check_boosts()
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
            damage_boost = self.damage_up > 0
            projectile = Projectile(origin, self.angle, damage_boost)
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

    """Add damage boost from resource pickup"""
    def add_damage(self):
        self.damage_up += 300
        globals.PROJECTILE_DAMAGE = 30
        self.shoot_sound = pygame.mixer.Sound(upgrade_shoot_sound_path)
    
    """Add shield boost from resource pickup"""
    def add_shield(self):
        self.shield_up += 300
        if not self.shield:
          self.shield = Shield(self)
          globals.PLAYER_SPRITE.add(self.shield)
    
    """Check for boosts from pickups on each update and decrement remaining boost time"""
    def check_boosts(self):
        if self.damage_up > 0:
            self.damage_up -= 1
        else:
            globals.PROJECTILE_DAMAGE = 10
            self.shoot_sound = pygame.mixer.Sound(shoot_sound_path)
          
        
        if self.shield_up > 0:
            self.shield_up -= 1
        elif self.shield:
            globals.PLAYER_SPRITE.remove(self.shield)
            self.shield.kill()
            self.shield = None

    """Play spaceship destruction audio and remove the player sprite."""
    def destroy(self):
        globals.LIVES -= 1
        self.destroyed_sound.play()
        self.kill()

"""Sprite to draw as an overlay on the player ship to represent the shield boost"""
class Shield(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.sprite_scaling = 0.3
        self.large_image = pygame.image.load(shield_path).convert_alpha()
        self.image = pygame.transform.scale_by(self.large_image, self.sprite_scaling)
        self.rect = self.image.get_rect(center=player.rect.center)
    
    def update(self):
        self.rect.center = self.player.rect.center