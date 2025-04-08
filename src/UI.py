import pygame
import pygame.freetype

from . import globals


class UI:
    def __init__(self, screen):
        self.screen = screen
        self.elements = list()

        self.scoreboard = Scoreboard((5, 5), self.screen)
        self.elements.append(self.scoreboard)

        self.lives = Lives((205, 5), screen)
        self.elements.append(self.lives)

    def update(self):
        for element in self.elements:
            element.update()

    def draw(self):
        for element in self.elements:
            element.draw()


class Scoreboard:
    def __init__(self, pos, screen):
        self.screen = screen
        self.pos = pos
        score = str(globals.SCORE)
        self.font = pygame.freetype.SysFont("Courier", 32, bold=True)
        self.image, self.rect = self.font.render(
            "Score: " + score, pygame.Color(255, 255, 255), pygame.Color(0, 0, 0)
        )
        self.rect.topleft = self.pos

    def update(self):
        score = str(globals.SCORE)
        self.image, self.rect = self.font.render(
            "Score: " + score, pygame.Color(255, 255, 255), pygame.Color(0, 0, 0)
        )
        self.rect.topleft = self.pos

    def draw(self):
        self.screen.blit(self.image, self.rect)


class Lives:
    def __init__(self, pos, screen):
        self.screen = screen
        self.pos = pos
        score = str(globals.LIVES)
        self.font = pygame.freetype.SysFont("Courier", 32, bold=True)
        self.image, self.rect = self.font.render(
            "Lives: " + score, pygame.Color(255, 255, 255), pygame.Color(0, 0, 0)
        )
        self.rect.topleft = self.pos

    def update(self):
        score = str(globals.LIVES)
        self.image, self.rect = self.font.render(
            "Lives: " + score, pygame.Color(255, 255, 255), pygame.Color(0, 0, 0)
        )
        self.rect.topleft = self.pos

    def draw(self):
        self.screen.blit(self.image, self.rect)


class StartModal(pygame.Surface):
    def __init__(self, pos):
        super().__init__((400, 400))
        self.rect = self.get_rect(center=pos)
        self.color = (122, 122, 122)
        self.fill(self.color)
        self.buttons = list()
        self.button_size = (200, 50)
        self.button_color = (0, 0, 0)

        header = pygame.freetype.SysFont("Courier", 32, bold=True)
        header_image, header_rect = header.render("Asteroid Survivors", (0,0,0))
        header_rect.center = (self.rect.width/2, 50)

        start = Button(self.button_size, (self.rect.width/2, self.rect.height/2), self.button_color, "Start")
        self.buttons.append(start)

        quit = Button(self.button_size, (self.rect.width/2, self.rect.height/2 + 75), self.button_color, "Quit")
        self.buttons.append(quit)

        self.blit(start, start.rect)
        self.blit(quit, quit.rect)
        self.blit(header_image, header_rect)

    def check_click(self, mouse):
        x_offset = self.rect.left
        y_offset = self.rect.top
        for button in self.buttons:
            temp = pygame.Rect(button.rect.left + x_offset, button.rect.top + y_offset, button.rect.w, button.rect.h)
            if temp.collidepoint(mouse):
                return button.text
            
class PauseModal(pygame.Surface):
    def __init__(self, pos):
        super().__init__((400, 400))
        self.rect = self.get_rect(center=pos)
        self.color = (122, 122, 122)
        self.fill(self.color)
        self.buttons = list()
        self.button_size = (200, 50)
        self.button_color = (0, 0, 0)

        header = pygame.freetype.SysFont("Courier", 32, bold=True)
        header_image, header_rect = header.render("Paused", (0, 0, 0))
        header_rect.center = (self.rect.width/2, 50)

        resume = Button(self.button_size, (self.rect.width/2, self.rect.height/2), self.button_color, "Resume")
        self.buttons.append(resume)

        quit = Button(self.button_size, (self.rect.width/2, self.rect.height/2 + 75), self.button_color, "Quit")
        self.buttons.append(quit)

        self.blit(resume, resume.rect)
        self.blit(quit, quit.rect)
        self.blit(header_image, header_rect)

    def check_click(self, mouse):
        x_offset = self.rect.left
        y_offset = self.rect.top
        for button in self.buttons:
            collider = pygame.Rect(button.rect.left + x_offset, button.rect.top + y_offset, button.rect.w, button.rect.h)
            if collider.collidepoint(mouse):
                return button.text
            
class EndModal(pygame.Surface):
    def __init__(self, pos):
        super().__init__((400, 400))
        self.rect = self.get_rect(center=pos)
        self.color = (122, 122, 122)
        self.fill(self.color)
        self.buttons = list()
        self.button_size = (200, 50)
        self.button_color = (0, 0, 0)

        header = pygame.freetype.SysFont("Courier", 32, bold=True)
        header_image, header_rect = header.render("Game over!", (0, 0, 0))
        header_rect.center = (self.rect.width/2, 50)

        retry = Button(self.button_size, (self.rect.width/2, self.rect.height/2), self.button_color, "Retry")
        self.buttons.append(retry)

        quit = Button(self.button_size, (self.rect.width/2, self.rect.height/2 + 75), self.button_color, "Quit")
        self.buttons.append(quit)

        self.blit(retry, retry.rect)
        self.blit(quit, quit.rect)
        self.blit(header_image, header_rect)

    def check_click(self, mouse):
        x_offset = self.rect.left
        y_offset = self.rect.top
        for button in self.buttons:
            collider = pygame.Rect(button.rect.left + x_offset, button.rect.top + y_offset, button.rect.w, button.rect.h)
            if collider.collidepoint(mouse):
                return button.text

class Button(pygame.Surface):
    def __init__(self, size, pos, color, text):
        super().__init__(size)
        self.fill(color)
        self.rect = self.get_rect(center=pos)
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
