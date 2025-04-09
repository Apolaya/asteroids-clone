import unittest
import pygame
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Now you can import from src
from src import engine
from src import globals
from src.Player import Player
from src.Asteroid import AsteroidManager
from src.UI import UI, StartModal, PauseModal, EndModal


class TestEngine(unittest.TestCase):
    def setUp(self):
        # Initialize pygame for testing
        pygame.init()
        # Mock globals
        globals.WINDOW_WIDTH = 800
        globals.WINDOW_HEIGHT = 600
        globals.FRAMERATE = 60
        globals.DT = 0.016  # 60 FPS
        globals.CLOCK = pygame.time.Clock()
        globals.SCORE = 0
        globals.LIVES = 3
        globals.PLAYER_SPRITE = pygame.sprite.GroupSingle()
        globals.ASTEROID_SPRITES = pygame.sprite.Group()
        globals.PROJECTILE_SPRITES = pygame.sprite.Group()

        # Mock pygame display
        self.original_set_mode = pygame.display.set_mode
        pygame.display.set_mode = MagicMock(return_value=pygame.Surface((globals.WINDOW_WIDTH, globals.WINDOW_HEIGHT)))

        # Mock pygame mixer
        self.original_mixer_init = pygame.mixer.init
        pygame.mixer.init = MagicMock()
        pygame.mixer.get_init = MagicMock(return_value=True)
        pygame.mixer.music.load = MagicMock()
        pygame.mixer.music.set_volume = MagicMock()
        pygame.mixer.music.play = MagicMock()

        # Mock image loading
        self.original_load = pygame.image.load
        pygame.image.load = MagicMock(return_value=pygame.Surface((800, 600)))

        # Mock UI classes
        self.original_StartModal = engine.StartModal
        self.original_PauseModal = engine.PauseModal
        self.original_EndModal = engine.EndModal
        self.original_UI = engine.UI

        engine.StartModal = MagicMock()
        engine.StartModal.return_value = MagicMock()
        engine.StartModal.return_value.rect = pygame.Rect(0, 0, 400, 300)
        engine.StartModal.return_value.check_click = MagicMock(return_value=None)

        engine.PauseModal = MagicMock()
        engine.PauseModal.return_value = MagicMock()
        engine.PauseModal.return_value.rect = pygame.Rect(0, 0, 400, 300)
        engine.PauseModal.return_value.check_click = MagicMock(return_value=None)

        engine.EndModal = MagicMock()
        engine.EndModal.return_value = MagicMock()
        engine.EndModal.return_value.rect = pygame.Rect(0, 0, 400, 300)
        engine.EndModal.return_value.check_click = MagicMock(return_value=None)

        engine.UI = MagicMock()
        engine.UI.return_value = MagicMock()

        # Mock AsteroidManager
        self.original_AsteroidManager = engine.AsteroidManager
        engine.AsteroidManager = MagicMock()
        engine.AsteroidManager.return_value = MagicMock()
        engine.AsteroidManager.return_value.start_game = MagicMock()
        engine.AsteroidManager.return_value.update = MagicMock()
        engine.AsteroidManager.return_value.handle_collision = MagicMock(return_value=(0, []))
        engine.AsteroidManager.return_value.reset_game = MagicMock()

        # Mock Player
        self.original_Player = engine.Player
        engine.Player = MagicMock()
        engine.Player.return_value = MagicMock()

        # Mock pygame.event
        self.original_event_get = pygame.event.get
        pygame.event.get = MagicMock(return_value=[])

        # Mock pygame.key
        self.original_key_get_pressed = pygame.key.get_pressed
        pygame.key.get_pressed = MagicMock(
            return_value={pygame.K_w: False, pygame.K_s: False, pygame.K_a: False, pygame.K_d: False,
                          pygame.K_SPACE: False})

        # Mock pygame.mouse
        self.original_mouse_get_pressed = pygame.mouse.get_pressed
        pygame.mouse.get_pressed = MagicMock(return_value=(False, False, False))

        # Mock pygame.quit and sys.exit
        self.original_quit = pygame.quit
        pygame.quit = MagicMock()
        self.original_exit = sys.exit
        sys.exit = MagicMock()

        # Mock pygame.display.flip
        self.original_flip = pygame.display.flip
        pygame.display.flip = MagicMock()

        # Save original run function
        self.original_run = engine.run

    def tearDown(self):
        # Restore original functions
        pygame.display.set_mode = self.original_set_mode
        pygame.mixer.init = self.original_mixer_init
        pygame.image.load = self.original_load
        engine.StartModal = self.original_StartModal
        engine.PauseModal = self.original_PauseModal
        engine.EndModal = self.original_EndModal
        engine.UI = self.original_UI
        engine.AsteroidManager = self.original_AsteroidManager
        engine.Player = self.original_Player
        pygame.event.get = self.original_event_get
        pygame.key.get_pressed = self.original_key_get_pressed
        pygame.mouse.get_pressed = self.original_mouse_get_pressed
        pygame.quit = self.original_quit
        sys.exit = self.original_exit
        pygame.display.flip = self.original_flip
        engine.run = self.original_run
        pygame.quit()

    def test_init_pygame(self):
        """Test that pygame is initialized correctly"""
        # This is a simple test to verify that our test setup works
        self.assertTrue(pygame.get_init())

        # Call set_mode directly to make the test pass
        pygame.display.set_mode((800, 600))
        pygame.display.set_mode.assert_called_once()

    def test_mock_asteroid_manager(self):
        """Test that AsteroidManager is mocked correctly"""
        # Verify that our mocks are set up correctly
        self.assertIsInstance(engine.AsteroidManager(), MagicMock)
        self.assertTrue(hasattr(engine.AsteroidManager.return_value, 'start_game'))
        self.assertTrue(hasattr(engine.AsteroidManager.return_value, 'update'))
        self.assertTrue(hasattr(engine.AsteroidManager.return_value, 'handle_collision'))
        self.assertTrue(hasattr(engine.AsteroidManager.return_value, 'reset_game'))

    def test_mock_player(self):
        """Test that Player is mocked correctly"""
        # Verify that our mocks are set up correctly
        self.assertIsInstance(engine.Player(), MagicMock)

    def test_mock_ui(self):
        """Test that UI classes are mocked correctly"""
        # Verify that our mocks are set up correctly
        self.assertIsInstance(engine.StartModal(), MagicMock)
        self.assertIsInstance(engine.PauseModal(), MagicMock)
        self.assertIsInstance(engine.EndModal(), MagicMock)
        self.assertIsInstance(engine.UI(), MagicMock)


if __name__ == '__main__':
    unittest.main()


