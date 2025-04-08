import pygame
import random
import math
from pathlib import Path
from . import globals

# Using the asteroid art files organized by size
ASTEROID_PATHS = {
    "large": [
        Path('assets', 'art', 'asteroids', 'large', f) for f in [
            'a10000.png', 'a10001.png', 'a10002.png', 'a10003.png', 'a10004.png',
            'a10005.png', 'a10006.png', 'a10007.png', 'a10008.png', 'a10009.png',
            'a10010.png', 'a10011.png', 'a10012.png', 'a10013.png', 'a10014.png',
            'a10015.png', 'a30000.png', 'a30001.png', 'a30002.png', 'a30003.png',
            'a30004.png', 'a30005.png', 'a30006.png', 'a30007.png', 'a30008.png',
            'a30009.png', 'a30010.png', 'a30011.png', 'a30012.png', 'a30013.png',
            'a30014.png', 'a30015.png', 'b10000.png', 'b10001.png', 'b10002.png',
            'b10003.png', 'b10004.png', 'b10005.png', 'b10006.png', 'b10007.png',
            'b10008.png', 'b10009.png', 'b10010.png', 'b10011.png', 'b10012.png',
            'b10013.png', 'b10014.png', 'b10015.png', 'b30000.png', 'b30001.png',
            'b30002.png', 'b30003.png', 'b30004.png', 'b30005.png', 'b30006.png',
            'b30007.png', 'b30008.png', 'b30009.png', 'b30010.png', 'b30011.png',
            'b30012.png', 'b30013.png', 'b30014.png', 'b30015.png', 'c10000.png',
            'c10001.png', 'c10002.png', 'c10003.png', 'c10004.png', 'c10005.png',
            'c10006.png', 'c10007.png', 'c10008.png', 'c10009.png', 'c10010.png',
            'c10011.png', 'c10012.png', 'c10013.png', 'c10014.png', 'c10015.png',
            'c30000.png', 'c30001.png', 'c30002.png', 'c30003.png', 'c30004.png',
            'c30005.png', 'c30006.png', 'c30007.png', 'c30008.png', 'c30009.png',
            'c30010.png', 'c30011.png', 'c30012.png', 'c30013.png', 'c30014.png',
            'c30015.png', 'c40000.png', 'c40001.png', 'c40002.png', 'c40003.png',
            'c40004.png', 'c40005.png', 'c40006.png', 'c40007.png', 'c40008.png',
            'c40009.png', 'c40010.png', 'c40011.png', 'c40012.png', 'c40013.png',
            'c40014.png','c40015.png'
        ]
    ],
    "medium": [
        Path('assets', 'art', 'asteroids', 'medium', f) for f in [
            'a10000.png', 'a10001.png', 'a10002.png', 'a10003.png', 'a10004.png',
            'a10005.png', 'a10006.png', 'a10007.png', 'a10008.png', 'a10009.png',
            'a10010.png', 'a10011.png', 'a10012.png', 'a10013.png', 'a10014.png',
            'a10015.png', 'a30000.png', 'a30001.png', 'a30002.png', 'a30003.png',
            'a30004.png', 'a30005.png', 'a30006.png', 'a30007.png', 'a30008.png',
            'a30009.png', 'a30010.png', 'a30011.png', 'a30012.png', 'a30013.png',
            'a30014.png', 'a30015.png', 'a40000.png', 'a40001.png', 'a40002.png',
            'a40003.png', 'a40004.png', 'a40005.png', 'a40006.png', 'a40007.png',
            'a40008.png', 'a40009.png', 'a40010.png', 'a40011.png', 'a40012.png',
            'a40013.png', 'a40014.png', 'a40015.png', 'b40000.png', 'b40001.png',
            'b40002.png', 'b40003.png', 'b40004.png', 'b40005.png', 'b40006.png',
            'b40007.png', 'b40008.png', 'b40009.png', 'b40010.png', 'b40011.png',
            'b40012.png', 'b40013.png', 'b40014.png', 'b40015.png', 'c10000.png',
            'c10001.png', 'c10002.png', 'c10003.png', 'c10004.png', 'c10005.png',
            'c10006.png', 'c10007.png', 'c10008.png', 'c10009.png', 'c10010.png',
            'c10011.png', 'c10012.png', 'c10013.png', 'c10014.png', 'c10015.png',
            'c30000.png', 'c30001.png', 'c30002.png', 'c30003.png', 'c30004.png',
            'c30005.png', 'c30006.png', 'c30007.png', 'c30008.png', 'c30009.png',
            'c30010.png', 'c30011.png', 'c30012.png', 'c30013.png', 'c30014.png',
            'c30015.png', 'c40000.png', 'c40001.png', 'c40002.png', 'c40003.png',
            'c40004.png', 'c40005.png', 'c40006.png', 'c40007.png', 'c40008.png',
            'c40009.png', 'c40010.png', 'c40011.png', 'c40012.png', 'c40013.png',
            'c40014.png', 'c40015.png', 'd10000.png', 'd10001.png', 'd10002.png',
            'd10003.png', 'd10004.png', 'd10005.png', 'd10006.png', 'd10007.png',
            'd10008.png', 'd10009.png', 'd10010.png', 'd10011.png', 'd10012.png',
            'd10013.png', 'd10014.png', 'd10015.png', 'd30000.png', 'd30001.png',
            'd30002.png', 'd30003.png', 'd30004.png', 'd30005.png', 'd30006.png',
            'd30007.png', 'd30008.png', 'd30009.png', 'd30010.png', 'd30011.png',
            'd30012.png', 'd30013.png', 'd30014.png', 'd30015.png', 'd40000.png',
            'd40001.png', 'd40002.png', 'd40003.png', 'd40004.png', 'd40005.png',
            'd40006.png', 'd40007.png', 'd40008.png', 'd40009.png', 'd40010.png',
            'd40011.png', 'd40012.png', 'd40013.png', 'd40014.png', 'd40015.png'
        ]
    ],
    "small": [
        Path('assets', 'art', 'asteroids', 'small', f) for f in [
            'a10000.png', 'a10001.png', 'a10002.png', 'a10003.png', 'a10004.png',
            'a10005.png', 'a10006.png', 'a10007.png', 'a10008.png', 'a10009.png',
            'a10010.png', 'a10011.png', 'a10012.png', 'a10013.png', 'a10014.png',
            'a10015.png', 'a30000.png', 'a30001.png', 'a30002.png', 'a30003.png',
            'a30004.png', 'a30005.png', 'a30006.png', 'a30007.png', 'a30008.png',
            'a30009.png', 'a30010.png', 'a30011.png', 'a30012.png', 'a30013.png',
            'a30014.png', 'a30015.png', 'a40000.png', 'a40001.png', 'a40002.png',
            'a40003.png', 'a40004.png', 'a40005.png', 'a40006.png', 'a40007.png',
            'a40008.png', 'a40009.png', 'a40010.png', 'a40011.png', 'a40012.png',
            'a40013.png', 'a40014.png', 'a40015.png', 'b10000.png', 'b10001.png',
            'b10002.png', 'b10003.png', 'b10004.png', 'b10005.png', 'b10006.png',
            'b10007.png', 'b10008.png', 'b10009.png', 'b10010.png', 'b10011.png',
            'b10012.png', 'b10013.png', 'b10014.png', 'b10015.png', 'b30000.png',
            'b30001.png', 'b30002.png', 'b30003.png', 'b30004.png', 'b30005.png',
            'b30006.png', 'b30007.png', 'b30008.png', 'b30009.png', 'b30010.png',
            'b30011.png', 'b30012.png', 'b30013.png', 'b30014.png', 'b30015.png',
            'b40000.png', 'b40001.png', 'b40002.png', 'b40003.png', 'b40004.png',
            'b40005.png', 'b40006.png', 'b40007.png', 'b40008.png', 'b40009.png',
            'b40010.png', 'b40011.png', 'b40012.png', 'b40013.png', 'b40014.png',
            'b40015.png'
        ]
    ]
}


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos=None, size=2, variant=None):
        super().__init__()

        # Size determines asteroid properties (3=large, 2=medium, 1=small)
        self.size = size

        # Select appropriate asteroid sprite based on size
        if size == 3:  # Large
            size_category = "large"
        elif size == 2:  # Medium
            size_category = "medium"
        else:  # Small
            size_category = "small"

        # Select a random variant if not specified
        if variant is None:
            sprite_path = random.choice(ASTEROID_PATHS[size_category])
        else:
            # Use the specified variant if available
            matching_paths = [p for p in ASTEROID_PATHS[size_category] if variant in p.name]
            sprite_path = random.choice(matching_paths) if matching_paths else random.choice(
                ASTEROID_PATHS[size_category])

        # Load and scale the sprite
        self.large_image = pygame.image.load(sprite_path).convert_alpha()
        self.image = self.large_image.copy()  # No scaling needed as we have proper sized assets
        self.start_img = self.image

        # Set position (random if not specified)
        if pos is None:
            self.pos = self._get_random_spawn_position()
        else:
            self.pos = pygame.math.Vector2(pos)

        self.rect = self.image.get_rect(center=self.pos)

        # Set random velocity based on size
        speed = random.uniform(50, 100) / size
        angle = random.uniform(0, 360)
        self.vel = pygame.math.Vector2.from_polar((speed, angle))

        # Set rotation properties
        self.rotation = 0
        self.rotation_speed = random.uniform(-1, 1)

        # Set health and points based on size
        self.health = size * 10
        self.points = size * 10

        # Store the variant for splitting
        self.variant = sprite_path.name[:2] if variant is None else variant

    def _get_random_spawn_position(self):
        """Generate a random position outside but near the screen"""
        side = random.randint(0, 3)  # 0=top, 1=right, 2=bottom, 3=left

        if side == 0:  # Top
            return pygame.math.Vector2(
                random.randint(0, globals.WINDOW_WIDTH),
                -50
            )
        elif side == 1:  # Right
            return pygame.math.Vector2(
                globals.WINDOW_WIDTH + 50,
                random.randint(0, globals.WINDOW_HEIGHT)
            )
        elif side == 2:  # Bottom
            return pygame.math.Vector2(
                random.randint(0, globals.WINDOW_WIDTH),
                globals.WINDOW_HEIGHT + 50
            )
        else:  # Left
            return pygame.math.Vector2(
                -50,
                random.randint(0, globals.WINDOW_HEIGHT)
            )

    def update(self, dt):
        # Update position
        self.pos += self.vel * dt
        self.rect.center = self.pos

        # Update rotation
        self.rotation += self.rotation_speed
        self.image = pygame.transform.rotozoom(self.start_img, self.rotation, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Check screen boundaries
        self.check_bounds()

    def check_bounds(self):
        if self.pos.x < -100:
            self.pos.x = globals.WINDOW_WIDTH + 100
        if self.pos.x > globals.WINDOW_WIDTH + 100:
            self.pos.x = -100
        if self.pos.y < -100:
            self.pos.y = globals.WINDOW_HEIGHT + 100
        if self.pos.y > globals.WINDOW_HEIGHT + 100:
            self.pos.y = -100

    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0

    def split(self):
        """Split asteroid into smaller pieces when destroyed"""
        if self.size > 1:
            new_size = self.size - 1
            offset = 20  # Offset for new asteroids

            # Create two new smaller asteroids with the same variant
            new_asteroids = [
                Asteroid((self.pos.x + offset, self.pos.y + offset), new_size, self.variant),
                Asteroid((self.pos.x - offset, self.pos.y - offset), new_size, self.variant)
            ]

            return new_asteroids
        return []


class AsteroidManager:
    def __init__(self):
        self.asteroids = pygame.sprite.Group()
        self.spawn_timer = 0
        self.spawn_rate = 1.0  # Asteroids per second
        self.level = 1
        self.wave_active = False
        self.wave_number = 0
        self.wave_timer = 0
        self.wave_duration = 60  # 60 seconds per wave
        self.break_duration = 10  # 10 seconds between waves

    def update(self, dt, sprite_group):
        # Update wave timer
        self.wave_timer += dt

        if self.wave_active:
            # Wave is active
            if self.wave_timer >= self.wave_duration:
                # End wave
                self.wave_active = False
                self.wave_timer = 0
                return "WAVE_END"

            # Update spawn timer during active wave
            self.spawn_timer += dt
            if self.spawn_timer >= 1 / self.spawn_rate:
                self.spawn_timer = 0
                self.spawn_asteroid(sprite_group)
        else:
            # Break between waves
            if self.wave_timer >= self.break_duration:
                # Start new wave
                self.wave_active = True
                self.wave_timer = 0
                self.wave_number += 1
                self.spawn_rate = min(3.0, 1.0 + (self.wave_number * 0.2))  # Increase spawn rate with waves
                return "WAVE_START"

        return None

    def start_game(self):
        """Initialize the first wave"""
        self.wave_active = True
        self.wave_timer = 0
        self.wave_number = 1
        self.spawn_rate = 1.0
        return "WAVE_START"

    def spawn_asteroid(self, sprite_group, pos=None, size=None):
        # Create a new asteroid
        if size is None:
            size = random.choices([3, 2, 1], weights=[0.3, 0.6, 0.1])[0]

        asteroid = Asteroid(pos, size)
        self.asteroids.add(asteroid)
        sprite_group.add(asteroid)

        return asteroid

    def handle_collision(self, projectile, sprite_group):
        # Check for collisions between projectile and asteroids
        hits = pygame.sprite.spritecollide(projectile, self.asteroids, False)

        points = 0
        resources = []

        for asteroid in hits:
            if asteroid.take_damage(10):  # Projectile damage = 10
                points += asteroid.points

                # Create smaller asteroids
                new_asteroids = asteroid.split()
                for new_asteroid in new_asteroids:
                    self.asteroids.add(new_asteroid)
                    sprite_group.add(new_asteroid)

                # Generate resources at asteroid position
                if random.random() < 0.3:  # 30% chance to drop a resource
                    resource_type = random.choice(["xp", "health", "shield"])
                    resources.append((asteroid.pos, resource_type))

                # Remove the destroyed asteroid
                asteroid.kill()

        return points, resources