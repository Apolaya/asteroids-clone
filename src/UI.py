import pygame
import pygame.freetype


"""Class to handle loading and refreshing of UI elements."""
class UI():
    def __init__(self, screen):
        self.screen = screen
        self.children = list()
    
    def add(self, element):
        if not isinstance(element, pygame.Surface):
            raise TypeError('Must be a Pygame Surface')
        self.children.append(element)
    
    def remove(self, element):
        self.children.remove(element)
    
    def clear(self):
        for child in self.children:
            if hasattr(child, 'children'):
                child.children.clear()
        self.children.clear()

    def draw(self):
        for element in self.children:
            element.draw(self.screen)

"""Class for modal UI elements"""
class Modal(pygame.Surface):
    def __init__(self, pos, size, color):
        super().__init__(size)
        self.parent = None
        self.rect = self.get_rect(topleft=pos)
        self.color = color
        self.fill(color)
        self.children = list()
    
    def add(self, element):
        if(not isinstance(element, (Text, Button))):
            raise TypeError('Must be Button or Text')
        element.parent = self
        self.children.append(element)
    
    def add_all(self, elements):
        for element in elements:
            self.add(element)
    
    def remove(self, element):
        self.children.remove(element)
    
    def remove_all(self, elements):
        for element in elements:
            self.children.remove(element)
    
    def clear(self):
        self.children.clear()
        self.fill(self.color)

    def draw(self, screen):
        for child in self.children:
            child.draw(screen)
            self.blit(child, child.rect)
        parent = self.parent or screen
        parent.blit(self, self.rect)
    
    """Check if a click falls in the bounds of a button on this modal."""
    def check_click(self, mouse):
        x_offset = self.rect.left
        y_offset = self.rect.top
        for child in self.children:
            if isinstance(child, Button):
              collider = pygame.Rect(child.rect.left + x_offset, child.rect.top + y_offset, child.rect.w, child.rect.h)
              if collider.collidepoint(mouse):
                  return child.text

"""Class to create a Button UI element"""
class Button(pygame.Surface):
    """Initialize the instance with Surface and text properties."""
    def __init__(self, pos, size, color, text=''):
        super().__init__(size)
        self.color = color
        self.fill(color)
        self.parent = None
        self.children = list()
        self.rect = self.get_rect(topleft=pos)
        self.text = text
        self.label = pygame.freetype.SysFont("Courier", 32, bold=True)
        self.label_image, self.label_rect = self.label.render(self.text, (123, 107, 189))
        self.blit(
            self.label_image,
            (
                self.get_rect().centerx - self.label_rect.width / 2,
                self.get_rect().centery - self.label_rect.height / 2,
            ),
        )
    
    def add(self, element):
        if(not isinstance(element, (Text, Button))):
            raise TypeError('Must be a UI element')
        element.parent = self
        self.children.append(element)
    
    def add_all(self, elements):
        for element in elements:
            self.add(element)
    
    def remove(self, element):
        self.children.remove(element)
    
    def remove_all(self, elements):
        for element in elements:
            self.children.remove(element)
    
    def clear(self):
        self.children.clear()

    def draw(self, screen):
        for child in self.children:
            child.draw(screen)
            self.blit(child, child.rect)
        parent = self.parent or screen
        parent.blit(self, self.rect)
    
    def set_text(self, text):
        self.fill(self.color)
        self.text = text
        self.label_image, self.label_rect = self.label.render(self.text, (123, 107, 189))
        self.blit(
            self.label_image,
            (
                self.get_rect().centerx - self.label_rect.width / 2,
                self.get_rect().centery - self.label_rect.height / 2,
            ),
        )


"""Class to create a Text UI element"""
class Text(pygame.Surface):
    def __init__(self, pos, fontsize, color, text, font, bold=False, italic=False):
        super().__init__((0,0))
        self.text = text
        self.font = pygame.freetype.SysFont(font, fontsize, bold, italic)
        self.color = color
        self.image, self.rect = self.font.render(text, color)
        self.rect.topleft = pos
        self.parent = None

    def draw(self, screen):
        parent = self.parent or screen
        parent.blit(self.image, self.rect)
    
    def set_text(self, text):
        pos = self.rect
        self.text = text
        self.image, self.rect = self.font.render(text, self.color)
        self.rect.center = pos.center
