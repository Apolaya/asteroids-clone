import pygame
from pathlib import Path

shield_path = Path("assets", "art", "pickups", "shield.png")
damage_path = Path("assets", "art", "pickups", "damage.png")
sound_path = Path("assets", "sounds", "power_up.wav")

"""Class to manage sprites for pickups that provide player boosts"""
class Pickup(pygame.sprite.Sprite):
  def __init__(self, pos, type):
    super().__init__()
    self.type = type
    if type == 'shield':
        self.image = pygame.image.load(shield_path).convert_alpha()
    elif type == 'damage':
        self.image = pygame.image.load(damage_path).convert_alpha()
    self.sprite_scaling = 0.2
    self.image = pygame.transform.scale_by(self.image, self.sprite_scaling)
    self.rect = self.image.get_rect(center=pos)
    self.sound = pygame.mixer.Sound(sound_path)
  
  def update(self):
     pass