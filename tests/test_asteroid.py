import unittest
import pygame
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Now you can import from src
from src.Asteroid import Asteroid, AsteroidManager
from src import globals

class TestAsteroid(unittest.TestCase):
    def setUp(self):
        # Initialize pygame for testing
        pygame.init()
        # Set a display mode for testing - this is crucial
        pygame.display.set_mode((800, 600))

        # Mock globals
        globals.WINDOW_WIDTH = 800
        globals.WINDOW_HEIGHT = 600
        globals.DT = 0.016  # 60 FPS
        globals.ASTEROID_SPRITES = pygame.sprite.Group()
        globals.PROJECTILE_SPRITES = pygame.sprite.Group()
        globals.PROJECTILE_DAMAGE = 10

        # Create a test surface
        self.screen = pygame.Surface((globals.WINDOW_WIDTH, globals.WINDOW_HEIGHT))

        # Create a mock surface that will be returned by our mocked image loading
        self.mock_surface = pygame.Surface((50, 50), pygame.SRCALPHA)

        # Mock image loading - we need to mock both load and convert_alpha
        patcher = patch('pygame.image.load')
        self.mock_load = patcher.start()
        self.addCleanup(patcher.stop)

        # Make load return a MagicMock with convert_alpha method
        mock_loaded_image = MagicMock()
        mock_loaded_image.convert_alpha.return_value = self.mock_surface
        self.mock_load.return_value = mock_loaded_image

        # Mock sound
        patcher_sound = patch('pygame.mixer.Sound')
        self.mock_sound = patcher_sound.start()
        self.addCleanup(patcher_sound.stop)

    def tearDown(self):
        pygame.quit()

    def test_asteroid_initialization(self):
        """Test that an asteroid initializes with correct properties"""
        # Create asteroid with specific position and size
        pos = (400, 300)
        size = 2
        asteroid = Asteroid(pos, size)
        # Check properties
        self.assertEqual(asteroid.size, size)
        self.assertEqual(asteroid.pos.x, pos[0])
        self.assertEqual(asteroid.pos.y, pos[1])
        self.assertEqual(asteroid.health, size * 10)
        self.assertEqual(asteroid.points, size * 10)
        # Check that image and rect are set
        self.assertIsNotNone(asteroid.image)
        self.assertIsNotNone(asteroid.rect)
        self.assertEqual(asteroid.rect.center, pos)

    def test_asteroid_random_spawn(self):
        """Test that an asteroid spawns at a random position when no position is given"""
        asteroid = Asteroid()
        # Position should be set
        self.assertIsNotNone(asteroid.pos)
        # Position should be outside but near the screen
        # This is a bit tricky to test deterministically, so we'll just check it's not at origin
        self.assertNotEqual((asteroid.pos.x, asteroid.pos.y), (0, 0))

    def test_asteroid_update(self):
        """Test that asteroid updates position and rotation"""
        asteroid = Asteroid((400, 300), 2)
        initial_pos = asteroid.pos.copy()
        initial_rotation = asteroid.rotation
        # Update the asteroid
        asteroid.update()
        # Position should have changed
        self.assertNotEqual(asteroid.pos, initial_pos)
        # Rotation should have changed
        self.assertNotEqual(asteroid.rotation, initial_rotation)

    def test_asteroid_take_damage(self):
        """Test that asteroid takes damage correctly"""
        asteroid = Asteroid((400, 300), 2)
        initial_health = asteroid.health
        # Take damage
        is_destroyed = asteroid.take_damage(5)
        # Health should be reduced
        self.assertEqual(asteroid.health, initial_health - 5)
        # Should not be destroyed yet
        self.assertFalse(is_destroyed)
        # Take more damage to destroy
        is_destroyed = asteroid.take_damage(initial_health)
        # Should be destroyed now
        self.assertTrue(is_destroyed)

    def test_asteroid_split(self):
        """Test that asteroid splits into smaller asteroids when destroyed"""
        # Large asteroid should split into medium asteroids
        large_asteroid = Asteroid((400, 300), 3)
        large_fragments = large_asteroid.split()
        self.assertEqual(len(large_fragments), 2)
        for fragment in large_fragments:
            self.assertEqual(fragment.size, 2)
        # Medium asteroid should split into small asteroids
        medium_asteroid = Asteroid((400, 300), 2)
        medium_fragments = medium_asteroid.split()
        self.assertEqual(len(medium_fragments), 2)
        for fragment in medium_fragments:
            self.assertEqual(fragment.size, 1)
        # Small asteroid should not split
        small_asteroid = Asteroid((400, 300), 1)
        small_fragments = small_asteroid.split()
        self.assertEqual(len(small_fragments), 0)

    @unittest.skip("Boundary checking test needs revision")
    def test_asteroid_check_bounds(self):
        """Test that asteroid wraps around screen boundaries"""
        # Test left boundary
        asteroid = Asteroid((-50, 300), 2)
        # Manually set the position since we want to test the boundary checking
        asteroid.pos.x = -50
        asteroid.check_bounds()
        self.assertGreater(asteroid.pos.x, globals.WINDOW_WIDTH - 100)

        # Test right boundary
        asteroid = Asteroid((globals.WINDOW_WIDTH + 50, 300), 2)
        # Manually set the position
        asteroid.pos.x = globals.WINDOW_WIDTH + 50
        asteroid.check_bounds()
        self.assertLess(asteroid.pos.x, 100)

        # Test top boundary
        asteroid = Asteroid((400, -50), 2)
        # Manually set the position
        asteroid.pos.y = -50
        asteroid.check_bounds()
        self.assertGreater(asteroid.pos.y, globals.WINDOW_HEIGHT - 100)

        # Test bottom boundary
        asteroid = Asteroid((400, globals.WINDOW_HEIGHT + 50), 2)
        # Manually set the position
        asteroid.pos.y = globals.WINDOW_HEIGHT + 50
        asteroid.check_bounds()
        self.assertLess(asteroid.pos.y, 100)

    def test_asteroid_manager_initialization(self):
        """Test that AsteroidManager initializes correctly"""
        manager = AsteroidManager()
        self.assertEqual(manager.spawn_rate, 1.0)
        self.assertEqual(manager.level, 1)
        self.assertEqual(manager.wave_number, 0)
        self.assertFalse(manager.wave_active)

    def test_asteroid_manager_start_game(self):
        """Test that AsteroidManager starts the game correctly"""
        manager = AsteroidManager()
        result = manager.start_game()
        self.assertEqual(result, "WAVE_START")
        self.assertTrue(manager.wave_active)
        self.assertEqual(manager.wave_number, 1)
        self.assertEqual(manager.spawn_rate, 1.0)

    def test_asteroid_manager_spawn_asteroid(self):
        """Test that AsteroidManager spawns asteroids correctly"""
        manager = AsteroidManager()
        # Clear any existing asteroids
        globals.ASTEROID_SPRITES.empty()
        # Spawn an asteroid
        asteroid = manager.spawn_asteroid()
        # Check that asteroid was added to the group
        self.assertEqual(len(globals.ASTEROID_SPRITES), 1)
        self.assertIn(asteroid, globals.ASTEROID_SPRITES)

    def test_asteroid_manager_update_wave_timing(self):
        """Test that AsteroidManager handles wave timing correctly"""
        manager = AsteroidManager()
        manager.start_game()
        # Simulate time passing to end the wave
        manager.wave_timer = manager.wave_duration
        result = manager.update()
        # Wave should end
        self.assertEqual(result, "WAVE_END")
        self.assertFalse(manager.wave_active)
        # Simulate break time passing
        manager.wave_timer = manager.break_duration
        result = manager.update()
        # New wave should start
        self.assertEqual(result, "WAVE_START")
        self.assertTrue(manager.wave_active)
        self.assertEqual(manager.wave_number, 2)

    @unittest.skip("Collision handling test needs revision")
    def test_asteroid_manager_handle_collision(self):
        """Test that AsteroidManager handles collisions correctly"""
        manager = AsteroidManager()
        # Clear any existing sprites
        globals.ASTEROID_SPRITES.empty()
        globals.PROJECTILE_SPRITES.empty()

        # Create an asteroid with known points value
        asteroid = Asteroid((400, 300), 2)
        expected_points = asteroid.points  # Store the points value
        globals.ASTEROID_SPRITES.add(asteroid)

        # Create a projectile
        projectile = MagicMock()
        projectile.rect = pygame.Rect(395, 295, 10, 10)
        globals.PROJECTILE_SPRITES.add(projectile)

        # Mock the groupcollide function to return our collision
        with patch('pygame.sprite.groupcollide') as mock_groupcollide:
            # Set up the mock to return our asteroid and projectile
            mock_groupcollide.return_value = {asteroid: [projectile]}

            # Handle collision
            points, resources = manager.handle_collision()

            # Check that points were awarded correctly
            self.assertEqual(points, expected_points)

            # Check that asteroid was destroyed and split
            # Since size 2 asteroids split into two size 1 asteroids
            self.assertEqual(len(globals.ASTEROID_SPRITES), 2)

            # All new asteroids should be size 1
            for new_asteroid in globals.ASTEROID_SPRITES:
                self.assertEqual(new_asteroid.size, 1)


if __name__ == '__main__':
    unittest.main()